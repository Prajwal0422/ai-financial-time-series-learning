"""
Advanced Feature Engineering for Improved Clustering Quality
Adds sophisticated features for better regime separation
"""

import pandas as pd
import numpy as np
from scipy import stats


def add_advanced_features(df):
    """
    Add advanced features to improve clustering quality.
    
    New Features:
    1. Volatility Ratio - Relative volatility changes
    2. Rolling Skewness - Distribution asymmetry
    3. Rolling Kurtosis - Tail risk measure
    4. ATR - Average True Range
    5. Z-score of price - Standardized price position
    6. Normalized volume change - Volume momentum
    7. Rolling Sharpe-like ratio - Risk-adjusted returns
    
    Args:
        df (pd.DataFrame): Dataframe with basic features
        
    Returns:
        pd.DataFrame: Enhanced dataframe with advanced features
    """
    df = df.copy()
    
    # 1. Volatility Ratio (short-term vs long-term)
    df['Volatility_Ratio'] = df['Volatility_10'] / (df['Volatility_30'] + 1e-8)
    
    # 2. Rolling Skewness (20-day)
    df['Rolling_Skewness'] = df['Log_Return'].rolling(window=20).apply(
        lambda x: stats.skew(x) if len(x) >= 3 else 0, raw=True
    )
    
    # 3. Rolling Kurtosis (20-day) - tail risk
    df['Rolling_Kurtosis'] = df['Log_Return'].rolling(window=20).apply(
        lambda x: stats.kurtosis(x) if len(x) >= 4 else 0, raw=True
    )
    
    # 4. Average True Range (ATR) - volatility measure
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift(1))
    low_close = np.abs(df['Low'] - df['Close'].shift(1))
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = true_range.rolling(window=14).mean()
    df['ATR_Normalized'] = df['ATR'] / (df['Close'] + 1e-8)
    
    # 5. Z-score of price (standardized price position)
    price_mean = df['Close'].rolling(window=30).mean()
    price_std = df['Close'].rolling(window=30).std()
    df['Price_Zscore'] = (df['Close'] - price_mean) / (price_std + 1e-8)
    
    # 6. Normalized volume change
    volume_change = df['Volume'].pct_change()
    df['Volume_Change_Norm'] = volume_change / (volume_change.rolling(window=20).std() + 1e-8)
    
    # 7. Rolling Sharpe-like ratio (risk-adjusted returns)
    rolling_mean_return = df['Log_Return'].rolling(window=20).mean()
    rolling_std_return = df['Log_Return'].rolling(window=20).std()
    df['Rolling_Sharpe'] = rolling_mean_return / (rolling_std_return + 1e-8)
    
    return df


def get_advanced_ml_features():
    """
    Return list of all features for advanced clustering.
    
    Combines basic + advanced features for maximum separation.
    
    Returns:
        list: Feature names for ML
    """
    return [
        # Basic features (proven)
        'Log_Return',
        'Volatility_10',
        'Volatility_30',
        'Momentum_5',
        'Price_to_MA10',
        'Price_to_MA30',
        'HL_Range',
        # Advanced features (new)
        'Volatility_Ratio',
        'Rolling_Skewness',
        'Rolling_Kurtosis',
        'ATR_Normalized',
        'Price_Zscore',
        'Volume_Change_Norm',
        'Rolling_Sharpe'
    ]
