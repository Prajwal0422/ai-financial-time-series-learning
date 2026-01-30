import pandas as pd
import os
from analysis.schema import enforce_schema
from functools import lru_cache
import time

@lru_cache(maxsize=16)
def load_stock_data_cached(csv_path, mtime):
    """Cached version of data loading with file modification time check"""
    df = pd.read_csv(csv_path)
    
    # Enforce data contract before processing
    df = enforce_schema(df)
    
    # Convert Date column to datetime (optimized)
    df["Date"] = pd.to_datetime(df["Date"], format='mixed', cache=True)
    
    # Sort by date (important for time-series)
    df = df.sort_values("Date")
    
    # Validate data before returning
    df = validate_stock_data(df)
    
    return df

def load_stock_data(csv_path):
    """Load stock data with caching based on file modification time"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    
    # Get file modification time for cache invalidation
    mtime = os.path.getmtime(csv_path)
    
    return load_stock_data_cached(csv_path, mtime)

def validate_stock_data(df):
    """
    Validate stock data for required columns and data quality.
    Real data is messy - professionals validate before analysis.
    Optimized for performance with early returns.
    """
    required_cols = {"Date", "Open", "High", "Low", "Close", "Volume"}
    missing = required_cols - set(df.columns)
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Quick null check with early return
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"Warning: Found {null_count} null values. Dropping rows with nulls.")
        df = df.dropna()
    
    # Validate data types (optimized)
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        raise ValueError("Date column must be datetime type")
    
    # Batch validate numeric columns
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    non_numeric = [col for col in numeric_cols if not pd.api.types.is_numeric_dtype(df[col])]
    
    if non_numeric:
        raise ValueError(f"Columns {non_numeric} must be numeric")
    
    return df

@lru_cache(maxsize=32)
def get_available_datasets():
    """Get list of available CSV files in data directory with caching"""
    from config import DATA_DIR
    datasets = []
    
    if os.path.exists(DATA_DIR):
        for file in os.listdir(DATA_DIR):
            if file.endswith(".csv"):
                datasets.append(file)
    
    return sorted(datasets)
