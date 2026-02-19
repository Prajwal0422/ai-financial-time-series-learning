"""
Modular ML Retraining Pipeline for Real Historical Data
Orchestrates all ml/ modules for production-ready model training

This is a near-production ML system with:
- Automatic model versioning
- Experiment tracking
- K selection with metric comparison
- Statistical validation (stationarity tests)
- Data drift monitoring
- Modular architecture with separation of concerns
"""

import time
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import modular ML components
from ml.version_manager import ModelVersionManager
from ml.data_loader_real import RealDataLoader
from ml.feature_builder import FeatureBuilder
from ml.cluster_trainer import ClusterTrainer
from ml.evaluator import ModelEvaluator
from ml.statistics import StatisticalValidator
from ml.drift_monitor import DriftMonitor


# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths
RAW_DATA_DIR = 'data/real'
MODELS_DIR = 'models/real_data'
EXPERIMENTS_LOG = 'experiments_real.csv'

# Features to use for clustering
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
K_RANGE = range(3, 9)
RANDOM_STATE = 42
N_INIT = 20
LARGE_DATASET_THRESHOLD = 100_000

# Drift detection threshold (10%)
DRIFT_THRESHOLD = 0.1


# ============================================================================
# MAIN TRAINING PIPELINE
# ============================================================================

def main():
    """
    Main training pipeline that orchestrates all modules.
    """
    print("\n" + "="*80)
    print("MODULAR ML RETRAINING PIPELINE")
    print("="*80)
    print(f"\nStarting training at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    
    # ========================================================================
    # PHASE 1: Initialize Modules
    # ========================================================================
    
    print("\n" + "="*80)
    print("INITIALIZING MODULES")
    print("="*80)
    
    version_manager = ModelVersionManager(base_dir=MODELS_DIR)
    data_loader = RealDataLoader(data_dir=RAW_DATA_DIR)
    feature_builder = FeatureBuilder(ml_features=ML_FEATURES)
    cluster_trainer = ClusterTrainer(
        k_range=K_RANGE,
        random_state=RANDOM_STATE,
        n_init=N_INIT,
        large_dataset_threshold=LARGE_DATASET_THRESHOLD
    )
    evaluator = ModelEvaluator(experiments_log=EXPERIMENTS_LOG)
    stat_validator = StatisticalValidator()
    drift_monitor = DriftMonitor(threshold=DRIFT_THRESHOLD)
    
    print("\n✓ All modules initialized")
    print(f"  - Version Manager: {MODELS_DIR}")
    print(f"  - Data Loader: {RAW_DATA_DIR}")
    print(f"  - Feature Builder: {len(ML_FEATURES)} features")
    print(f"  - Cluster Trainer: K={list(K_RANGE)}")
    print(f"  - Evaluator: {EXPERIMENTS_LOG}")
    print(f"  - Statistical Validator: ADF tests")
    print(f"  - Drift Monitor: threshold={DRIFT_THRESHOLD*100}%")
    
    # ========================================================================
    # PHASE 2: Load Data
    # ========================================================================
    
    df_raw = data_loader.load_all_stocks()
    data_summary = data_loader.get_data_summary(df_raw)
    
    # ========================================================================
    # PHASE 3: Feature Engineering
    # ========================================================================
    
    df_features = feature_builder.engineer_features(df_raw)
    
    # ========================================================================
    # PHASE 4: Statistical Validation
    # ========================================================================
    
    stationarity_report = stat_validator.test_stationarity(
        df_features,
        output_path=f'{MODELS_DIR}/stationarity_report.csv'
    )
    
    # ========================================================================
    # PHASE 5: Feature Selection
    # ========================================================================
    
    X = feature_builder.select_ml_features(df_features)
    feature_stats = feature_builder.get_feature_statistics(X)
    
    # ========================================================================
    # PHASE 6: Feature Scaling
    # ========================================================================
    
    X_scaled, scaler = cluster_trainer.scale_features(X)
    
    # ========================================================================
    # PHASE 7: Model Training & K Selection
    # ========================================================================
    
    comparison_results = cluster_trainer.compare_k_values(X_scaled)
    
    best_model = comparison_results['best_model']
    best_labels = comparison_results['best_labels']
    best_k = comparison_results['best_k']
    best_metrics = comparison_results['best_metrics']
    k_comparison_df = comparison_results['k_comparison_df']
    model_type = comparison_results['model_type']
    
    # ========================================================================
    # PHASE 8: Cluster Analysis
    # ========================================================================
    
    cluster_summary, cluster_means = cluster_trainer.analyze_clusters(
        X_scaled,
        best_labels,
        ML_FEATURES
    )
    
    # ========================================================================
    # PHASE 9: Data Drift Detection
    # ========================================================================
    
    drift_result = drift_monitor.check_drift(feature_stats, version_manager)
    drift_monitor.save_drift_report(
        drift_result,
        output_path=f'{MODELS_DIR}/drift_report.json'
    )
    
    # ========================================================================
    # PHASE 10: Save Model Version
    # ========================================================================
    
    training_time = time.time() - start_time
    
    training_config = {
        'data_dir': str(RAW_DATA_DIR),
        'dataset_count': data_summary['num_tickers'],
        'total_samples': data_summary['total_rows'],
        'features': ML_FEATURES,
        'k_range': list(K_RANGE),
        'random_state': RANDOM_STATE,
        'n_init': N_INIT,
        'large_dataset_threshold': LARGE_DATASET_THRESHOLD,
        'model_type': model_type,
        'training_time': training_time,
        'data_summary': data_summary,
        'feature_statistics': feature_stats,
        'drift_detection': drift_result
    }
    
    version = version_manager.save_model_version(
        model=best_model,
        scaler=scaler,
        features=ML_FEATURES,
        metrics=best_metrics,
        cluster_summary=cluster_summary,
        cluster_means=cluster_means,
        k_comparison=k_comparison_df,
        training_config=training_config
    )
    
    # ========================================================================
    # PHASE 11: Log Experiment
    # ========================================================================
    
    evaluator.log_experiment(
        version=version,
        dataset_count=data_summary['num_tickers'],
        total_samples=data_summary['total_rows'],
        k_selected=best_k,
        metrics=best_metrics,
        training_time=training_time,
        model_type=model_type
    )
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    print("\n" + "="*80)
    print("TRAINING COMPLETE")
    print("="*80)
    print(f"\n✓ Model Version: {version}")
    print(f"✓ Model Type: {model_type}")
    print(f"✓ Optimal K: {best_k}")
    print(f"✓ Silhouette Score: {best_metrics['silhouette_score']:.4f}")
    print(f"✓ Davies-Bouldin Index: {best_metrics['davies_bouldin_index']:.4f}")
    print(f"✓ Training Time: {training_time:.2f}s")
    print(f"✓ Total Samples: {data_summary['total_rows']:,}")
    print(f"✓ Datasets: {data_summary['num_tickers']}")
    
    if drift_result['has_drift']:
        print(f"\n⚠ Data Drift Detected: {drift_result['num_drifted_features']} features")
    else:
        print(f"\n✓ No Data Drift Detected")
    
    print(f"\n✓ Model saved to: {MODELS_DIR}/v{version}/")
    print(f"✓ Experiment logged to: {EXPERIMENTS_LOG}")
    print(f"\nFinished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
