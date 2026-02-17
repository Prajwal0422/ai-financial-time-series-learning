"""
Download real stock data from Yahoo Finance
Professional data acquisition script
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuration
TICKERS = ["AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "JPM", "V", "WMT"]
START_DATE = "2010-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = Path("data/raw")

def download_stock_data():
    """Download historical stock data from Yahoo Finance"""
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading stock data from {START_DATE} to {END_DATE}")
    print(f"Tickers: {', '.join(TICKERS)}\n")
    
    success_count = 0
    failed_tickers = []
    
    for ticker in TICKERS:
        try:
            print(f"Downloading {ticker}...", end=" ")
            
            # Download data
            df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
            
            if df.empty:
                print(f"❌ No data")
                failed_tickers.append(ticker)
                continue
            
            # Save to CSV
            output_path = OUTPUT_DIR / f"{ticker}.csv"
            df.to_csv(output_path)
            
            print(f"✓ {len(df)} rows saved")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed_tickers.append(ticker)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Download Complete!")
    print(f"Success: {success_count}/{len(TICKERS)}")
    
    if failed_tickers:
        print(f"Failed: {', '.join(failed_tickers)}")
    
    print(f"Data saved to: {OUTPUT_DIR.absolute()}")
    print(f"{'='*50}")

if __name__ == "__main__":
    download_stock_data()
