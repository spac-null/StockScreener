#!/usr/bin/env python3
"""
Stock Screener for High-Potential Low-Priced Stocks (FREE TIER OPTIMIZED)
Uses Polygon free tier endpoints cleverly to achieve the same goal
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


class StockScreenerFree:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.api_key = self.config['api']['polygon_api_key']
        self.base_url = "https://api.polygon.io"
        self.logger.info("Stock Screener (FREE TIER) initialized successfully")

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Error: Config file '{config_path}' not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
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

    def get_etoro_tickers(self) -> List[str]:
        tickers = self.config.get('etoro_available', [])
        self.logger.info(f"Loaded {len(tickers)} eToro-available tickers")
        return tickers

    def fetch_previous_day_data(self, ticker: str) -> Optional[Dict]:
        """
        Fetch previous day's aggregate data using free-tier endpoint
        Uses: /v2/aggs/ticker/{ticker}/prev
        """
        try:
            url = f"{self.base_url}/v2/aggs/ticker/{ticker}/prev"
            params = {'apiKey': self.api_key, 'adjusted': 'true'}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 403:
                self.logger.debug(f"API key not authorized for {ticker}")
                return None

            if response.status_code != 200:
                self.logger.debug(f"No data for {ticker}: HTTP {response.status_code}")
                return None

            data = response.json()

            if data.get('status') != 'OK' or not data.get('results'):
                return None

            result = data['results'][0]

            # Calculate daily change from open to close
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

        except Exception as e:
            self.logger.debug(f"Error fetching data for {ticker}: {e}")
            return None

    def fetch_recent_aggregates(self, ticker: str, days: int = 5) -> Optional[List[Dict]]:
        """
        Fetch last N days of data to detect momentum trends
        Uses: /v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}
        """
        try:
            to_date = datetime.now().strftime('%Y-%m-%d')
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

            url = f"{self.base_url}/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}"
            params = {'apiKey': self.api_key, 'adjusted': 'true', 'sort': 'desc', 'limit': days}

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()

            if data.get('status') != 'OK' or not data.get('results'):
                return None

            results = []
            for bar in data['results']:
                results.append({
                    'date': datetime.fromtimestamp(bar['t'] / 1000),
                    'open': bar['o'],
                    'close': bar['c'],
                    'high': bar['h'],
                    'low': bar['l'],
                    'volume': bar['v']
                })

            return results

        except Exception as e:
            self.logger.debug(f"Error fetching aggregates for {ticker}: {e}")
            return None

    def fetch_news(self, ticker: str, hours_back: int = 24) -> List[Dict]:
        """
        Fetch recent news (FREE TIER AVAILABLE)
        Uses: /v2/reference/news
        """
        try:
            published_after = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')

            url = f"{self.base_url}/v2/reference/news"
            params = {
                'apiKey': self.api_key,
                'ticker': ticker,
                'published_utc.gte': published_after,
                'order': 'desc',
                'limit': 10
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                self.logger.debug(f"News API error for {ticker}: HTTP {response.status_code}")
                return []

            data = response.json()

            if data.get('status') != 'OK' or not data.get('results'):
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

        except Exception as e:
            self.logger.debug(f"Error fetching news for {ticker}: {e}")
            return []

    def analyze_catalysts(self, news_items: List[Dict]) -> tuple[bool, List[str]]:
        positive_keywords = [
            'approval', 'approved', 'breakthrough', 'partnership', 'deal', 'contract',
            'expansion', 'growth', 'revenue', 'profit', 'acquisition', 'merger',
            'clinical trial', 'fda', 'patent', 'innovation', 'milestone',
            'beat expectations', 'upgrade', 'bullish', 'positive results',
            'new product', 'launch', 'collaboration', 'investment', 'funding',
            'earnings beat', 'contract win', 'regulatory approval'
        ]

        negative_keywords = [
            'lawsuit', 'investigation', 'fraud', 'bankruptcy', 'decline',
            'loss', 'miss', 'downgrade', 'bearish', 'failed', 'rejected',
            'warning', 'recall', 'delay', 'cut', 'layoff'
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
                        catalysts.append(f"{news['title']}")
                        found_positive = True

            for keyword in negative_keywords:
                if keyword in text:
                    negative_score += 1

        has_catalyst = positive_score > 0 and positive_score > negative_score
        return has_catalyst, list(set(catalysts[:3]))

    def check_sector_match(self, ticker: str, news_items: List[Dict]) -> bool:
        target_sectors = [s.lower() for s in self.config['screening']['target_sectors']]

        for news in news_items:
            text = (news['title'] + ' ' + news['description']).lower()
            for sector in target_sectors:
                if sector in text:
                    return True

        return False

    def analyze_momentum(self, aggregates: List[Dict]) -> Dict:
        """
        Analyze multi-day momentum for additional scoring
        """
        if not aggregates or len(aggregates) < 2:
            return {'trend': 'neutral', 'strength': 0}

        # Count up days vs down days
        up_days = 0
        down_days = 0
        total_change = 0

        for i in range(len(aggregates) - 1):
            current = aggregates[i]
            if current['close'] > current['open']:
                up_days += 1
                change_pct = ((current['close'] - current['open']) / current['open']) * 100
                total_change += change_pct
            else:
                down_days += 1

        trend = 'bullish' if up_days > down_days else 'bearish' if down_days > up_days else 'neutral'
        strength = min(abs(total_change), 20)  # Cap at 20 points

        return {'trend': trend, 'strength': strength, 'up_days': up_days, 'total_days': len(aggregates)}

    def calculate_score(self, stock_data: Dict, has_catalyst: bool, sector_match: bool, momentum: Dict) -> float:
        score = 0.0

        # Daily change weight (up to 30 points)
        score += min(abs(stock_data['daily_change']) * 2, 30)

        # Volume weight (up to 15 points)
        vol_millions = stock_data['volume'] / 1_000_000
        score += min(vol_millions * 1.5, 15)

        # Catalyst weight (25 points)
        if has_catalyst:
            score += 25

        # Sector match weight (10 points)
        if sector_match:
            score += 10

        # Momentum weight (up to 20 points)
        if momentum['trend'] == 'bullish':
            score += momentum['strength']

        return score

    def screen_stocks(self) -> List[Dict]:
        self.logger.info("=" * 80)
        self.logger.info("Starting stock screening cycle (FREE TIER MODE)...")

        tickers = self.get_etoro_tickers()
        screening_config = self.config['screening']

        candidates = []
        api_calls = 0

        for ticker in tickers:
            try:
                # Fetch previous day data
                stock_data = self.fetch_previous_day_data(ticker)
                api_calls += 1

                if not stock_data:
                    continue

                # Apply price filter
                if not (screening_config['min_price'] <= stock_data['price'] <= screening_config['max_price']):
                    continue

                # Apply daily change filter
                if abs(stock_data['daily_change']) < screening_config['min_daily_change']:
                    continue

                # Apply volume filter
                if stock_data['volume'] < screening_config['min_volume']:
                    continue

                # Fetch multi-day data for momentum
                aggregates = self.fetch_recent_aggregates(ticker, days=5)
                api_calls += 1
                momentum = self.analyze_momentum(aggregates) if aggregates else {'trend': 'neutral', 'strength': 0}

                # Fetch and analyze news
                news_items = self.fetch_news(ticker, screening_config['news_lookback_hours'])
                api_calls += 1
                has_catalyst, catalysts = self.analyze_catalysts(news_items)

                # CLEVER OPTIMIZATION: If no news, skip (saves processing)
                if not news_items:
                    self.logger.debug(f"Skipping {ticker} - no recent news")
                    continue

                # Check sector match
                sector_match = self.check_sector_match(ticker, news_items)

                # Calculate score
                score = self.calculate_score(stock_data, has_catalyst, sector_match, momentum)

                # Only include if has catalyst OR very strong momentum
                if has_catalyst or (momentum['trend'] == 'bullish' and momentum['strength'] > 10):
                    candidates.append({
                        'ticker': ticker,
                        'price': stock_data['price'],
                        'daily_change': stock_data['daily_change'],
                        'volume': stock_data['volume'],
                        'catalysts': catalysts,
                        'sector_match': sector_match,
                        'score': score,
                        'news_count': len(news_items),
                        'momentum': momentum
                    })

                    self.logger.info(f"✓ {ticker}: ${stock_data['price']:.2f} ({stock_data['daily_change']:+.1f}%) - Score: {score:.1f} [{momentum['trend']}]")

            except Exception as e:
                self.logger.error(f"Error screening {ticker}: {e}")
                continue

            # Rate limiting: Free tier = 5 calls/min = 12 sec between calls
            # We make 3 calls per ticker = 36 seconds per ticker minimum
            # Add buffer for safety: 40 seconds per ticker
            time.sleep(40)

        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:screening_config['max_notifications']]

        self.logger.info(f"API calls made: {api_calls}")
        self.logger.info(f"Found {len(candidates)} candidates, notifying top {len(top_candidates)}")
        return top_candidates

    def send_email_notification(self, candidates: List[Dict]):
        if not candidates:
            self.logger.info("No candidates to notify")
            return

        email_config = self.config.get('email', {})
        if not email_config.get('enabled', True):
            self.logger.info("Email notifications disabled")
            return

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚀 Stock Alert: {len(candidates)} High-Potential Stocks Found (Free Tier Mode)"
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']

            body = self._create_email_body(candidates)
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            self.logger.info(f"Email notification sent to {email_config['receiver_email']}")

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")

    def _create_email_body(self, candidates: List[Dict]) -> str:
        disclaimer = self.config['risk_management']['disclaimer']
        stop_loss = self.config['risk_management']['stop_loss_percentage']

        body = f"""
