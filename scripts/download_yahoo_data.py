"""
Yahoo Finance Data Downloader
Downloads real stock data from Yahoo Finance using yfinance library
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


def download_stock_data(ticker, start_date, end_date, output_dir='data/raw'):
    """
    Download stock data from Yahoo Finance.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        output_dir (str): Directory to save CSV file
        
    Returns:
        pd.DataFrame: Downloaded stock data
    """
    try:
        print(f"Downloading {ticker}...", end=" ")
        
        # Download data
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            print(f"❌ No data available")
            return None
        
        # Reset index to make Date a column
        df = df.reset_index()
        
        # Rename columns to match our format
        df = df.rename(columns={
            'Date': 'Date',
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low',
            'Close': 'Close',
            'Volume': 'Volume'
        })
        
        # Select only needed columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Save to CSV
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        csv_path = output_path / f"{ticker}.csv"
        df.to_csv(csv_path, index=False)
        
        print(f"✓ {len(df)} rows | Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def download_multiple_stocks(tickers, start_date=None, end_date=None, output_dir='data/raw'):
    """
    Download data for multiple stocks.
    
    Args:
        tickers (list): List of ticker symbols
        start_date (str): Start date (default: 10 years ago)
        end_date (str): End date (default: today)
        output_dir (str): Directory to save CSV files
        
    Returns:
        dict: Dictionary of ticker -> DataFrame
    """
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
    
    print(f"\nDownloading Yahoo Finance Data")
    print(f"Period: {start_date} to {end_date}")
    print(f"Tickers: {', '.join(tickers)}")
    print("=" * 60)
    
    results = {}
    successful = 0
    failed = 0
    
    for ticker in tickers:
        df = download_stock_data(ticker, start_date, end_date, output_dir)
        if df is not None:
            results[ticker] = df
            successful += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Download complete: {successful} successful, {failed} failed")
    print(f"Files saved to: {Path(output_dir).absolute()}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    # Default tickers - major US stocks
    DEFAULT_TICKERS = [
        'AAPL',   # Apple
        'MSFT',   # Microsoft
        'AMZN',   # Amazon
        'GOOG',   # Google
        'META',   # Meta (Facebook)
        'TSLA',   # Tesla
        'NVDA',   # NVIDIA
        'JPM',    # JPMorgan Chase
        'V',      # Visa
        'WMT'     # Walmart
    ]
    
    # Download data
    results = download_multiple_stocks(
        tickers=DEFAULT_TICKERS,
        start_date='2014-01-01',  # 10 years of data
        end_date=None  # Today
    )
    
    # Print summary
    if results:
        total_rows = sum(len(df) for df in results.values())
        print(f"\nTotal rows downloaded: {total_rows:,}")
        print(f"Average rows per stock: {total_rows // len(results):,}")
