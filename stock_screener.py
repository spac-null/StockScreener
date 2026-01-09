#!/usr/bin/env python3
"""
Stock Screener for High-Potential Low-Priced Stocks
Focuses on eToro-available stocks with catalyst-driven momentum
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
import pandas as pd
from polygon import RESTClient
from polygon.rest.models import TickerSnapshot, TickerNews


class StockScreener:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.polygon_client = RESTClient(self.config['api']['polygon_api_key'])
        self.logger.info("Stock Screener initialized successfully")

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
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
        """Setup logging configuration"""
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
        """Get list of eToro-available tickers from config"""
        tickers = self.config.get('etoro_available', [])
        self.logger.info(f"Loaded {len(tickers)} eToro-available tickers")
        return tickers

    def fetch_stock_data(self, ticker: str) -> Optional[Dict]:
        """Fetch current stock data from Polygon"""
        try:
            # Get snapshot for current price and volume
            snapshot = self.polygon_client.get_snapshot_ticker("stocks", ticker)

            if not snapshot or not snapshot.day:
                self.logger.debug(f"No snapshot data for {ticker}")
                return None

            # Get previous day for change calculation
            prev_day = snapshot.prev_day
            current_day = snapshot.day

            if not prev_day or not current_day:
                return None

            current_price = current_day.c if current_day.c else None
            prev_close = prev_day.c if prev_day.c else None
            volume = current_day.v if current_day.v else 0

            if not current_price or not prev_close or prev_close == 0:
                return None

            daily_change = ((current_price - prev_close) / prev_close) * 100

            return {
                'ticker': ticker,
                'price': current_price,
                'prev_close': prev_close,
                'daily_change': daily_change,
                'volume': volume,
                'open': current_day.o,
                'high': current_day.h,
                'low': current_day.l,
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.debug(f"Error fetching data for {ticker}: {e}")
            return None

    def fetch_news(self, ticker: str, hours_back: int = 24) -> List[Dict]:
        """Fetch recent news for a ticker"""
        try:
            published_after = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')

            news_items = []
            for news in self.polygon_client.list_ticker_news(
                ticker=ticker,
                published_utc_gte=published_after,
                limit=10
            ):
                news_items.append({
                    'title': news.title,
                    'description': news.description or '',
                    'published': news.published_utc,
                    'url': news.article_url,
                    'source': news.publisher.name if news.publisher else 'Unknown'
                })

            return news_items

        except Exception as e:
            self.logger.debug(f"Error fetching news for {ticker}: {e}")
            return []

    def analyze_catalysts(self, news_items: List[Dict]) -> tuple[bool, List[str]]:
        """Analyze news for positive catalysts"""
        positive_keywords = [
            'approval', 'approved', 'breakthrough', 'partnership', 'deal', 'contract',
            'expansion', 'growth', 'revenue', 'profit', 'acquisition', 'merger',
            'clinical trial', 'fda', 'patent', 'innovation', 'milestone',
            'beat expectations', 'upgrade', 'bullish', 'positive results',
            'new product', 'launch', 'collaboration', 'investment', 'funding'
        ]

        negative_keywords = [
            'lawsuit', 'investigation', 'fraud', 'bankruptcy', 'decline',
            'loss', 'miss', 'downgrade', 'bearish', 'failed', 'rejected',
            'warning', 'recall', 'investigation'
        ]

        catalysts = []
        positive_score = 0
        negative_score = 0

        for news in news_items:
            text = (news['title'] + ' ' + news['description']).lower()

            for keyword in positive_keywords:
                if keyword in text:
                    positive_score += 1
                    catalysts.append(f"{news['title']}")
                    break

            for keyword in negative_keywords:
                if keyword in text:
                    negative_score += 1

        has_catalyst = positive_score > 0 and positive_score > negative_score
        return has_catalyst, list(set(catalysts[:3]))

    def check_sector_match(self, ticker: str, news_items: List[Dict]) -> bool:
        """Check if stock matches target sectors"""
        target_sectors = [s.lower() for s in self.config['screening']['target_sectors']]

        for news in news_items:
            text = (news['title'] + ' ' + news['description']).lower()
            for sector in target_sectors:
                if sector in text:
                    return True

        return False

    def calculate_score(self, stock_data: Dict, has_catalyst: bool, sector_match: bool) -> float:
        """Calculate opportunity score for ranking"""
        score = 0.0

        # Daily change weight (up to 40 points)
        score += min(stock_data['daily_change'] * 2, 40)

        # Volume weight (up to 20 points)
        vol_millions = stock_data['volume'] / 1_000_000
        score += min(vol_millions * 2, 20)

        # Catalyst weight (30 points)
        if has_catalyst:
            score += 30

        # Sector match weight (10 points)
        if sector_match:
            score += 10

        return score

    def screen_stocks(self) -> List[Dict]:
        """Main screening logic"""
        self.logger.info("=" * 80)
        self.logger.info("Starting stock screening cycle...")

        tickers = self.get_etoro_tickers()
        screening_config = self.config['screening']

        candidates = []

        for ticker in tickers:
            try:
                # Fetch stock data
                stock_data = self.fetch_stock_data(ticker)
                if not stock_data:
                    continue

                # Apply filters
                if not (screening_config['min_price'] <= stock_data['price'] <= screening_config['max_price']):
                    continue

                if stock_data['daily_change'] < screening_config['min_daily_change']:
                    continue

                if stock_data['volume'] < screening_config['min_volume']:
                    continue

                # Fetch and analyze news
                news_items = self.fetch_news(ticker, screening_config['news_lookback_hours'])
                has_catalyst, catalysts = self.analyze_catalysts(news_items)

                if not has_catalyst:
                    continue

                # Check sector match
                sector_match = self.check_sector_match(ticker, news_items)

                # Calculate score
                score = self.calculate_score(stock_data, has_catalyst, sector_match)

                candidates.append({
                    'ticker': ticker,
                    'price': stock_data['price'],
                    'daily_change': stock_data['daily_change'],
                    'volume': stock_data['volume'],
                    'catalysts': catalysts,
                    'sector_match': sector_match,
                    'score': score,
                    'news_count': len(news_items)
                })

                self.logger.info(f"✓ {ticker}: ${stock_data['price']:.2f} (+{stock_data['daily_change']:.1f}%) - Score: {score:.1f}")

            except Exception as e:
                self.logger.error(f"Error screening {ticker}: {e}")
                continue

            # Rate limiting
            time.sleep(0.12)

        # Sort by score and return top N
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top_candidates = candidates[:screening_config['max_notifications']]

        self.logger.info(f"Found {len(candidates)} candidates, notifying top {len(top_candidates)}")
        return top_candidates

    def send_email_notification(self, candidates: List[Dict]):
        """Send email notification for top candidates"""
        if not candidates:
            self.logger.info("No candidates to notify")
            return

        email_config = self.config.get('email', {})
        if not email_config.get('enabled', True):
            self.logger.info("Email notifications disabled")
            return

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚀 Stock Alert: {len(candidates)} High-Potential Stocks Found"
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']

            # Create email body
            body = self._create_email_body(candidates)
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            self.logger.info(f"Email notification sent to {email_config['receiver_email']}")

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")

    def _create_email_body(self, candidates: List[Dict]) -> str:
        """Create formatted email body"""
        disclaimer = self.config['risk_management']['disclaimer']
        stop_loss = self.config['risk_management']['stop_loss_percentage']

        body = f"""
