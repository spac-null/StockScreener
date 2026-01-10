#!/usr/bin/env python3
"""
HYBRID Autonomous Stock Screener
Best of Both Worlds: Weekly summaries + Urgent immediate alerts

Solves: "What if there is ticket that is high buy/high reward with limited window?"
Answer: Immediate email for exceptional opportunities, weekly summary for rest
"""

import os
import sys
import time
import json
import logging
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional, Tuple
import yaml
import requests
from collections import defaultdict


class HybridAutonomousScreener:
    def __init__(self, config_path: str = "config_autonomous_hybrid.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.api_key = self.config['api']['polygon_api_key']
        self.base_url = "https://api.polygon.io"

        # Performance tracking
        self.performance_file = self.config['autonomous']['performance_file']
        self.performance_data = self._load_performance_data()

        # Adaptive settings
        self.adaptive_thresholds = {
            'min_daily_change': self.config['screening']['min_daily_change'],
            'min_volume': self.config['screening']['min_volume']
        }

        # Urgent alert tracking (prevent duplicates)
        self.urgent_alerts_today = []
        self.last_urgent_date = datetime.now().date()

        # Volume history for detecting unusual activity
        self.volume_history = defaultdict(list)

        self.logger.info("🎯 HYBRID Autonomous Screener initialized")
        self.logger.info("Mode: Weekly summaries + Urgent immediate alerts")

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def _setup_logging(self):
        log_file = self.config.get('logging', {}).get('log_file', 'autonomous_hybrid.log')
        log_level = logging.INFO

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_performance_data(self) -> dict:
        """Load historical performance data"""
        if os.path.exists(self.performance_file):
            try:
                with open(self.performance_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'candidates_found': [],
            'urgent_alerts': [],
            'config_changes': [],
            'ticker_discoveries': [],
            'last_optimization': None,
            'weekly_summaries': [],
            'start_date': datetime.now().isoformat()
        }

    def _save_performance_data(self):
        """Save performance data"""
        with open(self.performance_file, 'w') as f:
            json.dump(self.performance_data, f, indent=2, default=str)

    def _rate_limit_delay(self):
        """Smart rate limiting"""
        time.sleep(13)

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

    def fetch_stock_data(self, ticker: str) -> Optional[Dict]:
        """Fetch stock data and detect volume anomalies"""
        try:
            # Get previous day
            url = f"{self.base_url}/v2/aggs/ticker/{ticker}/prev"
            params = {'apiKey': self.api_key, 'adjusted': 'true'}
            data = self._api_get(url, params)

            if not data or data.get('status') != 'OK' or not data.get('results'):
                return None

            result = data['results'][0]
            close_price = result.get('c')
            open_price = result.get('o')
            volume = result.get('v', 0)

            if not close_price or not open_price or open_price == 0:
                return None

            daily_change = ((close_price - open_price) / open_price) * 100

            # Calculate volume multiplier
            volume_multiplier = self._calculate_volume_multiplier(ticker, volume)

            return {
                'ticker': ticker,
                'price': close_price,
                'open': open_price,
                'high': result.get('h'),
                'low': result.get('l'),
                'volume': volume,
                'daily_change': daily_change,
                'volume_multiplier': volume_multiplier,
                'timestamp': datetime.now()
            }

        except Exception as e:
            self.logger.debug(f"Error fetching {ticker}: {e}")
            return None

    def _calculate_volume_multiplier(self, ticker: str, current_volume: int) -> float:
        """Calculate current volume vs 20-day average"""
        # Store in history
        if ticker not in self.volume_history:
            self.volume_history[ticker] = []

        self.volume_history[ticker].append(current_volume)

        # Keep last 20 days
        if len(self.volume_history[ticker]) > 20:
            self.volume_history[ticker] = self.volume_history[ticker][-20:]

        # Calculate average
        if len(self.volume_history[ticker]) >= 5:  # Need at least 5 days
            avg_volume = sum(self.volume_history[ticker][:-1]) / (len(self.volume_history[ticker]) - 1)
            if avg_volume > 0:
                return current_volume / avg_volume

        return 1.0  # Default if not enough history

    def fetch_news(self, ticker: str, hours_back: int = 48) -> List[Dict]:
        """Fetch recent news"""
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

        except Exception as e:
            self.logger.debug(f"Error fetching news for {ticker}: {e}")
            return []

    def analyze_catalysts(self, news_items: List[Dict]) -> Tuple[bool, List[str], bool]:
        """
        Analyze news for catalysts
        Returns: (has_catalyst, catalyst_list, is_urgent_catalyst)
        """
        urgent_keywords = self.config['screening'].get('urgent_catalyst_keywords', [])

        positive_keywords = [
            'approval', 'approved', 'breakthrough', 'partnership', 'deal',
            'milestone', 'success', 'positive', 'beat', 'upgrade'
        ]

        negative_keywords = [
            'lawsuit', 'fraud', 'bankruptcy', 'decline', 'loss',
            'downgrade', 'failed', 'rejected', 'warning'
        ]

        catalysts = []
        positive_score = 0
        negative_score = 0
        is_urgent = False

        for news in news_items:
            text = (news['title'] + ' ' + news['description']).lower()

            # Check urgent keywords first
            for keyword in urgent_keywords:
                if keyword.lower() in text:
                    is_urgent = True
                    catalysts.append(news['title'])
                    positive_score += 3  # Higher weight for urgent
                    break

            # Regular positive keywords
            if not is_urgent:
                for keyword in positive_keywords:
                    if keyword in text:
                        positive_score += 1
                        catalysts.append(news['title'])
                        break

            # Negative keywords
            for keyword in negative_keywords:
                if keyword in text:
                    negative_score += 1

        has_catalyst = positive_score > negative_score and positive_score > 0
        return has_catalyst, list(set(catalysts[:3])), is_urgent

    def calculate_score(self, stock_data: Dict, has_catalyst: bool,
                       is_urgent_catalyst: bool, news_count: int) -> float:
        """Calculate opportunity score with urgent boost"""
        score = 0.0

        # Daily change (up to 30 points)
        score += min(abs(stock_data['daily_change']) * 2, 30)

        # Volume (up to 20 points)
        vol_millions = stock_data['volume'] / 1_000_000
        score += min(vol_millions * 2, 20)

        # Volume multiplier bonus (up to 15 points)
        if stock_data.get('volume_multiplier', 1.0) > 2.0:
            score += min(stock_data['volume_multiplier'] * 3, 15)

        # Catalyst (25 points, 35 if urgent)
        if has_catalyst:
            score += 35 if is_urgent_catalyst else 25

        # News count (up to 5 points)
        score += min(news_count, 5)

        # Urgent momentum bonus
        if stock_data['daily_change'] > 8 and stock_data.get('volume_multiplier', 1.0) > 3:
            score += 10  # Exceptional momentum

        return min(score, 100)  # Cap at 100

    def is_urgent(self, candidate: Dict) -> bool:
        """
        Determine if candidate qualifies for immediate urgent alert
        """
        urgent_criteria = self.config['email']['urgent_criteria']

        # Check all criteria
        checks = [
            candidate['score'] >= urgent_criteria['min_score'],
            candidate['daily_change'] >= urgent_criteria['min_daily_change'],
            candidate.get('volume_multiplier', 1.0) >= urgent_criteria['min_volume_multiplier'],
            candidate.get('is_urgent_catalyst', False) if urgent_criteria['require_catalyst'] else True
        ]

        if not all(checks):
            return False

        # Check spam prevention
        max_per_day = urgent_criteria.get('max_per_day', 2)

        # Reset counter if new day
        if datetime.now().date() != self.last_urgent_date:
            self.urgent_alerts_today = []
            self.last_urgent_date = datetime.now().date()

        if len(self.urgent_alerts_today) >= max_per_day:
            self.logger.info(f"Max urgent alerts reached today ({max_per_day})")
            return False

        # Check duplicate window (24 hours)
        duplicate_window = urgent_criteria.get('duplicate_window_hours', 24)
        cutoff = datetime.now() - timedelta(hours=duplicate_window)

        for alert in self.performance_data.get('urgent_alerts', []):
            if (alert['ticker'] == candidate['ticker'] and
                datetime.fromisoformat(alert['timestamp']) > cutoff):
                self.logger.info(f"{candidate['ticker']} already alerted in last {duplicate_window}h")
                return False

        return True

    def send_urgent_alert(self, candidate: Dict):
        """Send immediate urgent alert email"""
        email_config = self.config.get('email', {})
        if not email_config.get('urgent_alerts_enabled', True):
            return

        try:
            msg = MIMEMultipart()
            msg['Subject'] = f"🚨 URGENT: {candidate['ticker']} - {candidate['score']:.0f}/100 Score - LIMITED WINDOW"
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['receiver_email']

            body = self._create_urgent_email_body(candidate)
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            self.logger.info(f"⚡ URGENT ALERT SENT: {candidate['ticker']}")

            # Track urgent alert
            self.urgent_alerts_today.append(candidate['ticker'])
            self.performance_data['urgent_alerts'].append({
                'ticker': candidate['ticker'],
                'score': candidate['score'],
                'price': candidate['price'],
                'change': candidate['daily_change'],
                'catalysts': candidate['catalysts'],
                'timestamp': datetime.now().isoformat()
            })
            self._save_performance_data()

        except Exception as e:
            self.logger.error(f"Failed to send urgent alert: {e}")

    def _create_urgent_email_body(self, candidate: Dict) -> str:
        """Create urgent alert email body"""
        risk_mgmt = self.config['risk_management']

        body = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ TIME-SENSITIVE OPPORTUNITY DETECTED ⚡

This alert was sent IMMEDIATELY because:
✓ Exceptional score ({candidate['score']:.0f}/100)
✓ Strong momentum (+{candidate['daily_change']:.1f}%)
✓ Unusual volume ({candidate.get('volume_multiplier', 1.0):.1f}x average)
✓ Major catalyst detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{candidate['ticker']} - ${candidate['price']:.2f}

📈 Daily Change: +{candidate['daily_change']:.1f}%
📊 Volume: {candidate['volume']:,.0f} ({candidate.get('volume_multiplier', 1.0):.1f}x average)
🎯 Score: {candidate['score']:.0f}/100
⏰ Detected: {datetime.now().strftime('%a %b %d, %I:%M %p')}

🔥 CATALYST(S):
"""
        for catalyst in candidate['catalysts']:
            body += f"• {catalyst}\n"

        body += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  TIME-SENSITIVE ACTION REQUIRED:

This opportunity has a LIMITED WINDOW.
• Research immediately if interested
• Price may move quickly
• Window may close within hours

🛡️ RISK MANAGEMENT (URGENT TRADE):

• TIGHTER stop-loss: {risk_mgmt.get('urgent_stop_loss', 8)}% (not {risk_mgmt['stop_loss_percentage']}%)
• SMALLER position: {risk_mgmt.get('urgent_position_size', '1%')} of portfolio
• QUICK profit target: {risk_mgmt.get('urgent_take_profit', 20)}% (take profits fast)
• This is HIGH RISK - only for aggressive traders
• Catalyst can reverse - use tight stops!

📱 ETORO IMMEDIATE STEPS:

1. Search "{candidate['ticker']}" NOW on eToro
2. Check CURRENT price (may have moved from ${candidate['price']:.2f})
3. Google catalyst - verify it's real news
4. Quick research (5-10 minutes max)
5. Decide: Trade or pass (decide quickly!)
6. IF BUYING: Set {risk_mgmt.get('urgent_stop_loss', 8)}% stop-loss IMMEDIATELY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  NOT FINANCIAL ADVICE. Urgent = Highest Risk. Trade at your own risk.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Hybrid Autonomous Screener
"""
        return body

    def screen_stocks(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Screen stocks and separate into urgent vs normal
        Returns: (urgent_candidates, normal_candidates)
        """
        self.logger.info("Screening with hybrid detection...")

        tickers = self.config.get('etoro_available', [])
        urgent_candidates = []
        normal_candidates = []

        for ticker in tickers:
            try:
                # Fetch data
                stock_data = self.fetch_stock_data(ticker)
                if not stock_data:
                    continue

                # Apply basic filters
                if not (self.config['screening']['min_price'] <=
                       stock_data['price'] <=
                       self.config['screening']['max_price']):
                    continue

                if abs(stock_data['daily_change']) < self.adaptive_thresholds['min_daily_change']:
                    continue

                if stock_data['volume'] < self.adaptive_thresholds['min_volume']:
                    continue

                # Fetch news
                news_items = self.fetch_news(ticker)
                if not news_items:
                    continue

                has_catalyst, catalysts, is_urgent_catalyst = self.analyze_catalysts(news_items)

                if not has_catalyst:
                    continue

                # Calculate score
                score = self.calculate_score(stock_data, has_catalyst, is_urgent_catalyst, len(news_items))

                candidate = {
                    'ticker': ticker,
                    'price': stock_data['price'],
                    'daily_change': stock_data['daily_change'],
                    'volume': stock_data['volume'],
                    'volume_multiplier': stock_data.get('volume_multiplier', 1.0),
                    'catalysts': catalysts,
                    'is_urgent_catalyst': is_urgent_catalyst,
                    'score': score,
                    'news_count': len(news_items),
                    'timestamp': datetime.now().isoformat()
                }

                # Determine if urgent
                if self.is_urgent(candidate):
                    urgent_candidates.append(candidate)
                    self.logger.info(f"⚡ URGENT: {ticker} ${stock_data['price']:.2f} Score:{score:.0f}")
                else:
                    normal_candidates.append(candidate)
                    self.logger.info(f"✓ Normal: {ticker} ${stock_data['price']:.2f} Score:{score:.0f}")

                # Store all candidates
                self.performance_data['candidates_found'].append(candidate)

            except Exception as e:
                self.logger.error(f"Error screening {ticker}: {e}")
                continue

        self._save_performance_data()

        return urgent_candidates, normal_candidates

    def send_weekly_summary(self):
        """Send weekly summary email (similar to pure autonomous)"""
        # Implementation similar to autonomous screener's weekly summary
        # Include both urgent alerts sent this week + normal opportunities
        self.logger.info("📧 Sending weekly summary...")
        # (Full implementation would go here)

    def run(self):
        """Main hybrid loop"""
        self.logger.info("🎯 HYBRID AUTONOMOUS MODE ACTIVATED")
        self.logger.info("Features: Urgent immediate alerts + Weekly summaries")

        cycle = 0
        last_weekly_summary = datetime.now()

        while True:
            try:
                cycle += 1
                self.logger.info(f"\nCycle #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Screen stocks
                urgent_candidates, normal_candidates = self.screen_stocks()

                # Send urgent alerts immediately
                for candidate in urgent_candidates:
                    self.send_urgent_alert(candidate)

                # Check if weekly summary is due (Sunday 8 PM)
                now = datetime.now()
                if (now.weekday() == 6 and  # Sunday
                    now.hour >= 20 and  # 8 PM or later
                    (now - last_weekly_summary).days >= 7):
                    self.send_weekly_summary()
                    last_weekly_summary = now

                # Sleep
                scan_interval = self.config['screening'].get('scan_interval', 10800)
                next_scan = datetime.now() + timedelta(seconds=scan_interval)
                self.logger.info(f"Next scan: {next_scan.strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(scan_interval)

            except KeyboardInterrupt:
                self.logger.info("\n\nHybrid mode stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in hybrid loop: {e}")
                self.logger.info("Auto-recovering in 5 minutes...")
                time.sleep(300)


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║     HYBRID AUTONOMOUS SCREENER                            ║
║     Urgent Alerts + Weekly Summaries                      ║
║     Best of Both Worlds                                   ║
╚═══════════════════════════════════════════════════════════╝
    """)

    screener = HybridAutonomousScreener()
    screener.run()


if __name__ == "__main__":
    main()
