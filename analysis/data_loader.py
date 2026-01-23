import pandas as pd

def load_stock_data(csv_path):
    df = pd.read_csv(csv_path)
    
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Sort by date (important for time-series)
    df = df.sort_values("Date")
    
    return df
