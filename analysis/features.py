"""
Feature pipeline for time-series analysis.
Professionals think in pipelines, not scripts.
"""
from analysis.returns import calculate_returns

def build_features(df):
    """
    Build all features required for analysis.
    This centralizes feature engineering logic.
    """
    df = calculate_returns(df)
    return df