🚀 HIGH-POTENTIAL STOCK ALERT 🚀
Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Mode: FREE TIER (Previous Day Data + Fresh News)

{disclaimer}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP OPPORTUNITIES:

"""
        for i, stock in enumerate(candidates, 1):
            momentum_emoji = "📈" if stock['momentum']['trend'] == 'bullish' else "📉" if stock['momentum']['trend'] == 'bearish' else "➡️"

            body += f"""
{i}. {stock['ticker']} - ${stock['price']:.2f}
   {momentum_emoji} Previous Day Change: {stock['daily_change']:+.1f}%
   📊 Volume: {stock['volume']:,.0f} shares
   🎯 Opportunity Score: {stock['score']:.1f}/100
   📰 Recent News: {stock['news_count']} articles
   🔥 Momentum: {stock['momentum']['trend'].upper()} ({stock['momentum']['up_days']}/{stock['momentum']['total_days']} up days)

   CATALYSTS:
"""
            if stock['catalysts']:
                for catalyst in stock['catalysts']:
                    body += f"   • {catalyst}\n"
            else:
                body += f"   • Strong momentum detected\n"

            body += f"""
   🛡️ RISK MANAGEMENT:
   • Suggested Stop-Loss: {stop_loss}%
   • Position Size: Risk only what you can afford to lose

   📱 HOW TO TRADE ON eTORO:
   1. Search for "{stock['ticker']}" in eToro app
   2. Review company info and charts
   3. Set price alert for monitoring
   4. If buying, use stop-loss orders
   5. Consider taking profits at 20-50% gains

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        body += f"""
IMPORTANT REMINDERS:
• Data is from PREVIOUS trading day (free tier limitation)
• News is real-time and fresh
• Penny stocks are extremely volatile
• Past performance doesn't guarantee future results
• Only invest money you can afford to lose completely
• Set stop-losses to protect capital

This is NOT financial advice. Always do your own research.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Stock Screener v1.0 (FREE TIER MODE)
"""
        return body

    def print_console_notification(self, candidates: List[Dict]):
        if not candidates:
            print("\n" + "="*80)
            print("No high-potential candidates found in this cycle")
            print("="*80 + "\n")
            return

        print("\n" + "="*80)
        print(f"🚀 STOCK ALERT: {len(candidates)} HIGH-POTENTIAL OPPORTUNITIES (FREE TIER)")
        print("="*80)
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Note: Price data from previous trading day + fresh news\n")
        print(f"{self.config['risk_management']['disclaimer']}\n")

        for i, stock in enumerate(candidates, 1):
            momentum_indicator = f"[{stock['momentum']['trend'].upper()}]"
            print(f"\n{i}. {stock['ticker']} - ${stock['price']:.2f} {momentum_indicator}")
            print(f"   Prev Day Change: {stock['daily_change']:+.1f}%")
            print(f"   Volume: {stock['volume']:,.0f}")
            print(f"   Score: {stock['score']:.1f}/100")
            print(f"   Momentum: {stock['momentum']['up_days']}/{stock['momentum']['total_days']} up days")
            print(f"   Catalysts:")
            if stock['catalysts']:
                for catalyst in stock['catalysts']:
                    print(f"   • {catalyst}")
            else:
                print(f"   • Strong momentum pattern")

        print("\n" + "="*80 + "\n")

    def run(self):
        scan_interval = self.config['screening']['scan_interval']

        self.logger.info(f"Starting continuous screening (every {scan_interval/3600:.1f} hours)")
        self.logger.info("FREE TIER MODE: Using previous day data + real-time news")

        cycle = 0
        while True:
            try:
                cycle += 1
                self.logger.info(f"Cycle #{cycle} starting...")

                candidates = self.screen_stocks()

                if candidates:
                    self.print_console_notification(candidates)
                    self.send_email_notification(candidates)
                else:
                    self.logger.info("No candidates met criteria this cycle")

                next_scan = datetime.now() + timedelta(seconds=scan_interval)
                self.logger.info(f"Next scan at: {next_scan.strftime('%Y-%m-%d %H:%M:%S')}")
                self.logger.info(f"Sleeping for {scan_interval/3600:.1f} hours...\n")

                time.sleep(scan_interval)

            except KeyboardInterrupt:
                self.logger.info("\n\nShutdown requested by user")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.info("Retrying in 5 minutes...")
                time.sleep(300)


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║         HIGH-POTENTIAL STOCK SCREENER v1.0                ║
║         FREE TIER OPTIMIZED - eToro EU Edition            ║
║         Previous Day Price + Real-Time News               ║
╚═══════════════════════════════════════════════════════════╝
    """)

    config_file = "config.yaml"
    if not os.path.exists(config_file):
        print(f"❌ Error: {config_file} not found!")
        print(f"Please create {config_file} from the template")
        sys.exit(1)

    screener = StockScreenerFree(config_file)
    screener.run()


if __name__ == "__main__":
    main()
