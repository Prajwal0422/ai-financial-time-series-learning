"""
Unit tests for clustering module
Tests feature alignment between training and inference
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.clustering import cluster_market_regimes, load_trained_model
from analysis.features import build_features
from analysis.data_loader import load_stock_data


class TestClustering:
    """Test suite for market regime clustering"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample stock data for testing"""
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        data = {
            'Date': dates,
            'Open': np.random.uniform(90, 110, 100),
            'High': np.random.uniform(95, 115, 100),
            'Low': np.random.uniform(85, 105, 100),
            'Close': np.random.uniform(90, 110, 100),
            'Volume': np.random.randint(1000000, 5000000, 100)
        }
        df = pd.DataFrame(data)
        df = df.set_index('Date')
        return df
    
    @pytest.fixture
    def featured_data(self, sample_data):
        """Create sample data with features"""
        return build_features(sample_data)
    
    def test_load_trained_model(self):
        """Test that trained model can be loaded"""
        models_dir = Path("models")
        
        if not (models_dir / "kmeans.pkl").exists():
            pytest.skip("Trained model not found. Run train_model.py first.")
        
        model, scaler, feature_columns = load_trained_model()
        
        assert model is not None, "Model should be loaded"
        assert scaler is not None, "Scaler should be loaded"
        assert feature_columns is not None, "Feature columns should be loaded"
        assert len(feature_columns) == 7, "Should have 7 features"
        
        expected_features = [
            'Log_Return',
            'Volatility_10',
            'Volatility_30',
            'Momentum_5',
            'Price_to_MA10',
            'Price_to_MA30',
            'HL_Range'
        ]
        
        assert feature_columns == expected_features, f"Features mismatch. Expected {expected_features}, got {feature_columns}"
    
    def test_cluster_with_trained_model(self, featured_data):
        """Test clustering with trained model"""
        models_dir = Path("models")
        
        if not (models_dir / "kmeans.pkl").exists():
            pytest.skip("Trained model not found. Run train_model.py first.")
        
        df_clustered = cluster_market_regimes(featured_data, use_trained_model=True)
        
        assert 'Regime' in df_clustered.columns, "Regime column should be added"
        assert df_clustered['Regime'].notna().any(), "Should have some regime labels"
        assert df_clustered['Regime'].dtype in [np.int64, np.float64], "Regime should be numeric"
    
    def test_cluster_without_trained_model(self, featured_data):
        """Test clustering without trained model (fallback mode)"""
        df_clustered = cluster_market_regimes(featured_data, use_trained_model=False)
        
        assert 'Regime' in df_clustered.columns, "Regime column should be added"
        assert df_clustered['Regime'].notna().any(), "Should have some regime labels"
    
    def test_cluster_with_missing_features(self, sample_data):
        """Test clustering with missing features raises appropriate error"""
        models_dir = Path("models")
        
        if not (models_dir / "kmeans.pkl").exists():
            pytest.skip("Trained model not found. Run train_model.py first.")
        
        # Data without features should raise ValueError
        with pytest.raises(ValueError, match="Missing required features"):
            cluster_market_regimes(sample_data, use_trained_model=True)
    
    def test_cluster_with_insufficient_data(self):
        """Test clustering with insufficient data"""
        # Create minimal dataset
        dates = pd.date_range(start='2020-01-01', periods=2, freq='D')
        data = {
            'Date': dates,
            'Open': [100, 101],
            'High': [105, 106],
            'Low': [95, 96],
            'Close': [100, 101],
            'Volume': [1000000, 1000000]
        }
        df = pd.DataFrame(data).set_index('Date')
        df = build_features(df)
        
        # Should handle gracefully
        df_clustered = cluster_market_regimes(df, use_trained_model=False)
        assert 'Regime' in df_clustered.columns
    
    def test_feature_alignment_with_training(self):
        """Test that inference uses same features as training"""
        models_dir = Path("models")
        
        if not (models_dir / "kmeans.pkl").exists():
            pytest.skip("Trained model not found. Run train_model.py first.")
        
        # Load training features
        import joblib
        training_features = joblib.load(models_dir / "features.pkl")
        
        # Load model features
        _, _, inference_features = load_trained_model()
        
        assert training_features == inference_features, \
            f"Feature mismatch! Training: {training_features}, Inference: {inference_features}"
    
    def test_regime_distribution(self, featured_data):
        """Test that regime distribution is reasonable"""
        models_dir = Path("models")
        
        if not (models_dir / "kmeans.pkl").exists():
            pytest.skip("Trained model not found. Run train_model.py first.")
        
        df_clustered = cluster_market_regimes(featured_data, use_trained_model=True)
        
        regime_counts = df_clustered['Regime'].value_counts()
        
        # Should have at least 1 regime
        assert len(regime_counts) >= 1, "Should have at least one regime"
        
        # No regime should be completely empty
        assert all(regime_counts > 0), "All regimes should have some samples"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
