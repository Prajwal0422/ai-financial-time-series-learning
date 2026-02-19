"""
Scalable ML Training Pipeline for Real Historical Data
Trains clustering models on large-scale real stock datasets

This pipeline is designed for production-scale data processing:
- Handles 100k+ rows efficiently
- Uses MiniBatchKMeans for large datasets
- Validates data schema
- Compares multiple K values
- Saves versioned models with metadata
- Logs experiments for reproducibility
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

from analysis.features import build_features
from analysis.model_versioning import ModelVersionManager

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths
RAW_DATA_DIR = Path("data/real")
MODELS_DIR = Path("models/real_data")
EXPERIMENTS_LOG = Path("experiments_real.csv")

# Features to use for clustering (carefully selected for interpretability)
ML_FEATURES = [
    'Log_Return',
    'Volatility_10',
    'Volatility_30',
    'Momentum_5',
    'Price_to_MA10',
    'Price_to_MA30',
    'HL_Range'
]

# Model comparison settings
K_RANGE = range(3, 9)  # Test K from 3 to 8
RANDOM_STATE = 42
N_INIT = 20

# Scalability threshold
LARGE_DATASET_THRESHOLD = 100_000  # Use MiniBatchKMeans above this

# Required columns for validation
REQUIRED_COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']


# ============================================================================
# STEP 1: DATA LOADING & VALIDATION
# ============================================================================

def validate_schema(df, filename):
    """
    Validate that dataframe has required OHLCV columns.
    
    Args:
        df (pd.DataFrame): Dataframe to validate
        filename (str): Filename for error messages
        
    Returns:
        bool: True if valid, False otherwise
    """
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    if missing_cols:
        print(f"  ❌ Missing columns: {missing_cols}")
        return False
    
    # Check for critical missing values
    critical_cols = ['Close', 'Date']
    for col in critical_cols:
        if df[col].isna().any():
            print(f"  ⚠ Warning: {col} has missing values")
    
    return True


def load_single_stock(filepath):
    """
    Load and validate a single stock CSV file.
    
    Args:
        filepath (Path): Path to CSV file
        
    Returns:
        pd.DataFrame or None: Loaded dataframe or None if failed
    """
    try:
        # Load CSV
        df = pd.read_csv(filepath)
        
        # Validate schema
        if not validate_schema(df, filepath.name):
            return None
        
        # Parse dates
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort by date
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Drop rows with missing critical values
        df = df.dropna(subset=['Close', 'Date'])
        
        # Add ticker column
        ticker = filepath.stem
        df['Ticker'] = ticker
        
        return df
        
    except Exception as e:
        print(f"  ❌ Error loading {filepath.name}: {str(e)}")
        return None


def load_all_real_data(data_dir=RAW_DATA_DIR):
    """
    Load all CSV files from data/real directory.
    
    Args:
        data_dir (Path): Directory containing CSV files
        
    Returns:
        pd.DataFrame: Combined dataframe with all stocks
    """
    print("\n" + "=" * 80)
    print("STEP 1: LOADING REAL DATA")
    print("=" * 80)
    
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        raise ValueError(f"No CSV files found in {data_dir}")
    
    print(f"\nFound {len(csv_files)} CSV files")
    print(f"Loading from: {data_dir.absolute()}\n")
    
    loaded_dfs = []
    failed_files = []
    
    for csv_file in csv_files:
        print(f"Loading {csv_file.name}...", end=" ")
        
        df = load_single_stock(csv_file)
        
        if df is not None:
            loaded_dfs.append(df)
            print(f"✓ {len(df):,} rows")
        else:
            failed_files.append(csv_file.name)
    
    if not loaded_dfs:
        raise ValueError("No valid data files loaded")
    
    # Combine all stocks
    combined_df = pd.concat(loaded_dfs, ignore_index=True)
    
    print(f"\n{'─' * 80}")
    print(f"✓ Successfully loaded: {len(loaded_dfs)}/{len(csv_files)} files")
    if failed_files:
        print(f"✗ Failed to load: {', '.join(failed_files)}")
    print(f"✓ Total rows: {len(combined_df):,}")
    print(f"✓ Date range: {combined_df['Date'].min()} to {combined_df['Date'].max()}")
    print(f"✓ Tickers: {', '.join(sorted(combined_df['Ticker'].unique()))}")
    print("=" * 80)
    
    return combined_df


# ============================================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================================

def engineer_features(df):
    """
    Apply feature engineering to raw data.
    
    Args:
        df (pd.DataFrame): Raw stock data
        
    Returns:
        pd.DataFrame: Data with engineered features
    """
    print("\n" + "=" * 80)
    print("STEP 2: FEATURE ENGINEERING")
    print("=" * 80)
    
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
    print("=" * 80)
    
    return result_df


# ============================================================================
# STEP 3: FEATURE SELECTION & SCALING
# ============================================================================

def prepare_ml_features(df, feature_columns=ML_FEATURES):
    """
    Select and scale features for machine learning.
    
    Args:
        df (pd.DataFrame): Dataframe with engineered features
        feature_columns (list): List of feature names to use
        
    Returns:
        tuple: (X_scaled, scaler, feature_names)
    """
    print("\n" + "=" * 80)
    print("STEP 3: FEATURE SELECTION & SCALING")
    print("=" * 80)
    
    print(f"\nSelected features ({len(feature_columns)}):")
    for i, feat in enumerate(feature_columns, 1):
        print(f"  {i}. {feat}")
    
    # Extract features
    X = df[feature_columns].copy()
    
    # Remove any remaining NaN
    X = X.dropna()
    
    print(f"\n✓ Feature matrix: {X.shape[0]:,} samples × {X.shape[1]} features")
    
    # Scale features
    print(f"\nScaling features with StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"✓ Features scaled successfully")
    print(f"✓ Mean: {X_scaled.mean():.6f}")
    print(f"✓ Std: {X_scaled.std():.6f}")
    print("=" * 80)
    
    return X_scaled, scaler, feature_columns


# ============================================================================
# STEP 4: MODEL COMPARISON
# ============================================================================

def compare_cluster_counts(X_scaled, k_range=K_RANGE, use_minibatch=False):
    """
    Compare different values of K and select optimal.
    
    Args:
        X_scaled (np.ndarray): Scaled feature matrix
        k_range (range): Range of K values to test
        use_minibatch (bool): Use MiniBatchKMeans for large datasets
        
    Returns:
        dict: Comparison results
    """
    print("\n" + "=" * 80)
    print("STEP 4: MODEL COMPARISON")
    print("=" * 80)
    
    n_samples = X_scaled.shape[0]
    model_type = "MiniBatchKMeans" if use_minibatch else "KMeans"
    
    print(f"\nComparing K values: {list(k_range)}")
    print(f"Model type: {model_type}")
    print(f"Samples: {n_samples:,}")
    print(f"Random state: {RANDOM_STATE}")
    print(f"\n{'K':>3} | {'Silhouette':>11} | {'Davies-Bouldin':>15} | {'Inertia':>12}")
    print("─" * 50)
    
    results = []
    
    for k in k_range:
        # Choose model based on dataset size
        if use_minibatch:
            model = MiniBatchKMeans(
                n_clusters=k,
                random_state=RANDOM_STATE,
                batch_size=1024,
                n_init=3,
                max_iter=100
            )
        else:
            model = KMeans(
                n_clusters=k,
                random_state=RANDOM_STATE,
                n_init=N_INIT,
                max_iter=300
            )
        
        # Train
        labels = model.fit_predict(X_scaled)
        
        # Evaluate
        silhouette = silhouette_score(X_scaled, labels)
        davies_bouldin = davies_bouldin_score(X_scaled, labels)
        inertia = model.inertia_
        
        results.append({
            'k': k,
            'silhouette': silhouette,
            'davies_bouldin': davies_bouldin,
            'inertia': inertia,
            'model': model,
            'labels': labels
        })
        
        print(f"{k:3d} | {silhouette:11.4f} | {davies_bouldin:15.4f} | {inertia:12.0f}")
    
    print("─" * 50)
    
    # Select best K (highest silhouette score)
    best_result = max(results, key=lambda x: x['silhouette'])
    best_k = best_result['k']
    
    print(f"\n✓ Optimal K: {best_k}")
    print(f"  Silhouette: {best_result['silhouette']:.4f}")
    print(f"  Davies-Bouldin: {best_result['davies_bouldin']:.4f}")
    print("=" * 80)
    
    return {
        'results': results,
        'best_k': best_k,
        'best_model': best_result['model'],
        'best_labels': best_result['labels'],
        'best_metrics': {
            'silhouette_score': best_result['silhouette'],
            'davies_bouldin_index': best_result['davies_bouldin'],
            'inertia': best_result['inertia']
        }
    }


# ============================================================================
# STEP 5: CLUSTER ANALYSIS
# ============================================================================

def analyze_clusters(X_scaled, labels, feature_names, df):
    """
    Analyze cluster characteristics and distribution.
    
    Args:
        X_scaled (np.ndarray): Scaled features
        labels (np.ndarray): Cluster labels
        feature_names (list): Feature names
        df (pd.DataFrame): Original dataframe with Ticker column
        
    Returns:
        pd.DataFrame: Cluster summary
    """
    print("\n" + "=" * 80)
    print("STEP 5: CLUSTER ANALYSIS")
    print("=" * 80)
    
    # Cluster distribution
    unique, counts = np.unique(labels, return_counts=True)
    
    print(f"\nCluster Distribution:")
    print(f"{'Cluster':>8} | {'Count':>10} | {'Percentage':>10}")
    print("─" * 35)
    
    for cluster, count in zip(unique, counts):
        percentage = (count / len(labels)) * 100
        print(f"{cluster:8d} | {count:10,} | {percentage:9.2f}%")
    
    # Compute mean feature values per cluster
    X_df = pd.DataFrame(X_scaled, columns=feature_names)
    X_df['Cluster'] = labels
    
    cluster_means = X_df.groupby('Cluster').mean()
    
    print(f"\nCluster Feature Means (scaled):")
    print(cluster_means.to_string())
    
    # Save cluster summary
    summary_df = pd.DataFrame({
        'Cluster': unique,
        'Count': counts,
        'Percentage': (counts / len(labels)) * 100
    })
    
    print("=" * 80)
    
    return summary_df, cluster_means


# ============================================================================
# STEP 6: SAVE MODELS & ARTIFACTS
# ============================================================================

def save_model_artifacts(model, scaler, feature_names, metrics, comparison_results, 
                        cluster_summary, cluster_means, total_samples, dataset_count):
    """
    Save all model artifacts with versioning.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        feature_names (list): Feature names
        metrics (dict): Performance metrics
        comparison_results (dict): K comparison results
        cluster_summary (pd.DataFrame): Cluster distribution
        cluster_means (pd.DataFrame): Cluster feature means
        total_samples (int): Total number of samples
        dataset_count (int): Number of datasets
        
    Returns:
        str: Version tag
    """
    print("\n" + "=" * 80)
    print("STEP 6: SAVING MODEL ARTIFACTS")
    print("=" * 80)
    
    # Create models directory
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate version tag
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_tag = f"real_v_{timestamp}"
    
    version_dir = MODELS_DIR / version_tag
    version_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving to: {version_dir}")
    
    # Save model
    joblib.dump(model, version_dir / 'model.pkl')
    print(f"✓ Model saved")
    
    # Save scaler
    joblib.dump(scaler, version_dir / 'scaler.pkl')
    print(f"✓ Scaler saved")
    
    # Save feature names
    joblib.dump(feature_names, version_dir / 'features.pkl')
    print(f"✓ Feature names saved")
    
    # Save metrics
    joblib.dump(metrics, version_dir / 'metrics.pkl')
    print(f"✓ Metrics saved")
    
    # Save cluster summary
    cluster_summary.to_csv(version_dir / 'cluster_summary.csv', index=False)
    print(f"✓ Cluster summary saved")
    
    # Save cluster means
    cluster_means.to_csv(version_dir / 'cluster_means.csv')
    print(f"✓ Cluster means saved")
    
    # Save comparison results
    comparison_df = pd.DataFrame([
        {
            'K': r['k'],
            'Silhouette': r['silhouette'],
            'Davies_Bouldin': r['davies_bouldin'],
            'Inertia': r['inertia']
        }
        for r in comparison_results['results']
    ])
    comparison_df.to_csv(version_dir / 'k_comparison.csv', index=False)
    print(f"✓ K comparison saved")
    
    # Save metadata
    metadata = {
        'version': version_tag,
        'timestamp': datetime.now().isoformat(),
        'model_type': type(model).__name__,
        'n_clusters': int(model.n_clusters),
        'n_features': len(feature_names),
        'features': feature_names,
        'total_samples': total_samples,
        'dataset_count': dataset_count,
        'metrics': metrics,
        'random_state': RANDOM_STATE
    }
    
    with open(version_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved")
    
    # Also save as production model (for dashboard compatibility)
    production_dir = Path("models")
    production_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, production_dir / 'kmeans.pkl')
    joblib.dump(scaler, production_dir / 'scaler.pkl')
    joblib.dump(feature_names, production_dir / 'features.pkl')
    joblib.dump(metrics, production_dir / 'metrics.pkl')
    print(f"✓ Production models updated")
    
    print("=" * 80)
    
    return version_tag


# ============================================================================
# STEP 7: EXPERIMENT LOGGING
# ============================================================================

def log_experiment(version_tag, total_samples, k_selected, metrics, dataset_count):
    """
    Log experiment results to CSV.
    
    Args:
        version_tag (str): Version tag
        total_samples (int): Total samples
        k_selected (int): Selected K value
        metrics (dict): Performance metrics
        dataset_count (int): Number of datasets
    """
    print("\n" + "=" * 80)
    print("STEP 7: LOGGING EXPERIMENT")
    print("=" * 80)
    
    experiment_data = {
        'timestamp': datetime.now().isoformat(),
        'version': version_tag,
        'total_samples': total_samples,
        'dataset_count': dataset_count,
        'K_selected': k_selected,
        'silhouette': metrics['silhouette_score'],
        'davies_bouldin': metrics['davies_bouldin_index'],
        'inertia': metrics.get('inertia', 0)
    }
    
    # Append to CSV
    df = pd.DataFrame([experiment_data])
    
    if EXPERIMENTS_LOG.exists():
        df.to_csv(EXPERIMENTS_LOG, mode='a', header=False, index=False)
    else:
        df.to_csv(EXPERIMENTS_LOG, index=False)
    
    print(f"\n✓ Experiment logged to: {EXPERIMENTS_LOG}")
    print(f"  Version: {version_tag}")
    print(f"  Samples: {total_samples:,}")
    print(f"  K: {k_selected}")
    print(f"  Silhouette: {metrics['silhouette_score']:.4f}")
    print("=" * 80)


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    """
    Main training pipeline orchestrator.
    """
    print("\n" + "=" * 80)
    print("SCALABLE ML TRAINING PIPELINE FOR REAL DATA")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # STEP 1: Load data
    df = load_all_real_data()
    total_samples_raw = len(df)
    dataset_count = df['Ticker'].nunique()
    
    # STEP 2: Engineer features
    df = engineer_features(df)
    
    # STEP 3: Prepare ML features
    X_scaled, scaler, feature_names = prepare_ml_features(df)
    total_samples = X_scaled.shape[0]
    
    # Determine if we need MiniBatchKMeans
    use_minibatch = total_samples > LARGE_DATASET_THRESHOLD
    
    if use_minibatch:
        print(f"\n⚡ Large dataset detected ({total_samples:,} samples)")
        print(f"   Using MiniBatchKMeans for efficiency")
    
    # STEP 4: Compare cluster counts
    comparison_results = compare_cluster_counts(X_scaled, use_minibatch=use_minibatch)
    
    best_model = comparison_results['best_model']
    best_labels = comparison_results['best_labels']
    best_metrics = comparison_results['best_metrics']
    best_k = comparison_results['best_k']
    
    # STEP 5: Analyze clusters
    cluster_summary, cluster_means = analyze_clusters(
        X_scaled, best_labels, feature_names, df
    )
    
    # STEP 6: Save artifacts
    version_tag = save_model_artifacts(
        model=best_model,
        scaler=scaler,
        feature_names=feature_names,
        metrics=best_metrics,
        comparison_results=comparison_results,
        cluster_summary=cluster_summary,
        cluster_means=cluster_means,
        total_samples=total_samples,
        dataset_count=dataset_count
    )
    
    # STEP 7: Log experiment
    log_experiment(version_tag, total_samples, best_k, best_metrics, dataset_count)
    
    # Final summary
    print("\n" + "=" * 80)
    print("TRAINING COMPLETE!")
    print("=" * 80)
    print(f"✓ Version: {version_tag}")
    print(f"✓ Datasets: {dataset_count}")
    print(f"✓ Samples: {total_samples:,}")
    print(f"✓ Features: {len(feature_names)}")
    print(f"✓ Optimal K: {best_k}")
    print(f"✓ Silhouette: {best_metrics['silhouette_score']:.4f}")
    print(f"✓ Davies-Bouldin: {best_metrics['davies_bouldin_index']:.4f}")
    print(f"\nModels saved to: {MODELS_DIR.absolute()}")
    print(f"Experiments log: {EXPERIMENTS_LOG.absolute()}")
    print("=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
