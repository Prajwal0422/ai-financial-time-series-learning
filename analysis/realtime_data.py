"""
Real-Time Data Module
Fetches live stock data and updates the system
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time


class RealtimeDataFetcher:
    """
    Fetches real-time stock data and integrates with existing pipeline.
    """
    
    def __init__(self, tickers, update_interval=60):
        """
        Initialize real-time data fetcher.
        
        Args:
            tickers (list): List of stock tickers to track
            update_interval (int): Update interval in seconds (default: 60)
        """
        self.tickers = tickers
        self.update_interval = update_interval
        self.last_update = None
        self.cache = {}
    
    def fetch_latest_data(self, ticker, period='1d', interval='1m'):
        """
        Fetch latest intraday data for a ticker.
        
        Args:
            ticker (str): Stock ticker symbol
            period (str): Data period ('1d', '5d', '1mo')
            interval (str): Data interval ('1m', '5m', '15m', '1h')
            
        Returns:
            pd.DataFrame: Latest stock data
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                print(f"⚠ No data available for {ticker}")
                return None
            
            # Reset index to make datetime a column
            df = df.reset_index()
            df = df.rename(columns={'Datetime': 'Date'})
            
            # Select needed columns
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            return df
            
        except Exception as e:
            print(f"❌ Error fetching {ticker}: {str(e)}")
            return None
    
    def fetch_current_price(self, ticker):
        """
        Fetch current price for a ticker.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Current price information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            current_data = {
                'ticker': ticker,
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'timestamp': datetime.now().isoformat()
            }
            
            return current_data
            
        except Exception as e:
            print(f"❌ Error fetching current price for {ticker}: {str(e)}")
            return None
    
    def fetch_all_current_prices(self):
        """
        Fetch current prices for all tracked tickers.
        
        Returns:
            dict: Dictionary of ticker -> price data
        """
        print(f"\nFetching current prices for {len(self.tickers)} stocks...")
        
        results = {}
        for ticker in self.tickers:
            data = self.fetch_current_price(ticker)
            if data:
                results[ticker] = data
                print(f"✓ {ticker}: ${data['price']:.2f} ({data['change_percent']:+.2f}%)")
        
        self.last_update = datetime.now()
        self.cache = results
        
        return results
    
    def get_market_summary(self):
        """
        Get summary of current market conditions.
        
        Returns:
            dict: Market summary statistics
        """
        if not self.cache:
            self.fetch_all_current_prices()
        
        prices = [data['price'] for data in self.cache.values()]
        changes = [data['change_percent'] for data in self.cache.values()]
        
        summary = {
            'total_stocks': len(self.cache),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'avg_change': sum(changes) / len(changes) if changes else 0,
            'gainers': len([c for c in changes if c > 0]),
            'losers': len([c for c in changes if c < 0]),
            'unchanged': len([c for c in changes if c == 0]),
            'last_update': self.last_update.isoformat() if self.last_update else None
        }
        
        return summary
    
    def stream_data(self, duration_minutes=60, callback=None):
        """
        Stream real-time data for specified duration.
        
        Args:
            duration_minutes (int): How long to stream data
            callback (function): Optional callback function to process each update
        """
        print(f"\n🔴 Starting real-time data stream for {duration_minutes} minutes...")
        print(f"Update interval: {self.update_interval} seconds")
        print("=" * 60)
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        update_count = 0
        
        try:
            while datetime.now() < end_time:
                # Fetch current prices
                data = self.fetch_all_current_prices()
                update_count += 1
                
                # Call callback if provided
                if callback:
                    callback(data)
                
                # Display summary
                summary = self.get_market_summary()
                print(f"\nUpdate #{update_count} | {summary['gainers']} ↑ | {summary['losers']} ↓ | Avg: {summary['avg_change']:+.2f}%")
                
                # Wait for next update
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹ Stream stopped by user")
        
        print("=" * 60)
        print(f"Stream complete: {update_count} updates in {(datetime.now() - start_time).seconds / 60:.1f} minutes")
    
    def save_snapshot(self, output_path='data/realtime/snapshot.json'):
        """
        Save current data snapshot to file.
        
        Args:
            output_path (str): Path to save snapshot
        """
        import json
        
        if not self.cache:
            self.fetch_all_current_prices()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'data': self.cache,
            'summary': self.get_market_summary()
        }
        
        with open(output_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        print(f"✓ Snapshot saved to {output_file}")


def get_live_market_data(tickers):
    """
    Quick function to get live market data.
    
    Args:
        tickers (list): List of stock tickers
        
    Returns:
        dict: Current market data
    """
    fetcher = RealtimeDataFetcher(tickers)
    return fetcher.fetch_all_current_prices()


if __name__ == "__main__":
    # Example usage
    DEFAULT_TICKERS = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT']
    
    # Create fetcher
    fetcher = RealtimeDataFetcher(DEFAULT_TICKERS, update_interval=60)
    
    # Fetch current prices
    data = fetcher.fetch_all_current_prices()
    
    # Display summary
    summary = fetcher.get_market_summary()
    print(f"\n📊 Market Summary:")
    print(f"  Average Change: {summary['avg_change']:+.2f}%")
    print(f"  Gainers: {summary['gainers']} | Losers: {summary['losers']}")
    
    # Save snapshot
    fetcher.save_snapshot()
    
    # Optional: Stream for 5 minutes
    # fetcher.stream_data(duration_minutes=5)