🚀 HIGH-POTENTIAL STOCK ALERT 🚀
Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{disclaimer}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP OPPORTUNITIES:

"""
        for i, stock in enumerate(candidates, 1):
            body += f"""
{i}. {stock['ticker']} - ${stock['price']:.2f}
   📈 Daily Change: +{stock['daily_change']:.1f}%
   📊 Volume: {stock['volume']:,.0f} shares
   🎯 Opportunity Score: {stock['score']:.1f}/100
   📰 Recent News: {stock['news_count']} articles

   CATALYSTS:
"""
            for catalyst in stock['catalysts']:
                body += f"   • {catalyst}\n"

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
• Penny stocks are extremely volatile
• Past performance doesn't guarantee future results
• News catalysts can reverse quickly
• Only invest money you can afford to lose completely
• Set stop-losses to protect capital
• Consider scaling out profits gradually

This is NOT financial advice. Always do your own research.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Stock Screener v1.0
"""
        return body

    def print_console_notification(self, candidates: List[Dict]):
        """Print notification to console"""
        if not candidates:
            print("\n" + "="*80)
            print("No high-potential candidates found in this cycle")
            print("="*80 + "\n")
            return

        print("\n" + "="*80)
        print(f"🚀 STOCK ALERT: {len(candidates)} HIGH-POTENTIAL OPPORTUNITIES")
        print("="*80)
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n{self.config['risk_management']['disclaimer']}\n")

        for i, stock in enumerate(candidates, 1):
            print(f"\n{i}. {stock['ticker']} - ${stock['price']:.2f}")
            print(f"   Daily Change: +{stock['daily_change']:.1f}%")
            print(f"   Volume: {stock['volume']:,.0f}")
            print(f"   Score: {stock['score']:.1f}/100")
            print(f"   Catalysts:")
            for catalyst in stock['catalysts']:
                print(f"   • {catalyst}")

        print("\n" + "="*80 + "\n")

    def run(self):
        """Main loop - run continuously"""
        scan_interval = self.config['screening']['scan_interval']

        self.logger.info(f"Starting continuous screening (every {scan_interval/3600:.1f} hours)")

        cycle = 0
        while True:
            try:
                cycle += 1
                self.logger.info(f"Cycle #{cycle} starting...")

                # Screen stocks
                candidates = self.screen_stocks()

                # Notify if candidates found
                if candidates:
                    self.print_console_notification(candidates)
                    self.send_email_notification(candidates)
                else:
                    self.logger.info("No candidates met criteria this cycle")

                # Wait for next cycle
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
    """Entry point"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         HIGH-POTENTIAL STOCK SCREENER v1.0                ║
║         eToro EU Edition - Low-Priced Catalyst Stocks     ║
╚═══════════════════════════════════════════════════════════╝
    """)

    config_file = "config.yaml"
    if not os.path.exists(config_file):
        print(f"❌ Error: {config_file} not found!")
        print(f"Please create {config_file} from the template")
        sys.exit(1)

    screener = StockScreener(config_file)
    screener.run()


if __name__ == "__main__":
    main()
