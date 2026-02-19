"""
Enhanced Market Data Downloader
Downloads multiple stocks and indices efficiently using yfinance
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime


def download_multiple_tickers_efficient(tickers, start_date, end_date=None, output_dir='data/raw'):
    """
    Download multiple tickers efficiently using yfinance's multi-ticker feature.
    
    Args:
        tickers (list or str): List of tickers or space-separated string
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date (default: today)
        output_dir (str): Directory to save CSV files
        
    Returns:
        dict: Dictionary of ticker -> DataFrame
    """
    # Convert list to space-separated string if needed
    if isinstance(tickers, list):
        ticker_string = " ".join(tickers)
    else:
        ticker_string = tickers
    
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"\nDownloading Market Data (Efficient Multi-Ticker)")
    print(f"Period: {start_date} to {end_date}")
    print(f"Tickers: {ticker_string}")
    print("=" * 60)
    
    try:
        # Download all tickers at once (much faster!)
        df = yf.download(ticker_string, start=start_date, end=end_date, group_by="ticker")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        ticker_list = ticker_string.split()
        
        # Process each ticker
        for ticker in ticker_list:
            try:
                # Extract data for this ticker
                if len(ticker_list) == 1:
                    # Single ticker - data is not grouped
                    ticker_df = df.copy()
                else:
                    # Multiple tickers - data is grouped
                    ticker_df = df[ticker].copy()
                
                # Reset index to make Date a column
                ticker_df = ticker_df.reset_index()
                
                # Rename columns to standard format
                ticker_df = ticker_df.rename(columns={
                    'Date': 'Date',
                    'Open': 'Open',
                    'High': 'High',
                    'Low': 'Low',
                    'Close': 'Close',
                    'Volume': 'Volume',
                    'Adj Close': 'Adj_Close'
                })
                
                # Select needed columns
                columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                if 'Adj_Close' in ticker_df.columns:
                    columns.append('Adj_Close')
                
                ticker_df = ticker_df[columns]
                
                # Remove rows with NaN
                ticker_df = ticker_df.dropna()
                
                if len(ticker_df) == 0:
                    print(f"❌ {ticker}: No data available")
                    continue
                
                # Save to CSV
                # Handle special characters in ticker names (e.g., ^GSPC)
                safe_ticker = ticker.replace('^', '').replace('/', '_')
                csv_path = output_path / f"{safe_ticker}.csv"
                ticker_df.to_csv(csv_path, index=False)
                
                results[ticker] = ticker_df
                
                # Display info
                price_range = f"${ticker_df['Close'].min():.2f} - ${ticker_df['Close'].max():.2f}"
                print(f"✓ {ticker:10} | {len(ticker_df):5} rows | {price_range}")
                
            except Exception as e:
                print(f"❌ {ticker}: Error - {str(e)}")
                continue
        
        print("=" * 60)
        print(f"Download complete: {len(results)}/{len(ticker_list)} successful")
        print(f"Files saved to: {output_path.absolute()}")
        print("=" * 60)
        
        return results
        
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return {}


def download_with_indices(include_indices=True, start_date='2000-01-01', end_date=None):
    """
    Download stocks and market indices.
    
    Args:
        include_indices (bool): Include market indices
        start_date (str): Start date
        end_date (str): End date
        
    Returns:
        dict: Downloaded data
    """
    # Major stocks
    stocks = [
        'AAPL',   # Apple
        'MSFT',   # Microsoft
        'AMZN',   # Amazon
        'GOOGL',  # Google (Alphabet Class A)
        'META',   # Meta (Facebook)
        'TSLA',   # Tesla
        'NVDA',   # NVIDIA
        'JPM',    # JPMorgan Chase
        'V',      # Visa
        'WMT'     # Walmart
    ]
    
    # Market indices
    indices = [
        '^GSPC',  # S&P 500
        '^DJI',   # Dow Jones Industrial Average
        '^IXIC',  # NASDAQ Composite
        '^RUT',   # Russell 2000
        '^VIX'    # CBOE Volatility Index
    ]
    
    # Combine tickers
    if include_indices:
        all_tickers = stocks + indices
        print("\n📊 Downloading Stocks + Market Indices")
    else:
        all_tickers = stocks
        print("\n📈 Downloading Stocks Only")
    
    # Download
    results = download_multiple_tickers_efficient(
        tickers=all_tickers,
        start_date=start_date,
        end_date=end_date
    )
    
    return results


def download_sp500_only(start_date='2000-01-01', end_date=None):
    """
    Download S&P 500 index data only.
    
    Args:
        start_date (str): Start date
        end_date (str): End date
        
    Returns:
        pd.DataFrame: S&P 500 data
    """
    print("\n📊 Downloading S&P 500 Index (^GSPC)")
    
    results = download_multiple_tickers_efficient(
        tickers='^GSPC',
        start_date=start_date,
        end_date=end_date
    )
    
    return results.get('^GSPC')


def compare_download_methods():
    """
    Compare single vs multi-ticker download performance.
    """
    import time
    
    tickers = ['AAPL', 'MSFT', 'AMZN']
    start_date = '2023-01-01'
    
    print("\n⏱️  Performance Comparison")
    print("=" * 60)
    
    # Method 1: Individual downloads
    print("\nMethod 1: Individual Downloads")
    start = time.time()
    for ticker in tickers:
        yf.download(ticker, start=start_date, progress=False)
    time1 = time.time() - start
    print(f"Time: {time1:.2f} seconds")
    
    # Method 2: Multi-ticker download
    print("\nMethod 2: Multi-Ticker Download")
    start = time.time()
    yf.download(" ".join(tickers), start=start_date, group_by="ticker", progress=False)
    time2 = time.time() - start
    print(f"Time: {time2:.2f} seconds")
    
    print("\n" + "=" * 60)
    print(f"Speedup: {time1/time2:.2f}x faster with multi-ticker!")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Download market data from Yahoo Finance')
    parser.add_argument('--mode', choices=['stocks', 'indices', 'all', 'sp500', 'compare'], 
                       default='all', help='Download mode')
    parser.add_argument('--start', default='2000-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default=None, help='End date (YYYY-MM-DD)')
    parser.add_argument('--tickers', nargs='+', help='Custom ticker list')
    
    args = parser.parse_args()
    
    if args.mode == 'compare':
        # Performance comparison
        compare_download_methods()
    
    elif args.mode == 'sp500':
        # S&P 500 only
        df = download_sp500_only(start_date=args.start, end_date=args.end)
        if df is not None:
            print(f"\n✓ S&P 500 data: {len(df)} rows")
            print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
            print(f"  Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    
    elif args.tickers:
        # Custom tickers
        results = download_multiple_tickers_efficient(
            tickers=args.tickers,
            start_date=args.start,
            end_date=args.end
        )
        print(f"\n✓ Downloaded {len(results)} tickers")
    
    elif args.mode == 'stocks':
        # Stocks only
        results = download_with_indices(
            include_indices=False,
            start_date=args.start,
            end_date=args.end
        )
    
    elif args.mode == 'indices':
        # Indices only
        indices = ['^GSPC', '^DJI', '^IXIC', '^RUT', '^VIX']
        results = download_multiple_tickers_efficient(
            tickers=indices,
            start_date=args.start,
            end_date=args.end
        )
    
    else:  # 'all'
        # Stocks + Indices
        results = download_with_indices(
            include_indices=True,
            start_date=args.start,
            end_date=args.end
        )
    
    # Summary
    if 'results' in locals() and results:
        total_rows = sum(len(df) for df in results.values())
        print(f"\n📊 Summary:")
        print(f"  Total tickers: {len(results)}")
        print(f"  Total rows: {total_rows:,}")
        print(f"  Average rows per ticker: {total_rows // len(results):,}")
