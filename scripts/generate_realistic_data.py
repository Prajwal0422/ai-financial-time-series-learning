"""
Generate realistic stock data for professional analysis
Creates large datasets with realistic market behavior
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
TICKERS = ["AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "JPM", "V", "WMT"]
START_DATE = "2010-01-01"
NUM_DAYS = 3650  # ~10 years
OUTPUT_DIR = Path("data/raw")

def generate_realistic_stock_data(ticker, start_price, volatility, trend):
    """Generate realistic stock price data with trends and volatility"""
    
    dates = pd.date_range(start=START_DATE, periods=NUM_DAYS, freq='D')
    
    # Generate returns with trend and volatility
    np.random.seed(hash(ticker) % 2**32)
    returns = np.random.normal(trend, volatility, NUM_DAYS)
    
    # Add volatility clustering
    volatility_series = np.abs(returns)
    for i in range(1, len(volatility_series)):
        volatility_series[i] = 0.7 * volatility_series[i-1] + 0.3 * volatility_series[i]
    
    returns = returns * (1 + volatility_series)
    
    # Calculate prices
    prices = start_price * np.exp(np.cumsum(returns))
    
    # Generate OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC
        daily_volatility = volatility * np.random.uniform(0.5, 1.5)
        high = close * (1 + abs(np.random.normal(0, daily_volatility)))
        low = close * (1 - abs(np.random.normal(0, daily_volatility)))
        open_price = np.random.uniform(low, high)
        
        # Ensure OHLC relationships
        high = max(high, open_price, close)
        low = min(low, open_price, close)
        
        # Generate volume (higher volume on volatile days)
        base_volume = np.random.uniform(50000000, 150000000)
        volume = int(base_volume * (1 + abs(returns[i]) * 10))
        
        data.append({
            'Date': date,
            'Open': round(open_price, 2),
            'High': round(high, 2),
            'Low': round(low, 2),
            'Close': round(close, 2),
            'Volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    return df

def main():
    """Generate data for all tickers"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Stock configurations (start_price, volatility, trend)
    stock_configs = {
        "AAPL": (50, 0.015, 0.0008),    # Strong growth
        "MSFT": (30, 0.012, 0.0007),    # Steady growth
        "AMZN": (100, 0.020, 0.0009),   # High volatility growth
        "GOOG": (300, 0.014, 0.0006),   # Moderate growth
        "META": (25, 0.018, 0.0005),    # Volatile growth
        "TSLA": (20, 0.030, 0.0012),    # Very volatile growth
        "NVDA": (15, 0.025, 0.0015),    # Explosive growth
        "JPM": (40, 0.010, 0.0004),     # Stable banking
        "V": (80, 0.011, 0.0006),       # Steady fintech
        "WMT": (50, 0.008, 0.0003),     # Low volatility retail
    }
    
    print(f"Generating realistic stock data")
    print(f"Period: {START_DATE} to present ({NUM_DAYS} days)")
    print(f"Tickers: {len(TICKERS)}\n")
    
    for ticker in TICKERS:
        start_price, volatility, trend = stock_configs[ticker]
        
        print(f"Generating {ticker}...", end=" ")
        df = generate_realistic_stock_data(ticker, start_price, volatility, trend)
        
        output_path = OUTPUT_DIR / f"{ticker}.csv"
        df.to_csv(output_path)
        
        print(f"✓ {len(df)} rows | Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    
    print(f"\n{'='*60}")
    print(f"Data generation complete!")
    print(f"Files saved to: {OUTPUT_DIR.absolute()}")
    print(f"Total rows: {NUM_DAYS * len(TICKERS):,}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
