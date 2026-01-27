import numpy as np
from config import VOLATILITY_WINDOW, RETURN_WINDOW

def calculate_returns(df):
    df = df.copy()
    
    # Simple returns
    df["Simple_Return"] = df["Close"].pct_change()
    
    # Log returns (used in quantitative finance)
    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
    
    # Rolling statistics (using config values)
    df["Rolling_Mean_Return"] = df["Log_Return"].rolling(window=RETURN_WINDOW).mean()
    df["Rolling_Volatility"] = df["Log_Return"].rolling(window=VOLATILITY_WINDOW).std()
    
    return df
