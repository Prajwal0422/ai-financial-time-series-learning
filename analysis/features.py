"""
Professional Feature Engineering Module
Transforms raw stock data into ML-ready features

This module centralizes all feature engineering logic following
the principle of separation of concerns. Features are designed
for interpretability and analytical insight, not prediction.
"""

import pandas as pd
import numpy as np
from analysis.returns import calculate_returns


def build_features(df):
    """
    Build comprehensive feature set for time-series analysis.
    
    This is the main entry point for feature engineering. It orchestrates
    all feature creation in a logical sequence, ensuring dependencies
    are respected (e.g., returns before volatility).
    
    Args:
        df (pd.DataFrame): Raw stock data with OHLCV columns
        
    Returns:
        pd.DataFrame: Enhanced dataframe with all engineered features
        
    Features Created:
        - Returns (log and simple)
        - Moving averages (10, 30, 50 day)
        - Volatility measures (10, 30 day rolling std)
        - Momentum indicators (5, 10 day)
        - Relative price positions
        - Volume features
        - Range indicators
        - Trend signals
    """
    df = df.copy()
    
    # Step 1: Calculate returns (foundation for other features)
    df = calculate_returns(df)
    
    # Step 2: Moving averages (trend indicators)
    df = add_moving_averages(df)
    
    # Step 3: Volatility features (risk measures)
    df = add_volatility_features(df)
    
    # Step 4: Momentum features (rate of change)
    df = add_momentum_features(df)
    
    # Step 5: Relative position features (context)
    df = add_relative_features(df)
    
    # Step 6: Volume features (market participation)
    df = add_volume_features(df)
    
    # Step 7: Range features (intraday volatility)
    df = add_range_features(df)
    
    # Step 8: Trend signals (directional indicators)
    df = add_trend_signals(df)
    
    return df


def add_moving_averages(df):
    """
    Calculate moving averages for trend identification.
    
    Moving averages smooth price action and help identify
    structural trends by filtering out short-term noise.
    """
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    return df


def add_volatility_features(df):
    """
    Calculate volatility measures using rolling standard deviation.
    
    Volatility clustering is a key characteristic of financial markets.
    These features capture the magnitude of price fluctuations.
    """
    df['Volatility_10'] = df['Log_Return'].rolling(window=10).std()
    df['Volatility_30'] = df['Log_Return'].rolling(window=30).std()
    return df


def add_momentum_features(df):
    """
    Calculate momentum indicators (rate of price change).
    
    Momentum measures the speed of price movements and can
    indicate the strength of trends.
    """
    df['Momentum_5'] = df['Close'] - df['Close'].shift(5)
    df['Momentum_10'] = df['Close'] - df['Close'].shift(10)
    return df


def add_relative_features(df):
    """
    Calculate price position relative to moving averages.
    
    These features provide context about whether price is
    above or below key trend lines, useful for regime detection.
    """
    df['Price_to_MA10'] = df['Close'] / df['MA_10']
    df['Price_to_MA30'] = df['Close'] / df['MA_30']
    return df


def add_volume_features(df):
    """
    Calculate volume-based features.
    
    Volume provides insight into market participation and
    can confirm or contradict price movements.
    """
    df['Volume_MA_10'] = df['Volume'].rolling(window=10).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_MA_10']
    return df


def add_range_features(df):
    """
    Calculate intraday range features.
    
    High-low range normalized by close price captures
    intraday volatility independent of price level.
    """
    df['HL_Range'] = (df['High'] - df['Low']) / df['Close']
    return df


def add_trend_signals(df):
    """
    Calculate trend signals based on moving average crossovers.
    
    Binary signal indicating bullish (1) or bearish (0) regime
    based on short-term MA relative to long-term MA.
    """
    df['MA_Cross'] = (df['MA_10'] > df['MA_30']).astype(int)
    return df


def get_feature_names():
    """
    Return list of all feature names created by this module.
    
    Useful for feature selection, model training, and documentation.
    
    Returns:
        list: Names of all engineered features
    """
    return [
        'Log_Return',
        'Simple_Return',
        'MA_10',
        'MA_30',
        'MA_50',
        'Volatility_10',
        'Volatility_30',
        'Momentum_5',
        'Momentum_10',
        'Price_to_MA10',
        'Price_to_MA30',
        'Volume_MA_10',
        'Volume_Ratio',
        'HL_Range',
        'MA_Cross'
    ]


def get_ml_features():
    """
    Return list of features suitable for machine learning.
    
    These features are selected for regime clustering based on:
    - Statistical significance
    - Low correlation with each other
    - Interpretability
    - Stability across different market conditions
    
    Returns:
        list: Names of features recommended for ML models
    """
    return [
        'Log_Return',
        'Volatility_10',
        'Volatility_30',
        'Momentum_5',
        'Price_to_MA10',
        'Price_to_MA30',
        'HL_Range'
    ]
