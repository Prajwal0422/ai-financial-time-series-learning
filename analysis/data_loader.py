import pandas as pd
import os

def load_stock_data(csv_path):
    df = pd.read_csv(csv_path)
    
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Sort by date (important for time-series)
    df = df.sort_values("Date")
    
    return df

def get_available_datasets():
    """Get list of available CSV files in data directory"""
    data_dir = "data"
    datasets = []
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith(".csv"):
                datasets.append(file)
    
    return sorted(datasets)
