"""
Advanced Model Training Script
Professional ML pipeline with model selection, stability analysis, and experiment tracking
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Import our advanced modules
from analysis.model_selection import evaluate_k_range, select_optimal_k, plot_model_comparison, save_comparison_results
from analysis.stability import measure_clustering_stability, save_stability_results
from analysis.statistical_validation import run_statistical_validation, save_validation_report
from analysis.experiment_tracker import ExperimentTracker, log_training_experiment
from analysis.model_versioning import ModelVersionManager
from analysis.regime_insights import create_regime_summary_report, save_regime_insights

# Configuration
PROCESSED_DIR = Path("data/processed")
MODELS_DIR = Path("models")
K_RANGE = (3, 9)  # Test K from 3 to 8
N_INIT = 20
RANDOM_STATE = 42

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
    
    return combined_df, len(csv_files)


def prepare_features(df, feature_columns):
    """Extract and clean features for training"""
    print(f"\nPreparing features...")
    print(f"Selected features: {', '.join(feature_columns)}")
    
    X = df[feature_columns].copy()
    X = X.dropna()
    
    print(f"✓ Feature matrix: {X.shape[0]:,} samples × {X.shape[1]} features")
    
    return X


def main():
    """Main advanced training pipeline"""
    
    print("=" * 80)
    print("ADVANCED ML TRAINING PIPELINE")
    print("=" * 80)
    
    # Initialize trackers
    experiment_tracker = ExperimentTracker()
    version_manager = ModelVersionManager()
    
    # Step 1: Load data
    print("\n" + "=" * 80)
    print("STEP 1: DATA LOADING")
    print("=" * 80)
    df, n_stocks = load_all_processed_data()
    
    # Step 2: Statistical Validation
    print("\n" + "=" * 80)
    print("STEP 2: STATISTICAL VALIDATION")
    print("=" * 80)
    validation_report = run_statistical_validation(df)
    save_validation_report(validation_report)
    
    # Step 3: Prepare features
    print("\n" + "=" * 80)
    print("STEP 3: FEATURE PREPARATION")
    print("=" * 80)
    X = prepare_features(df, FEATURE_COLUMNS)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Step 4: Model Selection (compare different K values)
    print("\n" + "=" * 80)
    print("STEP 4: MODEL SELECTION")
    print("=" * 80)
    comparison_results = evaluate_k_range(X_scaled, k_range=K_RANGE, n_init=N_INIT, random_state=RANDOM_STATE)
    
    # Select optimal K
    optimal_k_silhouette = select_optimal_k(comparison_results, method='silhouette')
    optimal_k_db = select_optimal_k(comparison_results, method='davies_bouldin')
    
    # Use silhouette score as primary criterion
    optimal_k = optimal_k_silhouette
    print(f"\n✓ Selected K = {optimal_k} (based on Silhouette Score)")
    
    # Save comparison results
    save_comparison_results(comparison_results, optimal_k)
    plot_model_comparison(comparison_results)
    
    # Step 5: Train final model with optimal K
    print("\n" + "=" * 80)
    print("STEP 5: FINAL MODEL TRAINING")
    print("=" * 80)
    print(f"Training K-Means with K={optimal_k}...")
    
    final_model = KMeans(
        n_clusters=optimal_k,
        n_init=N_INIT,
        random_state=RANDOM_STATE,
        max_iter=300
    )
    labels = final_model.fit_predict(X_scaled)
    
    # Calculate final metrics
    from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
    
    final_metrics = {
        'silhouette_score': float(silhouette_score(X_scaled, labels)),
        'davies_bouldin_index': float(davies_bouldin_score(X_scaled, labels)),
        'calinski_harabasz_score': float(calinski_harabasz_score(X_scaled, labels)),
        'inertia': float(final_model.inertia_),
        'n_clusters': int(optimal_k),
        'n_samples': int(len(X)),
        'n_features': int(len(FEATURE_COLUMNS))
    }
    
    print(f"✓ Model trained successfully")
    print(f"  Silhouette Score: {final_metrics['silhouette_score']:.4f}")
    print(f"  Davies-Bouldin Index: {final_metrics['davies_bouldin_index']:.4f}")
    print(f"  Calinski-Harabasz Score: {final_metrics['calinski_harabasz_score']:.2f}")
    
    # Step 6: Clustering Stability Analysis
    print("\n" + "=" * 80)
    print("STEP 6: STABILITY ANALYSIS")
    print("=" * 80)
    stability_metrics = measure_clustering_stability(X_scaled, n_clusters=optimal_k, n_runs=10)
    save_stability_results(stability_metrics)
    
    # Step 7: Generate Regime Insights
    print("\n" + "=" * 80)
    print("STEP 7: REGIME INSIGHTS")
    print("=" * 80)
    
    # Add regime labels to dataframe
    df_with_regimes = df.copy()
    df_with_regimes = df_with_regimes.loc[X.index]
    df_with_regimes['Regime'] = labels
    
    regime_report = create_regime_summary_report(df_with_regimes)
    save_regime_insights(regime_report)
    
    # Step 8: Save Model with Version
    print("\n" + "=" * 80)
    print("STEP 8: MODEL VERSIONING")
    print("=" * 80)
    
    version_tag = version_manager.save_model(
        model=final_model,
        scaler=scaler,
        features=FEATURE_COLUMNS,
        metrics=final_metrics,
        description=f"Optimal K={optimal_k} selected via model comparison"
    )
    
    # Step 9: Log Experiment
    print("\n" + "=" * 80)
    print("STEP 9: EXPERIMENT TRACKING")
    print("=" * 80)
    
    data_info = {
        'n_samples': len(X),
        'n_stocks': n_stocks,
        'date_range': f"{df.index.min()} to {df.index.max()}"
    }
    
    experiment_id = log_training_experiment(
        tracker=experiment_tracker,
        n_clusters=optimal_k,
        features=FEATURE_COLUMNS,
        metrics=final_metrics,
        data_info=data_info
    )
    
    # Print final summary
    print("\n" + "=" * 80)
    print("TRAINING COMPLETE")
    print("=" * 80)
    print(f"Model Version: {version_tag}")
    print(f"Experiment ID: {experiment_id}")
    print(f"Optimal K: {optimal_k}")
    print(f"Silhouette Score: {final_metrics['silhouette_score']:.4f}")
    print(f"Stability (ARI): {stability_metrics['ari_mean']:.4f} ± {stability_metrics['ari_std']:.4f}")
    print(f"\nArtifacts saved:")
    print(f"  • Model: models/versions/{version_tag}/")
    print(f"  • Comparison: models/model_comparison.json")
    print(f"  • Stability: models/stability_metrics.json")
    print(f"  • Validation: models/validation_report.json")
    print(f"  • Insights: models/regime_insights.json")
    print(f"  • Experiment: experiments/experiment_log.jsonl")
    print("=" * 80)


if __name__ == "__main__":
    main()
