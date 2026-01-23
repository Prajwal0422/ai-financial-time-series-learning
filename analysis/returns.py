import numpy as np

def calculate_returns(df):
    df = df.copy()
    
    # Simple returns
    df["Simple_Return"] = df["Close"].pct_change()
    
    # Log returns (used in quantitative finance)
    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
    
    # Rolling statistics
    df["Rolling_Mean_Return"] = df["Log_Return"].rolling(window=3).mean()
    df["Rolling_Volatility"] = df["Log_Return"].rolling(window=3).std()
    
    return df
