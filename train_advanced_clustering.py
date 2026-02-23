"""
Advanced Clustering Training Pipeline
Scientific improvements for better cluster quality

Phases:
1. Advanced feature engineering
2. Outlier handling
3. PCA denoising
4. Algorithm comparison
5. K optimization
6. Interpretability analysis
7. Save artifacts
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

# Import modules
from analysis.features import build_features
from analysis.advanced_features import add_advanced_features, get_advanced_ml_features
from analysis.outlier_handling import filter_outliers
from analysis.pca_denoising import apply_pca_denoising
from analysis.algorithm_comparison import compare_algorithms

# Paths
RAW_DATA_DIR = Path("data/real")
MODELS_DIR = Path("models/real_data")
EXPERIMENTS_LOG = Path("experiments_advanced.csv")

# Configuration
RANDOM_STATE = 42
K_RANGE = range(2, 9)
REQUIRED_COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']



# ============================================================================
# DATA LOADING
# ============================================================================

def load_single_stock(filepath):
    """Load and validate a single stock CSV file."""
    try:
        df = pd.read_csv(filepath)
        
        # Validate schema
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            print(f"  ❌ Missing columns: {missing_cols}")
            return None
        
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        df = df.dropna(subset=['Close', 'Date'])
        df['Ticker'] = filepath.stem
        
        return df
    except Exception as e:
        print(f"  ❌ Error loading {filepath.name}: {str(e)}")
        return None


def load_all_data():
    """Load all CSV files from data/real directory."""
    print("\n" + "=" * 80)
    print("PHASE 1: DATA LOADING")
    print("=" * 80)
    
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))
    if not csv_files:
        raise ValueError(f"No CSV files found in {RAW_DATA_DIR}")
    
    print(f"\nFound {len(csv_files)} CSV files")
    
    loaded_dfs = []
    for csv_file in csv_files:
        print(f"Loading {csv_file.name}...", end=" ")
        df = load_single_stock(csv_file)
        if df is not None:
            loaded_dfs.append(df)
            print(f"✓ {len(df):,} rows")
    
    combined_df = pd.concat(loaded_dfs, ignore_index=True)
    
    print(f"\n✓ Total rows: {len(combined_df):,}")
    print(f"✓ Tickers: {combined_df['Ticker'].nunique()}")
    print("=" * 80)
    
    return combined_df



# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def engineer_all_features(df):
    """Apply basic + advanced feature engineering."""
    print("\n" + "=" * 80)
    print("PHASE 2: ADVANCED FEATURE ENGINEERING")
    print("=" * 80)
    
    print(f"\nProcessing {df['Ticker'].nunique()} tickers...")
    
    processed_dfs = []
    for ticker in df['Ticker'].unique():
        ticker_df = df[df['Ticker'] == ticker].copy()
        ticker_df = ticker_df.set_index('Date')
        
        # Basic features
        ticker_df = build_features(ticker_df)
        
        # Advanced features
        ticker_df = add_advanced_features(ticker_df)
        
        ticker_df = ticker_df.reset_index()
        processed_dfs.append(ticker_df)
    
    result_df = pd.concat(processed_dfs, ignore_index=True)
    result_df = result_df.dropna()
    
    print(f"✓ Features engineered: {len(get_advanced_ml_features())}")
    print(f"✓ Final rows: {len(result_df):,}")
    print("=" * 80)
    
    return result_df



# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    """Main training pipeline."""
    print("\n" + "=" * 80)
    print("ADVANCED CLUSTERING TRAINING PIPELINE")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Load data
    df = load_all_data()
    
    # Engineer features
    df = engineer_all_features(df)
    
    # Get feature columns
    feature_columns = get_advanced_ml_features()
    X = df[feature_columns].values
    
    print(f"\n✓ Feature matrix: {X.shape[0]:,} samples × {X.shape[1]} features")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"✓ Features scaled")
    
    # PHASE 3: Outlier handling
    print("\n" + "=" * 80)
    print("PHASE 3: OUTLIER HANDLING")
    print("=" * 80)
    
    print("\nRemoving outliers (Z-score > 3.0)...")
    X_no_outliers, keep_mask = filter_outliers(X_scaled, method='zscore', threshold=3.0)
    
    print("\nRemoving extreme percentiles (0.5% and 99.5%)...")
    X_clean, keep_mask2 = filter_outliers(X_no_outliers, method='percentile', lower=0.5, upper=99.5)
    
    print(f"\n✓ Final clean samples: {len(X_clean):,}")
    print("=" * 80)

    
    # PHASE 4: PCA Denoising
    print("\n" + "=" * 80)
    print("PHASE 4: PCA DENOISING")
    print("=" * 80)
    
    X_pca, pca_model, n_components = apply_pca_denoising(X_clean, variance_threshold=0.95)
    print("=" * 80)
    
    # PHASE 5: Algorithm Comparison
    print("\n" + "=" * 80)
    print("PHASE 5: ALGORITHM COMPARISON")
    print("=" * 80)
    
    # Test with K=3 first
    best_algo, all_algos = compare_algorithms(X_pca, n_clusters=3, random_state=RANDOM_STATE)
    print("=" * 80)
    
    # PHASE 6: K Optimization
    print("\n" + "=" * 80)
    print("PHASE 6: K OPTIMIZATION")
    print("=" * 80)
    
    print(f"\nTesting K values: {list(K_RANGE)}")
    print(f"Using best algorithm: {best_algo['algorithm']}")
    print(f"\n{'K':>3} | {'Silhouette':>11} | {'Davies-Bouldin':>15}")
    print("─" * 45)
    
    k_results = []
    for k in K_RANGE:
        best_k_algo, _ = compare_algorithms(X_pca, n_clusters=k, random_state=RANDOM_STATE)
        k_results.append({
            'K': k,
            'Silhouette': best_k_algo['silhouette'],
            'Davies_Bouldin': best_k_algo['davies_bouldin'],
            'Algorithm': best_k_algo['algorithm'],
            'model': best_k_algo['model'],
            'labels': best_k_algo['labels']
        })
        print(f"{k:3d} | {best_k_algo['silhouette']:11.4f} | {best_k_algo['davies_bouldin']:15.4f}")
    
    # Select best K
    best_k_result = max(k_results, key=lambda x: x['Silhouette'])
    best_k = best_k_result['K']
    
    print("─" * 45)
    print(f"\n✓ Optimal K: {best_k}")
    print(f"  Silhouette: {best_k_result['Silhouette']:.4f}")
    print("=" * 80)

    
    # PHASE 7: Save artifacts
    print("\n" + "=" * 80)
    print("PHASE 7: SAVING ARTIFACTS")
    print("=" * 80)
    
    # Create version directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_tag = f"advanced_v{timestamp}"
    version_dir = MODELS_DIR / version_tag
    version_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving to: {version_dir}")
    
    # Save model
    joblib.dump(best_k_result['model'], version_dir / 'model.pkl')
    print(f"✓ Model saved")
    
    # Save scaler
    joblib.dump(scaler, version_dir / 'scaler.pkl')
    print(f"✓ Scaler saved")
    
    # Save PCA
    joblib.dump(pca_model, version_dir / 'pca.pkl')
    print(f"✓ PCA saved")
    
    # Save features
    joblib.dump(feature_columns, version_dir / 'features.pkl')
    print(f"✓ Features saved")
    
    # Save K comparison
    k_comparison_df = pd.DataFrame([{
        'K': r['K'],
        'Silhouette': r['Silhouette'],
        'Davies_Bouldin': r['Davies_Bouldin'],
        'Algorithm': r['Algorithm']
    } for r in k_results])
    k_comparison_df.to_csv(version_dir / 'k_comparison_full.csv', index=False)
    print(f"✓ K comparison saved")
    
    # Save metadata
    metadata = {
        'version': version_tag,
        'timestamp': datetime.now().isoformat(),
        'algorithm': best_k_result['Algorithm'],
        'n_clusters': best_k},
        'n_features': len(feature_columns),
        'features': feature_columns,
        'pca_components': n_components,
        'total_samples': len(X_clean),
        'metrics': {
            'silhouette_score': float(best_k_result['Silhouette']),
            'davies_bouldin_index': float(best_k_result['Davies_Bouldin'])
        }
    }
    
    with open(version_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved")
    
    print("=" * 80)
    print("\nTRAINING COMPLETE!")
    print(f"✓ Version: {version_tag}")
    print(f"✓ Algorithm: {best_k_result['Algorithm']}")
    print(f"✓ Optimal K: {best_k}")
    print(f"✓ Silhouette: {best_k_result['Silhouette']:.4f}")
    print(f"✓ PCA Components: {n_components}")
    print("=" * 80)


if __name__ == "__main__":
    main()
