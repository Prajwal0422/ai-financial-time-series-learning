"""
Real Data Loader
Handles loading and validation of real historical stock data
"""

import pandas as pd
from pathlib import Path


class RealDataLoader:
    """
    Loads and validates real historical stock data from CSV files.
    """
    
    REQUIRED_COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    def __init__(self, data_dir='data/real'):
        self.data_dir = Path(data_dir)
    
    def validate_schema(self, df, filename):
        """
        Validate that dataframe has required OHLCV columns.
        
        Args:
            df (pd.DataFrame): Dataframe to validate
            filename (str): Filename for error messages
            
        Returns:
            bool: True if valid, False otherwise
        """
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        
        if missing_cols:
            print(f"  ❌ {filename}: Missing columns: {missing_cols}")
            return False
        
        # Check for critical missing values
        critical_cols = ['Close', 'Date']
        for col in critical_cols:
            if df[col].isna().any():
                print(f"  ⚠ {filename}: {col} has missing values")
        
        return True
    
    def load_single_stock(self, filepath):
        """
        Load and validate a single stock CSV file.
        
        Args:
            filepath (Path): Path to CSV file
            
        Returns:
            pd.DataFrame or None: Loaded dataframe or None if failed
        """
        try:
            # Load CSV
            df = pd.read_csv(filepath)
            
            # Validate schema
            if not self.validate_schema(df, filepath.name):
                return None
            
            # Parse dates
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Sort by date
            df = df.sort_values('Date').reset_index(drop=True)
            
            # Drop rows with missing critical values
            df = df.dropna(subset=['Close', 'Date'])
            
            # Add ticker column
            ticker = filepath.stem
            df['Ticker'] = ticker
            
            return df
            
        except Exception as e:
            print(f"  ❌ Error loading {filepath.name}: {str(e)}")
            return None
    
    def load_all_stocks(self):
        """
        Load all CSV files from data directory.
        
        Returns:
            pd.DataFrame: Combined dataframe with all stocks
        """
        print(f"\n{'='*80}")
        print("LOADING REAL DATA")
        print(f"{'='*80}")
        
        csv_files = list(self.data_dir.glob("*.csv"))
        
        if not csv_files:
            raise ValueError(f"No CSV files found in {self.data_dir}")
        
        print(f"\nFound {len(csv_files)} CSV files")
        print(f"Loading from: {self.data_dir.absolute()}\n")
        
        loaded_dfs = []
        failed_files = []
        
        for csv_file in csv_files:
            print(f"Loading {csv_file.name}...", end=" ")
            
            df = self.load_single_stock(csv_file)
            
            if df is not None:
                loaded_dfs.append(df)
                print(f"✓ {len(df):,} rows")
            else:
                failed_files.append(csv_file.name)
        
        if not loaded_dfs:
            raise ValueError("No valid data files loaded")
        
        # Combine all stocks
        combined_df = pd.concat(loaded_dfs, ignore_index=True)
        
        print(f"\n{'─'*80}")
        print(f"✓ Successfully loaded: {len(loaded_dfs)}/{len(csv_files)} files")
        if failed_files:
            print(f"✗ Failed to load: {', '.join(failed_files)}")
        print(f"✓ Total rows: {len(combined_df):,}")
        print(f"✓ Date range: {combined_df['Date'].min()} to {combined_df['Date'].max()}")
        print(f"✓ Tickers: {', '.join(sorted(combined_df['Ticker'].unique()))}")
        print(f"{'='*80}\n")
        
        return combined_df
    
    def get_data_summary(self, df):
        """Get summary statistics of loaded data."""
        return {
            'total_rows': len(df),
            'num_tickers': df['Ticker'].nunique(),
            'tickers': sorted(df['Ticker'].unique()),
            'date_range': {
                'start': df['Date'].min().isoformat(),
                'end': df['Date'].max().isoformat()
            },
            'rows_per_ticker': df.groupby('Ticker').size().to_dict()
        }
