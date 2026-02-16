"""
Professional Feature Engineering Pipeline
Transforms raw stock data into ML-ready features
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_stock_data(path):
    """Load stock data from CSV"""
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df

def build_features(df):
    """
    Build comprehensive feature set for time-series analysis
    
    Features:
    - Returns (log returns)
    - Volatility (rolling std)
    - Moving averages
    - Momentum indicators
    - Volume features
    """
    
    # Returns
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Simple_Return'] = df['Close'].pct_change()
    
    # Moving Averages
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    
    # Volatility
    df['Volatility_10'] = df['Log_Return'].rolling(window=10).std()
    df['Volatility_30'] = df['Log_Return'].rolling(window=30).std()
    
    # Momentum
    df['Momentum_5'] = df['Close'] - df['Close'].shift(5)
    df['Momentum_10'] = df['Close'] - df['Close'].shift(10)
    
    # Price position relative to MA
    df['Price_to_MA10'] = df['Close'] / df['MA_10']
    df['Price_to_MA30'] = df['Close'] / df['MA_30']
    
    # Volume features
    df['Volume_MA_10'] = df['Volume'].rolling(window=10).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_MA_10']
    
    # High-Low range
    df['HL_Range'] = (df['High'] - df['Low']) / df['Close']
    
    # Trend indicator (MA crossover)
    df['MA_Cross'] = (df['MA_10'] > df['MA_30']).astype(int)
    
    return df

def full_pipeline(path, output_dir=None):
    """
    Complete pipeline: load -> engineer features -> clean -> save
    
    Args:
        path: Path to raw CSV file
        output_dir: Optional directory to save processed data
    
    Returns:
        DataFrame with engineered features
    """
    
    # Load data
    df = load_stock_data(path)
    
    # Build features
    df = build_features(df)
    
    # Drop NaN values
    df = df.dropna()
    
    # Save processed data if output directory provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = Path(path).name
        save_path = output_path / filename
        df.to_csv(save_path)
        print(f"Processed data saved to: {save_path}")
    
    return df

def process_all_stocks(raw_dir="data/raw", processed_dir="data/processed"):
    """Process all stocks in raw directory"""
    
    raw_path = Path(raw_dir)
    processed_path = Path(processed_dir)
    processed_path.mkdir(parents=True, exist_ok=True)
    
    csv_files = list(raw_path.glob("*.csv"))
    
    print(f"Processing {len(csv_files)} stock files...")
    print(f"{'='*60}\n")
    
    results = []
    
    for csv_file in csv_files:
        ticker = csv_file.stem
        print(f"Processing {ticker}...", end=" ")
        
        try:
            df = full_pipeline(csv_file, processed_dir)
            
            print(f"✓ {len(df)} rows, {len(df.columns)} features")
            
            results.append({
                'ticker': ticker,
                'rows': len(df),
                'features': len(df.columns),
                'status': 'success'
            })
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                'ticker': ticker,
                'status': 'failed',
                'error': str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Pipeline Complete!")
    print(f"Processed: {len([r for r in results if r['status'] == 'success'])}/{len(results)}")
    print(f"Output directory: {processed_path.absolute()}")
    print(f"{'='*60}")
    
    return results

if __name__ == "__main__":
    # Process all stocks
    results = process_all_stocks()
    
    # Display summary
    print("\nFeature Summary:")
    print("-" * 60)
    for result in results:
        if result['status'] == 'success':
            print(f"{result['ticker']:6} | {result['rows']:5} rows | {result['features']:2} features")
