#!/usr/bin/env python3
"""
Test script to verify Stock Screener setup
Runs a quick test without waiting for full scan cycle
"""

import os
import sys
import yaml
from polygon import RESTClient

def test_config():
    """Test if config file exists and is valid"""
    print("Testing configuration...")
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✓ config.yaml found and valid")
        return config
    except FileNotFoundError:
        print("✗ config.yaml not found")
        return None
    except yaml.YAMLError as e:
        print(f"✗ Error parsing config.yaml: {e}")
        return None

def test_polygon_api(api_key):
    """Test Polygon API connection"""
    print("\nTesting Polygon API connection...")
    try:
        client = RESTClient(api_key)
        # Test with a simple call
        snapshot = client.get_snapshot_ticker("stocks", "AAPL")
        if snapshot:
            print(f"✓ Polygon API working (Test: AAPL at ${snapshot.day.c if snapshot.day else 'N/A'})")
            return True
        else:
            print("✗ No data returned from Polygon API")
            return False
    except Exception as e:
        print(f"✗ Polygon API error: {e}")
        print("  Check your API key in config.yaml")
        return False

def test_email_config(config):
    """Test email configuration (doesn't send, just validates)"""
    print("\nTesting email configuration...")
    email_config = config.get('email', {})

    if not email_config.get('enabled', False):
        print("⚠ Email notifications disabled in config")
        return True

    required = ['sender_email', 'sender_password', 'receiver_email', 'smtp_server', 'smtp_port']
    missing = [field for field in required if not email_config.get(field)]

    if missing:
        print(f"✗ Missing email fields: {', '.join(missing)}")
        return False

    print("✓ Email configuration looks valid")
    print(f"  Sender: {email_config['sender_email']}")
    print(f"  Receiver: {email_config['receiver_email']}")
    return True

def test_etoro_tickers(config):
    """Test eToro ticker list"""
    print("\nTesting eToro ticker list...")
    tickers = config.get('etoro_available', [])

    if not tickers:
        print("✗ No tickers in etoro_available list")
        return False

    print(f"✓ Found {len(tickers)} eToro-available tickers")
    print(f"  Sample: {', '.join(tickers[:5])}")
    return True

def test_screening_params(config):
    """Test screening parameters"""
    print("\nTesting screening parameters...")
    screening = config.get('screening', {})

    checks = [
        ('min_price', 'Minimum price'),
        ('max_price', 'Maximum price'),
        ('min_daily_change', 'Minimum daily change'),
        ('min_volume', 'Minimum volume'),
        ('scan_interval', 'Scan interval')
    ]

    all_valid = True
    for key, label in checks:
        value = screening.get(key)
        if value is None:
            print(f"✗ Missing: {label}")
            all_valid = False
        else:
            print(f"✓ {label}: {value}")

    return all_valid

def run_quick_scan(config):
    """Run a quick scan on a few tickers"""
    print("\n" + "="*60)
    print("Running quick test scan...")
    print("="*60)

    try:
        from stock_screener import StockScreener

        # Temporarily limit tickers for quick test
        original_tickers = config['etoro_available'][:]
        config['etoro_available'] = original_tickers[:5]  # Test with 5 tickers

        # Save modified config temporarily
        with open('config_test.yaml', 'w') as f:
            yaml.dump(config, f)

        # Run screener
        screener = StockScreener('config_test.yaml')
        candidates = screener.screen_stocks()

        # Cleanup
        os.remove('config_test.yaml')

        print("\n" + "="*60)
        print(f"Test scan complete: Found {len(candidates)} candidates")
        print("="*60)

        if candidates:
            print("\nSample candidate:")
            stock = candidates[0]
            print(f"  Ticker: {stock['ticker']}")
            print(f"  Price: ${stock['price']:.2f}")
            print(f"  Change: +{stock['daily_change']:.1f}%")
            print(f"  Score: {stock['score']:.1f}")

        return True

    except Exception as e:
        print(f"\n✗ Error during test scan: {e}")
        return False

def main():
    """Run all tests"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         STOCK SCREENER SETUP TEST                         ║
╚═══════════════════════════════════════════════════════════╝
    """)

    results = []

    # Test 1: Config file
    config = test_config()
    results.append(('Configuration', config is not None))

    if not config:
        print("\n❌ Setup incomplete. Please create and configure config.yaml")
        sys.exit(1)

    # Test 2: Polygon API
    api_key = config.get('api', {}).get('polygon_api_key', '')
    if 'YOUR_' in api_key or not api_key:
        print("\n⚠ Polygon API key not configured")
        results.append(('Polygon API', False))
    else:
        results.append(('Polygon API', test_polygon_api(api_key)))

    # Test 3: Email config
    results.append(('Email Config', test_email_config(config)))

    # Test 4: eToro tickers
    results.append(('eToro Tickers', test_etoro_tickers(config)))

    # Test 5: Screening params
    results.append(('Screening Params', test_screening_params(config)))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the screener.")

        # Ask if user wants to run quick scan
        try:
            response = input("\nRun a quick test scan? (y/n): ")
            if response.lower() == 'y':
                run_quick_scan(config)
        except KeyboardInterrupt:
            print("\nTest cancelled by user")

        print("\nTo start the full screener:")
        print("  python stock_screener.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
