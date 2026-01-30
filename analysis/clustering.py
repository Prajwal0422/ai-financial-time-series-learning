from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from config import N_CLUSTERS, RANDOM_STATE
import numpy as np

def cluster_market_regimes(df, n_clusters=N_CLUSTERS):
    """
    Cluster trading days into market regimes using unsupervised learning.
    
    We cluster days based on behavior, not price level.
    - Log_Return captures direction & magnitude of movement
    - Rolling_Volatility captures uncertainty / risk
    
    n_clusters chosen for interpretability on small datasets
    (typical regimes: stable, volatile, declining)
    """
    df = df.copy()
    
    # Select features (drop NaNs from rolling ops)
    features = df[["Log_Return", "Rolling_Volatility"]].dropna()
    
    # Check if we have enough data for clustering
    n_samples = len(features)
    if n_samples < n_clusters:
        print(f"Warning: Only {n_samples} samples available, reducing clusters from {n_clusters} to {max(1, n_samples)}")
        n_clusters = max(1, n_samples)
    
    if n_samples < 2:
        print("Warning: Not enough data for clustering, assigning single regime")
        df["Regime"] = 0
        return df
    
    # Feature scaling is essential for KMeans
    # Returns and volatility have different scales
    scaler = StandardScaler()
    X = scaler.fit_transform(features.values)
    
    # KMeans clustering - no labels, no prediction, pure pattern discovery
    kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
    labels = kmeans.fit_predict(X)
    
    # Align labels back to df index
    df["Regime"] = None
    df.loc[features.index, "Regime"] = labels
    
    # Fill any remaining NaN values with regime 0
    df["Regime"] = df["Regime"].fillna(0)
    
    # Sanity check: verify cluster distribution
    print("Regime distribution:")
    print(df["Regime"].value_counts().sort_index())
    
    return df
