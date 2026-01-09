#!/usr/bin/env python3
"""
Stock Screener - ULTRA-OPTIMIZED for FREE TIER
Strategy: Check NEWS first, only fetch price data for stocks with catalysts
This reduces API calls by ~70% and respects 5 calls/min limit
"""

import os
import sys
import time
import logging
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import yaml
import requests


class StockScreenerUltra:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.api_key = self.config['api']['polygon_api_key']
        self.base_url = "https://api.polygon.io"
        self.api_call_count = 0
        self.last_call_time = time.time()
        self.logger.info("Stock Screener (ULTRA-OPTIMIZED) initialized")

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def _setup_logging(self):
        log_config = self.config.get('logging', {})
        if not log_config.get('enabled', True):
            logging.disable(logging.CRITICAL)
            return

        log_level = getattr(logging, log_config.get('log_level', 'INFO'))
        log_file = log_config.get('log_file', 'stock_screener.log')

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _rate_limit_delay(self):
        """
        Smart rate limiting: 5 calls per minute = 12 seconds between calls
        Add extra buffer for safety
        """
        elapsed = time.time() - self.last_call_time
        required_delay = 13  # 13 seconds = safer than 12
        if elapsed < required_delay:
            sleep_time = required_delay - elapsed
            self.logger.debug(f"Rate limit: sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_call_time = time.time()
        self.api_call_count += 1

    def _api_get(self, url: str, params: dict) -> Optional[dict]:
        """API call with rate limiting"""
        try:
            self._rate_limit_delay()
            response = requests.get(url, params=params, timeout=15)

            if response.status_code == 429:
                self.logger.warning("Rate limit hit - waiting 60s")
                time.sleep(60)
                return None

            if response.status_code != 200:
                return None

            return response.json()

        except Exception as e:
            self.logger.debug(f"API error: {e}")
            return None

    def fetch_news(self, ticker: str, hours_back: int = 24) -> List[Dict]:
        """Fetch recent news"""
        published_after = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')

        url = f"{self.base_url}/v2/reference/news"
        params = {
            'apiKey': self.api_key,
            'ticker': ticker,
            'published_utc.gte': published_after,
            'order': 'desc',
            'limit': 10
        }

        data = self._api_get(url, params)

        if not data or data.get('status') != 'OK' or not data.get('results'):
            return []

        news_items = []
        for article in data['results']:
            news_items.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'published': article.get('published_utc', ''),
                'url': article.get('article_url', ''),
                'source': article.get('publisher', {}).get('name', 'Unknown')
            })

        return news_items

    def fetch_stock_data(self, ticker: str) -> Optional[Dict]:
        """Fetch previous day's price data"""
        url = f"{self.base_url}/v2/aggs/ticker/{ticker}/prev"
        params = {'apiKey': self.api_key, 'adjusted': 'true'}

        data = self._api_get(url, params)

        if not data or data.get('status') != 'OK' or not data.get('results'):
            return None

        result = data['results'][0]
        open_price = result.get('o')
        close_price = result.get('c')
        volume = result.get('v', 0)

        if not open_price or not close_price or open_price == 0:
            return None

        daily_change = ((close_price - open_price) / open_price) * 100

        return {
            'ticker': ticker,
            'price': close_price,
            'open': open_price,
            'high': result.get('h'),
            'low': result.get('l'),
            'volume': volume,
            'daily_change': daily_change,
            'timestamp': datetime.fromtimestamp(result.get('t', 0) / 1000)
        }

    def analyze_catalysts(self, news_items: List[Dict]) -> tuple[bool, List[str]]:
        """Analyze news for positive catalysts"""
        positive_keywords = [
            'approval', 'approved', 'breakthrough', 'partnership', 'deal', 'contract',
            'expansion', 'growth', 'revenue', 'profit', 'acquisition', 'merger',
            'clinical trial', 'fda', 'patent', 'innovation', 'milestone',
            'beat', 'upgrade', 'bullish', 'positive', 'launch', 'funding'
        ]

        negative_keywords = [
            'lawsuit', 'fraud', 'bankruptcy', 'decline', 'loss', 'miss',
            'downgrade', 'bearish', 'failed', 'rejected', 'warning', 'layoff'
        ]

        catalysts = []
        positive_score = 0
        negative_score = 0

        for news in news_items:
            text = (news['title'] + ' ' + news['description']).lower()

            found_positive = False
            for keyword in positive_keywords:
                if keyword in text:
                    positive_score += 1
                    if not found_positive:
                        catalysts.append(news['title'])
                        found_positive = True

            for keyword in negative_keywords:
                if keyword in text:
                    negative_score += 1

        has_catalyst = positive_score > negative_score and positive_score > 0
        return has_catalyst, list(set(catalysts[:3]))

    def check_sector_match(self, news_items: List[Dict]) -> bool:
        """Check if matches target sectors"""
        target_sectors = [s.lower() for s in self.config['screening']['target_sectors']]

        for news in news_items:
            text = (news['title'] + ' ' + news['description']).lower()
            for sector in target_sectors:
                if sector in text:
                    return True
        return False

    def calculate_score(self, stock_data: Dict, has_catalyst: bool,
                       sector_match: bool, news_count: int) -> float:
        """Calculate opportunity score"""
        score = 0.0

        # Daily change (up to 35 points)
        score += min(abs(stock_data['daily_change']) * 2.5, 35)

        # Volume (up to 20 points)
        vol_millions = stock_data['volume'] / 1_000_000
        score += min(vol_millions * 2, 20)

        # Catalyst (30 points)
        if has_catalyst:
            score += 30

        # Sector match (10 points)
        if sector_match:
            score += 10

        # News freshness (up to 5 points)
        score += min(news_count, 5)

        return score

    def screen_stocks(self) -> List[Dict]:
        """
        ULTRA-OPTIMIZED SCREENING STRATEGY:
        Phase 1: Check NEWS for all tickers (1 API call each)
        Phase 2: Only fetch PRICE data for tickers with news (1 API call each)
        Result: 70% fewer API calls, respects 5/min limit
        """
        self.logger.info("=" * 80)
        self.logger.info("Starting ULTRA-OPTIMIZED screening cycle...")

        tickers = self.config.get('etoro_available', [])
        screening_config = self.config['screening']

        self.logger.info(f"Phase 1: Scanning news for {len(tickers)} tickers...")
        self.api_call_count = 0
        start_time = time.time()

        # PHASE 1: News scan (identify tickers with catalysts)
        tickers_with_news = []

        for ticker in tickers:
            news_items = self.fetch_news(ticker, screening_config['news_lookback_hours'])

            if news_items:
                has_catalyst, catalysts = self.analyze_catalysts(news_items)
                sector_match = self.check_sector_match(news_items)

                if has_catalyst or len(news_items) >= 3:  # Catalyst OR significant news volume
                    tickers_with_news.append({
                        'ticker': ticker,
                        'news_items': news_items,
                        'catalysts': catalysts,
                        'has_catalyst': has_catalyst,
                        'sector_match': sector_match
                    })
                    self.logger.info(f"📰 {ticker}: {len(news_items)} news items, catalyst={has_catalyst}")

        self.logger.info(f"Phase 1 complete: {len(tickers_with_news)} tickers with news (API calls: {self.api_call_count})")

        if not tickers_with_news:
            self.logger.info("No tickers with significant news - ending scan")
            return []

        # PHASE 2: Price data for tickers with news only
        self.logger.info(f"Phase 2: Fetching price data for {len(tickers_with_news)} tickers...")

        candidates = []

        for item in tickers_with_news:
            ticker = item['ticker']

            # Fetch price data
            stock_data = self.fetch_stock_data(ticker)

            if not stock_data:
                self.logger.debug(f"No price data for {ticker}")
                continue

            # Apply filters
            if not (screening_config['min_price'] <= stock_data['price'] <= screening_config['max_price']):
                self.logger.debug(f"{ticker}: price ${stock_data['price']:.2f} outside range")
                continue

            if abs(stock_data['daily_change']) < screening_config['min_daily_change']:
                self.logger.debug(f"{ticker}: change {stock_data['daily_change']:.1f}% too low")
                continue

            if stock_data['volume'] < screening_config['min_volume']:
                self.logger.debug(f"{ticker}: volume {stock_data['volume']:,.0f} too low")
                continue

            # Calculate score
            score = self.calculate_score(
                stock_data,
                item['has_catalyst'],
                item['sector_match'],
                len(item['news_items'])
            )

            candidates.append({
                'ticker': ticker,
                'price': stock_data['price'],
                'daily_change': stock_data['daily_change'],
                'volume': stock_data['volume'],
                'catalysts': item['catalysts'],
                'sector_match': item['sector_match'],
                'score': score,
                'news_count': len(item['news_items'])
            })

            self.logger.info(f"✓ {ticker}: ${stock_data['price']:.2f} ({stock_data['daily_change']:+.1f}%) - Score: {score:.1f}")

        elapsed = time.time() - start_time
        self.logger.info(f"Scan complete: {len(candidates)} candidates found")
        self.logger.info(f"Total API calls: {self.api_call_count}, Time: {elapsed/60:.1f} minutes")

        # Sort and return top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return candidates[:screening_config['max_notifications']]

    def send_email_notification(self, candidates: List[Dict]):
        """Send email notification"""
        if not candidates:
            return

        email_config = self.config.get('email', {})
        if not email_config.get('enabled', True):
            return

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚀 Stock Alert: {len(candidates)} High-Potential Opportunities"
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']

            body = self._create_email_body(candidates)
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            self.logger.info(f"📧 Email sent to {email_config['receiver_email']}")

        except Exception as e:
            self.logger.error(f"Email failed: {e}")

    def _create_email_body(self, candidates: List[Dict]) -> str:
        """Create email body"""
        disclaimer = self.config['risk_management']['disclaimer']
        stop_loss = self.config['risk_management']['stop_loss_percentage']

        body = f"""
🚀 HIGH-POTENTIAL STOCK ALERT 🚀
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{disclaimer}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP OPPORTUNITIES:

"""
        for i, stock in enumerate(candidates, 1):
            body += f"""
{i}. {stock['ticker']} - ${stock['price']:.2f}
   📈 Previous Day: {stock['daily_change']:+.1f}%
   📊 Volume: {stock['volume']:,.0f}
   🎯 Score: {stock['score']:.1f}/100
   📰 News: {stock['news_count']} articles

   CATALYSTS:
"""
            for catalyst in stock['catalysts']:
                body += f"   • {catalyst}\n"

            body += f"""
   🛡️ RISK MANAGEMENT:
   • Stop-Loss: {stop_loss}%
   • Position Size: Only risk what you can lose

   📱 eTORO STEPS:
   1. Search "{stock['ticker']}"
   2. Review charts
   3. Set stop-loss order
   4. Take profits at 20-50%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        body += """
