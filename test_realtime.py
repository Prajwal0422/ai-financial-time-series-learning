"""
Quick test script for real-time data features
"""

from analysis.realtime_data import get_live_market_data

# Test with 2 stocks
print("Testing real-time data fetcher...")
print("=" * 60)

tickers = ['AAPL', 'MSFT']
data = get_live_market_data(tickers)

if data:
    print(f"\n✓ Successfully fetched data for {len(data)} stocks\n")
    
    for ticker, info in data.items():
        price = info['price']
        change = info['change_percent']
        symbol = '▲' if change > 0 else '▼' if change < 0 else '●'
        
        print(f"{ticker:6} | ${price:8.2f} | {symbol} {change:+6.2f}%")
    
    print("\n" + "=" * 60)
    print("✓ Real-time data is working!")
else:
    print("❌ No data received")
