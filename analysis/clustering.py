"""
Professional Market Regime Clustering Module
Uses trained K-Means model to assign regime labels to trading days
"""

from pathlib import Path
import joblib
import numpy as np
from config import N_CLUSTERS, RANDOM_STATE

# Model paths
MODELS_DIR = Path("models")
MODEL_PATH = MODELS_DIR / "kmeans.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
FEATURES_PATH = MODELS_DIR / "features.pkl"

# Load trained model artifacts (lazy loading)
_model = None
_scaler = None
_feature_columns = None

def load_trained_model():
    """
    Load trained K-Means model, scaler, and feature configuration.
    
    This function implements lazy loading - models are loaded once
    and cached for subsequent calls.
    
    Returns:
        tuple: (model, scaler, feature_columns)
    """
    global _model, _scaler, _feature_columns
    
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Trained model not found at {MODEL_PATH}. "
                f"Please run train_model.py first."
            )
        
        print(f"Loading trained model from {MODELS_DIR}...")
        _model = joblib.load(MODEL_PATH)
        _scaler = joblib.load(SCALER_PATH)
        _feature_columns = joblib.load(FEATURES_PATH)
        print(f"✓ Model loaded with {len(_feature_columns)} features: {', '.join(_feature_columns)}")
    
    return _model, _scaler, _feature_columns

def cluster_market_regimes(df, use_trained_model=True):
    """
    Cluster trading days into market regimes using K-Means clustering.
    
    This function assigns regime labels to each trading day based on
    behavioral patterns in returns, volatility, momentum, and trend features.
    
    Args:
        df (pd.DataFrame): Stock data with engineered features
        use_trained_model (bool): If True, use pre-trained model from models/
                                   If False, train new model on this data
    
    Returns:
        pd.DataFrame: Input dataframe with added 'Regime' column
        
    Features Used (aligned with train_model.py):
        - Log_Return: Direction and magnitude of price movement
        - Volatility_10: Short-term volatility (10-day rolling std)
        - Volatility_30: Long-term volatility (30-day rolling std)
        - Momentum_5: 5-day price momentum
        - Price_to_MA10: Price relative to 10-day moving average
        - Price_to_MA30: Price relative to 30-day moving average
        - HL_Range: Intraday high-low range normalized by close
    
    Regime Interpretation:
        Regimes are discovered patterns, not pre-defined categories.
        Typical patterns include:
        - Low volatility, positive returns (stable growth)
        - High volatility, negative returns (market stress)
        - Low volatility, flat returns (consolidation)
        - High volatility, positive returns (recovery/momentum)
    """
    df = df.copy()
    
    if use_trained_model:
        # Load trained model and use consistent features
        model, scaler, feature_columns = load_trained_model()
        
        # Verify all required features exist
        missing_features = [f for f in feature_columns if f not in df.columns]
        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}. "
                f"Ensure build_features() was called before clustering."
            )
        
        # Extract features in correct order
        features = df[feature_columns].copy()
        
        # Drop rows with NaN (from rolling operations)
        valid_idx = features.dropna().index
        X = features.loc[valid_idx].values
        
        # Check if we have enough data
        if len(X) < 2:
            print("Warning: Not enough valid data for clustering, assigning regime 0")
            df["Regime"] = 0
            return df
        
        # Scale features using trained scaler
        X_scaled = scaler.transform(X)
        
        # Predict regimes using trained model
        labels = model.predict(X_scaled)
        
        # Assign labels back to dataframe
        df["Regime"] = None
        df.loc[valid_idx, "Regime"] = labels
        
        # Fill any remaining NaN with regime 0
        df["Regime"] = df["Regime"].fillna(0).infer_objects(copy=False)
        
    else:
        # Fallback: Train new model on this data (for backward compatibility)
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Use same features as trained model
        feature_columns = [
            'Log_Return',
            'Volatility_10',
            'Volatility_30',
            'Momentum_5',
            'Price_to_MA10',
            'Price_to_MA30',
            'HL_Range'
        ]
        
        # Check which features exist
        available_features = [f for f in feature_columns if f in df.columns]
        
        if not available_features:
            print("Warning: No features available for clustering, assigning regime 0")
            df["Regime"] = 0
            return df
        
        features = df[available_features].dropna()
        
        n_samples = len(features)
        n_clusters = min(N_CLUSTERS, n_samples)
        
        if n_samples < 2:
            print("Warning: Not enough data for clustering, assigning regime 0")
            df["Regime"] = 0
            return df
        
        # Scale and cluster
        scaler = StandardScaler()
        X = scaler.fit_transform(features.values)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
        labels = kmeans.fit_predict(X)
        
        # Assign labels
        df["Regime"] = None
        df.loc[features.index, "Regime"] = labels
        df["Regime"] = df["Regime"].fillna(0).infer_objects(copy=False)
    
    # Sanity check: verify cluster distribution
    print("Regime distribution:")
    print(df["Regime"].value_counts().sort_index())
    
    return df