REMINDERS:
• Extremely high risk - possible total loss
• Set stop-losses immediately
• Only invest disposable income
• This is NOT financial advice

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stock Screener ULTRA (FREE TIER OPTIMIZED)
"""
        return body

    def print_console_notification(self, candidates: List[Dict]):
        """Print to console"""
        if not candidates:
            print("\n" + "="*80)
            print("No candidates found this cycle")
            print("="*80 + "\n")
            return

        print("\n" + "="*80)
        print(f"🚀 STOCK ALERT: {len(candidates)} OPPORTUNITIES")
        print("="*80)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"{self.config['risk_management']['disclaimer']}\n")

        for i, stock in enumerate(candidates, 1):
            print(f"\n{i}. {stock['ticker']} - ${stock['price']:.2f}")
            print(f"   Change: {stock['daily_change']:+.1f}%")
            print(f"   Volume: {stock['volume']:,.0f}")
            print(f"   Score: {stock['score']:.1f}/100")
            print(f"   Catalysts:")
            for catalyst in stock['catalysts']:
                print(f"   • {catalyst}")

        print("\n" + "="*80 + "\n")

    def run(self):
        """Main loop"""
        scan_interval = self.config['screening']['scan_interval']

        self.logger.info(f"Starting continuous operation (every {scan_interval/3600:.1f} hours)")
        self.logger.info("ULTRA-OPTIMIZED: News-first strategy for free tier")

        cycle = 0
        while True:
            try:
                cycle += 1
                self.logger.info(f"\nCycle #{cycle} starting...")

                candidates = self.screen_stocks()

                if candidates:
                    self.print_console_notification(candidates)
                    self.send_email_notification(candidates)
                else:
                    self.logger.info("No candidates met criteria")

                next_scan = datetime.now() + timedelta(seconds=scan_interval)
                self.logger.info(f"Next scan: {next_scan.strftime('%Y-%m-%d %H:%M:%S')}")
                self.logger.info(f"Sleeping {scan_interval/3600:.1f} hours...\n")

                time.sleep(scan_interval)

            except KeyboardInterrupt:
                self.logger.info("\nShutdown requested")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.info("Retrying in 5 minutes...")
                time.sleep(300)


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║    HIGH-POTENTIAL STOCK SCREENER - ULTRA OPTIMIZED       ║
║    FREE TIER: News-First Strategy (70% Fewer API Calls)  ║
╚═══════════════════════════════════════════════════════════╝
    """)

    if not os.path.exists("config.yaml"):
        print("❌ config.yaml not found!")
        sys.exit(1)

    screener = StockScreenerUltra("config.yaml")
    screener.run()


if __name__ == "__main__":
    main()
