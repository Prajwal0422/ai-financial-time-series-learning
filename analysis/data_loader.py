import pandas as pd
import os

def load_stock_data(csv_path):
    df = pd.read_csv(csv_path)
    
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Sort by date (important for time-series)
    df = df.sort_values("Date")
    
    # Validate data before returning
    df = validate_stock_data(df)
    
    return df

def validate_stock_data(df):
    """
    Validate stock data for required columns and data quality.
    Real data is messy - professionals validate before analysis.
    """
    required_cols = {"Date", "Open", "High", "Low", "Close", "Volume"}
    missing = required_cols - set(df.columns)
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Check for null values
    if df.isnull().sum().sum() > 0:
        print(f"Warning: Found {df.isnull().sum().sum()} null values. Dropping rows with nulls.")
        df = df.dropna()
    
    # Validate data types
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        raise ValueError("Date column must be datetime type")
    
    # Validate numeric columns
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col} must be numeric")
    
    return df

def get_available_datasets():
    """Get list of available CSV files in data directory"""
    from config import DATA_DIR
    datasets = []
    
    if os.path.exists(DATA_DIR):
        for file in os.listdir(DATA_DIR):
            if file.endswith(".csv"):
                datasets.append(file)
    
    return sorted(datasets)
