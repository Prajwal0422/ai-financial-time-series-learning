"""
Unit Tests for Feature Engineering Module

Tests ensure that feature engineering produces correct results
and handles edge cases appropriately.
"""

import pytest
import pandas as pd
import numpy as np
from analysis.features import (
    build_features,
    add_moving_averages,
    add_volatility_features,
    get_feature_names,
    get_ml_features
)


@pytest.fixture
def sample_stock_data():
    """Create sample stock data for testing"""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    data = {
        'Date': dates,
        'Open': np.random.uniform(90, 110, 100),
        'High': np.random.uniform(95, 115, 100),
        'Low': np.random.uniform(85, 105, 100),
        'Close': np.random.uniform(90, 110, 100),
        'Volume': np.random.randint(1000000, 10000000, 100)
    }
    df = pd.DataFrame(data)
    
    # Ensure OHLC relationships
    df['High'] = df[['Open', 'High', 'Close']].max(axis=1)
    df['Low'] = df[['Open', 'Low', 'Close']].min(axis=1)
    
    return df


class TestFeatureEngineering:
    """Test suite for feature engineering functions"""
    
    def test_build_features_returns_dataframe(self, sample_stock_data):
        """Test that build_features returns a DataFrame"""
        result = build_features(sample_stock_data)
        assert isinstance(result, pd.DataFrame)
    
    def test_build_features_preserves_original_columns(self, sample_stock_data):
        """Test that original columns are preserved"""
        result = build_features(sample_stock_data)
        original_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        for col in original_cols:
            assert col in result.columns
    
    def test_build_features_creates_expected_features(self, sample_stock_data):
        """Test that all expected features are created"""
        result = build_features(sample_stock_data)
        expected_features = get_feature_names()
        
        for feature in expected_features:
            assert feature in result.columns, f"Missing feature: {feature}"
    
    def test_moving_averages_calculation(self, sample_stock_data):
        """Test moving average calculations are correct"""
        df = sample_stock_data.copy()
        df = add_moving_averages(df)
        
        # MA_10 should be mean of last 10 closes
        expected_ma10 = df['Close'].rolling(window=10).mean()
        pd.testing.assert_series_equal(df['MA_10'], expected_ma10, check_names=False)
    
    def test_volatility_features_are_positive(self, sample_stock_data):
        """Test that volatility features are non-negative"""
        df = build_features(sample_stock_data)
        
        # Volatility (std dev) should always be >= 0
        assert (df['Volatility_10'].dropna() >= 0).all()
        assert (df['Volatility_30'].dropna() >= 0).all()
    
    def test_feature_names_list_is_complete(self):
        """Test that get_feature_names returns all features"""
        feature_names = get_feature_names()
        
        # Should have at least 15 features
        assert len(feature_names) >= 15
        
        # Should include key features
        assert 'Log_Return' in feature_names
        assert 'Volatility_10' in feature_names
        assert 'MA_10' in feature_names
    
    def test_ml_features_subset_of_all_features(self):
        """Test that ML features are a subset of all features"""
        all_features = get_feature_names()
        ml_features = get_ml_features()
        
        for feature in ml_features:
            assert feature in all_features
    
    def test_handles_small_dataset(self):
        """Test that feature engineering handles small datasets"""
        small_df = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=10),
            'Open': [100] * 10,
            'High': [105] * 10,
            'Low': [95] * 10,
            'Close': [100] * 10,
            'Volume': [1000000] * 10
        })
        
        result = build_features(small_df)
        
        # Should not raise error
        assert isinstance(result, pd.DataFrame)
        
        # Should have NaN for features requiring more data
        assert result['MA_50'].isnull().all()


class TestFeatureQuality:
    """Test suite for feature quality and edge cases"""
    
    def test_no_infinite_values(self, sample_stock_data):
        """Test that features don't produce infinite values"""
        df = build_features(sample_stock_data)
        
        for col in df.select_dtypes(include=[np.number]).columns:
            assert not np.isinf(df[col]).any(), f"Infinite values in {col}"
    
    def test_price_to_ma_ratio_reasonable(self, sample_stock_data):
        """Test that price/MA ratios are in reasonable range"""
        df = build_features(sample_stock_data)
        
        # Price/MA ratio should typically be between 0.5 and 2.0
        # (allowing for extreme cases)
        assert (df['Price_to_MA10'].dropna() > 0).all()
        assert (df['Price_to_MA10'].dropna() < 10).all()
    
    def test_volume_ratio_positive(self, sample_stock_data):
        """Test that volume ratio is positive"""
        df = build_features(sample_stock_data)
        
        assert (df['Volume_Ratio'].dropna() > 0).all()


# Run tests with: pytest tests/test_features.py -v
