"""
Professional Model Training Script
Trains K-Means clustering model with proper evaluation and persistence
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import joblib

# Configuration
PROCESSED_DIR = Path("data/processed")
MODELS_DIR = Path("models")
N_CLUSTERS = 4
RANDOM_STATE = 42
N_INIT = 20

# Features to use for clustering
FEATURE_COLUMNS = [
    'Log_Return',
    'Volatility_10',
    'Volatility_30',
    'Momentum_5',
    'Price_to_MA10',
    'Price_to_MA30',
    'HL_Range'
]

def load_all_processed_data():
    """Load and combine all processed stock data"""
    
    csv_files = list(PROCESSED_DIR.glob("*.csv"))
    
    print(f"Loading {len(csv_files)} processed files...")
    
    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        df['Ticker'] = csv_file.stem
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=False)
    print(f"✓ Loaded {len(combined_df):,} total rows")
    
    return combined_df

def prepare_features(df, feature_columns):
    """Extract and clean features for training"""
    
    print(f"\nPreparing features...")
    print(f"Selected features: {', '.join(feature_columns)}")
    
    # Extract features
    X = df[feature_columns].copy()
    
    # Remove any remaining NaN
    X = X.dropna()
    
    print(f"✓ Feature matrix: {X.shape[0]:,} samples × {X.shape[1]} features")
    
    return X

def train_kmeans(X, n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=N_INIT):
    """Train K-Means clustering model"""
    
    print(f"\nTraining K-Means model...")
    print(f"Clusters: {n_clusters}")
    print(f"Random state: {random_state}")
    print(f"Initializations: {n_init}")
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=n_init,
        max_iter=300
    )
    
    labels = model.fit_predict(X_scaled)
    
    print(f"✓ Model trained successfully")
    
    return model, scaler, labels, X_scaled

def evaluate_model(X_scaled, labels):
    """Evaluate clustering quality"""
    
    print(f"\nEvaluating model...")
    
    # Silhouette Score (higher is better, range: -1 to 1)
    silhouette = silhouette_score(X_scaled, labels)
    
    # Davies-Bouldin Index (lower is better)
    davies_bouldin = davies_bouldin_score(X_scaled, labels)
    
    # Cluster distribution
    unique, counts = np.unique(labels, return_counts=True)
    
    print(f"\n{'='*60}")
    print(f"Model Evaluation Metrics")
    print(f"{'='*60}")
    print(f"Silhouette Score:      {silhouette:.4f}  (higher is better)")
    print(f"Davies-Bouldin Index:  {davies_bouldin:.4f}  (lower is better)")
    print(f"\nCluster Distribution:")
    for cluster, count in zip(unique, counts):
        percentage = (count / len(labels)) * 100
        print(f"  Cluster {cluster}: {count:6,} samples ({percentage:5.2f}%)")
    print(f"{'='*60}")
    
    return {
        'silhouette_score': silhouette,
        'davies_bouldin_index': davies_bouldin,
        'cluster_distribution': dict(zip(unique.tolist(), counts.tolist()))
    }

def save_models(model, scaler, metrics):
    """Save trained model and scaler"""
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving models...")
    
    # Save model
    model_path = MODELS_DIR / "kmeans.pkl"
    joblib.dump(model, model_path)
    print(f"✓ Model saved: {model_path}")
    
    # Save scaler
    scaler_path = MODELS_DIR / "scaler.pkl"
    joblib.dump(scaler, scaler_path)
    print(f"✓ Scaler saved: {scaler_path}")
    
    # Save metrics
    metrics_path = MODELS_DIR / "metrics.pkl"
    joblib.dump(metrics, metrics_path)
    print(f"✓ Metrics saved: {metrics_path}")
    
    # Save feature names
    features_path = MODELS_DIR / "features.pkl"
    joblib.dump(FEATURE_COLUMNS, features_path)
    print(f"✓ Features saved: {features_path}")

def main():
    """Main training pipeline"""
    
    print(f"{'='*60}")
    print(f"Professional K-Means Training Pipeline")
    print(f"{'='*60}\n")
    
    # Load data
    df = load_all_processed_data()
    
    # Prepare features
    X = prepare_features(df, FEATURE_COLUMNS)
    
    # Train model
    model, scaler, labels, X_scaled = train_kmeans(X)
    
    # Evaluate
    metrics = evaluate_model(X_scaled, labels)
    
    # Save
    save_models(model, scaler, metrics)
    
    print(f"\n{'='*60}")
    print(f"Training Complete!")
    print(f"Models saved to: {MODELS_DIR.absolute()}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
