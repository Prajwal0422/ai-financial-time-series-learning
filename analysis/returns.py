import numpy as np
import pandas as pd
from config import VOLATILITY_WINDOW, RETURN_WINDOW

def calculate_returns(df):
    """Calculate returns and rolling statistics with optimized operations"""
    df = df.copy()
    
    # Vectorized calculations for better performance
    close_values = df["Close"].values
    
    # Simple returns (vectorized)
    df["Simple_Return"] = pd.Series(close_values).pct_change().values
    
    # Log returns (vectorized, used in quantitative finance)
    df["Log_Return"] = np.log(close_values / np.roll(close_values, 1))
    
    # Rolling statistics (optimized with efficient window operations)
    log_returns = df["Log_Return"]
    df["Rolling_Mean_Return"] = log_returns.rolling(window=RETURN_WINDOW, min_periods=1).mean()
    df["Rolling_Volatility"] = log_returns.rolling(window=VOLATILITY_WINDOW, min_periods=1).std()
    
    # Handle NaN values efficiently
    df = df.fillna(method='bfill').fillna(0)
    
    return df
