"""
Feature Builder
Applies feature engineering to raw stock data
"""

import pandas as pd
from analysis.features import build_features


class FeatureBuilder:
    """
    Builds features from raw stock data using existing pipeline.
    """
    
    def __init__(self, ml_features=None):
        """
        Initialize feature builder.
        
        Args:
            ml_features (list): List of features to use for ML (None for default)
        """
        self.ml_features = ml_features or [
            'Log_Return',
            'Volatility_10',
            'Volatility_30',
            'Momentum_5',
            'Price_to_MA10',
            'Price_to_MA30',
            'HL_Range'
        ]
    
    def engineer_features(self, df):
        """
        Apply feature engineering to raw data.
        
        Args:
            df (pd.DataFrame): Raw stock data
            
        Returns:
            pd.DataFrame: Data with engineered features
        """
        print(f"\n{'='*80}")
        print("FEATURE ENGINEERING")
        print(f"{'='*80}")
        
        print(f"\nApplying feature engineering pipeline...")
        print(f"Input shape: {df.shape}")
        
        # Process each ticker separately to avoid cross-contamination
        processed_dfs = []
        
        for ticker in df['Ticker'].unique():
            ticker_df = df[df['Ticker'] == ticker].copy()
            
            # Set Date as index for feature engineering
            ticker_df = ticker_df.set_index('Date')
            
            # Apply feature engineering
            ticker_df = build_features(ticker_df)
            
            # Reset index
            ticker_df = ticker_df.reset_index()
            
            processed_dfs.append(ticker_df)
        
        # Combine
        result_df = pd.concat(processed_dfs, ignore_index=True)
        
        # Drop NaN values created by rolling windows
        rows_before = len(result_df)
        result_df = result_df.dropna()
        rows_after = len(result_df)
        
        print(f"✓ Features engineered successfully")
        print(f"✓ Output shape: {result_df.shape}")
        print(f"✓ Rows dropped (NaN): {rows_before - rows_after:,}")
        print(f"✓ Final rows: {rows_after:,}")
        print(f"{'='*80}\n")
        
        return result_df
    
    def select_ml_features(self, df):
        """
        Select features for machine learning.
        
        Args:
            df (pd.DataFrame): Dataframe with engineered features
            
        Returns:
            pd.DataFrame: Selected features only
        """
        print(f"\n{'='*80}")
        print("FEATURE SELECTION")
        print(f"{'='*80}")
        
        print(f"\nSelected features ({len(self.ml_features)}):")
        for i, feat in enumerate(self.ml_features, 1):
            print(f"  {i}. {feat}")
        
        # Extract features
        X = df[self.ml_features].copy()
        
        # Remove any remaining NaN
        X = X.dropna()
        
        print(f"\n✓ Feature matrix: {X.shape[0]:,} samples × {X.shape[1]} features")
        print(f"{'='*80}\n")
        
        return X
    
    def get_feature_statistics(self, X):
        """Get statistics of selected features."""
        return {
            'n_samples': len(X),
            'n_features': len(self.ml_features),
            'features': self.ml_features,
            'feature_means': X.mean().to_dict(),
            'feature_stds': X.std().to_dict(),
            'missing_values': X.isna().sum().to_dict()
        }
