"""
System Runtime Audit Tool
Validates all major components of the AI Financial Time-Series Analysis project
Generates comprehensive markdown report
"""

import os
import sys
import json
import time
import warnings
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = Path("data/real")
MODELS_DIR = Path("models/real_data")
EXPERIMENTS_LOG = Path("experiments_real.csv")
REPORT_FILE = Path("PROJECT_RUNTIME_AUDIT.md")

REQUIRED_COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
REQUIRED_FEATURES = [
    'Log_Return',
    'Volatility_10',
    'Volatility_30',
    'Momentum_5',
    'Price_to_MA10',
    'Price_to_MA30',
    'HL_Range'
]

# ============================================================================
# AUDIT RESULTS STORAGE
# ============================================================================

audit_results = {
    'timestamp': datetime.now().isoformat(),
    'data_validation': {},
    'feature_validation': {},
    'model_validation': {},
    'performance_test': {},
    'experiment_log': {},
    'drift_check': {},
    'file_structure': {},
    'warnings': [],
    'errors': [],
    'completion_score': 0
}


# ============================================================================
# STEP 1: DATA VALIDATION
# ============================================================================

def validate_data():
    """Validate data directory and CSV files"""
    print("\n" + "="*80)
    print("STEP 1: DATA VALIDATION")
    print("="*80)
    
    results = {
        'data_dir_exists': False,
        'csv_count': 0,
        'total_rows': 0,
        'valid_files': [],
        'invalid_files': [],
        'date_range': {},
        'tickers': []
    }
    
    try:
        if not DATA_DIR.exists():
            audit_results['errors'].append(f"Data directory not found: {DATA_DIR}")
            print(f"❌ Data directory not found: {DATA_DIR}")
            return results
        
        results['data_dir_exists'] = True
        print(f"✓ Data directory exists: {DATA_DIR}")
        
        csv_files = list(DATA_DIR.glob("*.csv"))
        results['csv_count'] = len(csv_files)
        print(f"✓ Found {len(csv_files)} CSV files")
        
        if len(csv_files) == 0:
            audit_results['warnings'].append("No CSV files found in data directory")
            print("⚠ No CSV files found")
            return results
        
        total_rows = 0
        min_date = None
        max_date = None
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                
                # Validate columns
                missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
                if missing_cols:
                    results['invalid_files'].append({
                        'file': csv_file.name,
                        'reason': f"Missing columns: {missing_cols}"
                    })
                    print(f"  ❌ {csv_file.name}: Missing {missing_cols}")
                    continue
                
                # Parse dates
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Update stats
                total_rows += len(df)
                results['valid_files'].append(csv_file.name)
                results['tickers'].append(csv_file.stem)
                
                if min_date is None or df['Date'].min() < min_date:
                    min_date = df['Date'].min()
                if max_date is None or df['Date'].max() > max_date:
                    max_date = df['Date'].max()
                
                print(f"  ✓ {csv_file.name}: {len(df):,} rows")
                
            except Exception as e:
                results['invalid_files'].append({
                    'file': csv_file.name,
                    'reason': str(e)
                })
                print(f"  ❌ {csv_file.name}: {str(e)}")
        
        results['total_rows'] = total_rows
        if min_date and max_date:
            results['date_range'] = {
                'start': min_date.isoformat(),
                'end': max_date.isoformat()
            }
        
        print(f"\n✓ Total valid files: {len(results['valid_files'])}")
        print(f"✓ Total rows: {total_rows:,}")
        if results['date_range']:
            print(f"✓ Date range: {results['date_range']['start']} to {results['date_range']['end']}")
        
    except Exception as e:
        audit_results['errors'].append(f"Data validation error: {str(e)}")
        print(f"❌ Error: {str(e)}")
    
    audit_results['data_validation'] = results
    return results


# ============================================================================
# STEP 2: FEATURE PIPELINE CHECK
# ============================================================================

def validate_features():
    """Validate feature engineering pipeline"""
    print("\n" + "="*80)
    print("STEP 2: FEATURE PIPELINE CHECK")
    print("="*80)
    
    results = {
        'pipeline_works': False,
        'features_generated': [],
        'missing_features': [],
        'nan_counts': {},
        'sample_file': None
    }
    
    try:
        # Import feature engineering
        from analysis.features import build_features
        
        # Get first valid CSV file
        csv_files = list(DATA_DIR.glob("*.csv"))
        if not csv_files:
            audit_results['warnings'].append("No CSV files to test features")
            print("⚠ No CSV files available")
            return results
        
        sample_file = csv_files[0]
        results['sample_file'] = sample_file.name
        print(f"Testing with: {sample_file.name}")
        
        # Load and process
        df = pd.read_csv(sample_file)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        
        print(f"  Input shape: {df.shape}")
        
        # Apply feature engineering
        df_features = build_features(df)
        
        print(f"  Output shape: {df_features.shape}")
        
        # Check for required features
        for feature in REQUIRED_FEATURES:
            if feature in df_features.columns:
                results['features_generated'].append(feature)
                nan_count = df_features[feature].isna().sum()
                results['nan_counts'][feature] = int(nan_count)
                print(f"  ✓ {feature}: {nan_count} NaN values")
            else:
                results['missing_features'].append(feature)
                print(f"  ❌ {feature}: MISSING")
        
        if len(results['missing_features']) == 0:
            results['pipeline_works'] = True
            print(f"\n✓ All {len(REQUIRED_FEATURES)} required features generated")
        else:
            audit_results['errors'].append(f"Missing features: {results['missing_features']}")
            print(f"\n❌ Missing {len(results['missing_features'])} features")
        
    except Exception as e:
        audit_results['errors'].append(f"Feature validation error: {str(e)}")
        print(f"❌ Error: {str(e)}")
    
    audit_results['feature_validation'] = results
    return results


# ============================================================================
# STEP 3: MODEL CHECK
# ============================================================================

def validate_model():
    """Validate model artifacts"""
    print("\n" + "="*80)
    print("STEP 3: MODEL CHECK")
    print("="*80)
    
    results = {
        'models_dir_exists': False,
        'latest_version': None,
        'model_files': {},
        'model_loaded': False,
        'n_clusters': None,
        'training_timestamp': None,
        'metrics': {}
    }
    
    try:
        if not MODELS_DIR.exists():
            audit_results['warnings'].append(f"Models directory not found: {MODELS_DIR}")
            print(f"⚠ Models directory not found: {MODELS_DIR}")
            return results
        
        results['models_dir_exists'] = True
        print(f"✓ Models directory exists: {MODELS_DIR}")
        
        # Check for versions.json
        versions_file = MODELS_DIR / "versions.json"
        if versions_file.exists():
            with open(versions_file, 'r') as f:
                versions_data = json.load(f)
            
            current_version = versions_data.get('current_version', 0)
            results['latest_version'] = current_version
            print(f"✓ Latest version: v{current_version}")
            
            if current_version > 0:
                version_dir = MODELS_DIR / f"v{current_version}"
                
                # Check for required files
                required_files = ['model.pkl', 'scaler.pkl', 'metrics.json']
                for file in required_files:
                    file_path = version_dir / file
                    results['model_files'][file] = file_path.exists()
                    if file_path.exists():
                        print(f"  ✓ {file}")
                    else:
                        print(f"  ❌ {file} missing")
                        audit_results['warnings'].append(f"Missing {file} in v{current_version}")
                
                # Load metadata
                metadata_file = version_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    results['n_clusters'] = metadata.get('n_clusters')
                    results['training_timestamp'] = metadata.get('timestamp')
                    results['metrics'] = metadata.get('metrics', {})
                    
                    print(f"\n✓ Model metadata loaded")
                    print(f"  Clusters: {results['n_clusters']}")
                    print(f"  Timestamp: {results['training_timestamp']}")
                    if 'silhouette_score' in results['metrics']:
                        print(f"  Silhouette: {results['metrics']['silhouette_score']:.4f}")
                    
                    # Try to load model
                    try:
                        import joblib
                        model_path = version_dir / "model.pkl"
                        model = joblib.load(model_path)
                        results['model_loaded'] = True
                        print(f"✓ Model loaded successfully")
                    except Exception as e:
                        audit_results['warnings'].append(f"Could not load model: {str(e)}")
                        print(f"⚠ Could not load model: {str(e)}")
        else:
            audit_results['warnings'].append("No versions.json found")
            print("⚠ No versions.json found")
        
    except Exception as e:
        audit_results['errors'].append(f"Model validation error: {str(e)}")
        print(f"❌ Error: {str(e)}")
    
    audit_results['model_validation'] = results
    return results


# ============================================================================
# STEP 4: PERFORMANCE TEST
# ============================================================================

def test_performance():
    """Test clustering performance on small sample"""
    print("\n" + "="*80)
    print("STEP 4: PERFORMANCE TEST")
    print("="*80)
    
    results = {
        'test_passed': False,
        'sample_size': 0,
        'predictions_generated': False,
        'runtime_seconds': 0,
        'unique_clusters': 0
    }
    
    try:
        import joblib
        from sklearn.preprocessing import StandardScaler
        
        # Check if model exists
        versions_file = MODELS_DIR / "versions.json"
        if not versions_file.exists():
            print("⚠ No model available for testing")
            return results
        
        with open(versions_file, 'r') as f:
            versions_data = json.load(f)
        
        current_version = versions_data.get('current_version', 0)
        if current_version == 0:
            print("⚠ No trained model version")
            return results
        
        version_dir = MODELS_DIR / f"v{current_version}"
        
        # Load model and scaler
        model = joblib.load(version_dir / "model.pkl")
        scaler = joblib.load(version_dir / "scaler.pkl")
        features = joblib.load(version_dir / "features.pkl")
        
        print(f"✓ Loaded model v{current_version}")
        
        # Get sample data
        csv_files = list(DATA_DIR.glob("*.csv"))
        if not csv_files:
            print("⚠ No data files for testing")
            return results
        
        from analysis.features import build_features
        
        df = pd.read_csv(csv_files[0])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df = build_features(df)
        df = df.dropna()
        
        # Take small sample
        sample_size = min(100, len(df))
        df_sample = df.tail(sample_size)
        results['sample_size'] = sample_size
        
        # Extract features
        X = df_sample[features].values
        
        # Scale and predict
        start_time = time.time()
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)
        runtime = time.time() - start_time
        
        results['runtime_seconds'] = round(runtime, 4)
        results['predictions_generated'] = True
        results['unique_clusters'] = len(np.unique(predictions))
        results['test_passed'] = True
        
        print(f"✓ Performance test passed")
        print(f"  Sample size: {sample_size}")
        print(f"  Runtime: {runtime:.4f}s")
        print(f"  Unique clusters: {results['unique_clusters']}")
        
    except Exception as e:
        audit_results['errors'].append(f"Performance test error: {str(e)}")
        print(f"❌ Error: {str(e)}")
    
    audit_results['performance_test'] = results
    return results


# ============================================================================
# STEP 5: EXPERIMENT LOG CHECK
# ============================================================================

def validate_experiments():
    """Validate experiment tracking"""
    print("\n" + "="*80)
    print("STEP 5: EXPERIMENT LOG CHECK")
    print("="*80)
    
    results = {
        'log_exists': False,
        'experiment_count': 0,
        'last_experiment': {}
    }
    
    try:
        if not EXPERIMENTS_LOG.exists():
            audit_results['warnings'].append(f"Experiment log not found: {EXPERIMENTS_LOG}")
            print(f"⚠ Experiment log not found: {EXPERIMENTS_LOG}")
            return results
        
        results['log_exists'] = True
        print(f"✓ Experiment log exists: {EXPERIMENTS_LOG}")
        
        # Try to read with error handling for malformed CSV
        try:
            df = pd.read_csv(EXPERIMENTS_LOG, on_bad_lines='skip')
        except:
            df = pd.read_csv(EXPERIMENTS_LOG, error_bad_lines=False)
        
        results['experiment_count'] = len(df)
        
        print(f"✓ Total experiments: {len(df)}")
        
        if len(df) > 0:
            last_exp = df.iloc[-1].to_dict()
            results['last_experiment'] = {
                'version': int(last_exp.get('version', 0)),
                'timestamp': str(last_exp.get('timestamp', 'N/A')),
                'K_selected': int(last_exp.get('K_selected', 0)),
                'silhouette_score': float(last_exp.get('silhouette_score', 0)),
                'total_samples': int(last_exp.get('total_samples', 0))
            }
            
            print(f"\nLast experiment:")
            print(f"  Version: v{results['last_experiment']['version']}")
            print(f"  Timestamp: {results['last_experiment']['timestamp']}")
            print(f"  K: {results['last_experiment']['K_selected']}")
            print(f"  Silhouette: {results['last_experiment']['silhouette_score']:.4f}")
            print(f"  Samples: {results['last_experiment']['total_samples']:,}")
        
    except Exception as e:
        audit_results['errors'].append(f"Experiment log error: {str(e)}")
        print(f"❌ Error: {str(e)}")
    
    audit_results['experiment_log'] = results
    return results


# ============================================================================
# STEP 6: DRIFT CHECK
# ============================================================================

def check_drift():
    """Check for data drift"""
    print("\n" + "="*80)
    print("STEP 6: DRIFT CHECK")
    print("="*80)
    
    results = {
        'drift_report_exists': False,
        'has_drift': False,
        'drifted_features': []
    }
    
    try:
        drift_report = MODELS_DIR / "drift_report.json"
        
        if not drift_report.exists():
            print("⚠ No drift report found")
            return results
        
        results['drift_report_exists'] = True
        
        with open(drift_report, 'r') as f:
            drift_data = json.load(f)
        
        results['has_drift'] = drift_data.get('has_drift', False)
        
        if results['has_drift']:
            results['drifted_features'] = [
                f['feature'] for f in drift_data.get('drifted_features', [])
            ]
            print(f"⚠ Data drift detected!")
            print(f"  Drifted features: {', '.join(results['drifted_features'])}")
            audit_results['warnings'].append(f"Data drift detected in {len(results['drifted_features'])} features")
        else:
            print("✓ No data drift detected")
        
    except Exception as e:
        audit_results['warnings'].append(f"Drift check error: {str(e)}")
        print(f"⚠ Error: {str(e)}")
    
    audit_results['drift_check'] = results
    return results


# ============================================================================
# STEP 7: FILE STRUCTURE SNAPSHOT
# ============================================================================

def check_file_structure():
    """Check project file structure"""
    print("\n" + "="*80)
    print("STEP 7: FILE STRUCTURE SNAPSHOT")
    print("="*80)
    
    results = {
        'directories': {},
        'key_files': {}
    }
    
    key_dirs = ['analysis', 'ml', 'models', 'data', 'templates', 'static', 'api', 'tests']
    
    for dir_name in key_dirs:
        dir_path = Path(dir_name)
        exists = dir_path.exists()
        results['directories'][dir_name] = {
            'exists': exists,
            'file_count': len(list(dir_path.glob("*"))) if exists else 0
        }
        
        if exists:
            print(f"✓ {dir_name}/: {results['directories'][dir_name]['file_count']} items")
        else:
            print(f"❌ {dir_name}/: NOT FOUND")
    
    # Check key files
    key_files = [
        'app.py',
        'retrain_real.py',
        'train_real_model.py',
        'pipeline.py',
        'config.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("\nKey files:")
    for file_name in key_files:
        file_path = Path(file_name)
        exists = file_path.exists()
        results['key_files'][file_name] = exists
        
        if exists:
            print(f"  ✓ {file_name}")
        else:
            print(f"  ❌ {file_name}")
    
    audit_results['file_structure'] = results
    return results


# ============================================================================
# STEP 8: PROJECT COMPLETION ESTIMATION
# ============================================================================

def calculate_completion_score():
    """Calculate project completion percentage"""
    print("\n" + "="*80)
    print("STEP 8: PROJECT COMPLETION ESTIMATION")
    print("="*80)
    
    score = 0
    max_score = 100
    
    # Data availability (20 points)
    if audit_results['data_validation'].get('data_dir_exists'):
        score += 10
        if audit_results['data_validation'].get('csv_count', 0) >= 5:
            score += 10
    
    # Feature pipeline (15 points)
    if audit_results['feature_validation'].get('pipeline_works'):
        score += 15
    
    # Model training (25 points)
    if audit_results['model_validation'].get('models_dir_exists'):
        score += 5
        if audit_results['model_validation'].get('latest_version', 0) > 0:
            score += 10
            if audit_results['model_validation'].get('model_loaded'):
                score += 10
    
    # Experiment tracking (10 points)
    if audit_results['experiment_log'].get('log_exists'):
        score += 5
        if audit_results['experiment_log'].get('experiment_count', 0) > 0:
            score += 5
    
    # Drift monitoring (10 points)
    if audit_results['drift_check'].get('drift_report_exists'):
        score += 10
    
    # Performance test (10 points)
    if audit_results['performance_test'].get('test_passed'):
        score += 10
    
    # UI presence (5 points)
    if audit_results['file_structure']['key_files'].get('app.py'):
        score += 5
    
    # Tests presence (5 points)
    if audit_results['file_structure']['directories'].get('tests', {}).get('exists'):
        score += 5
    
    audit_results['completion_score'] = score
    
    print(f"\n{'='*80}")
    print(f"PROJECT COMPLETION SCORE: {score}/{max_score} ({score}%)")
    print(f"{'='*80}")
    
    if score >= 90:
        print("🎉 Excellent! Project is production-ready")
    elif score >= 70:
        print("✓ Good! Project is well-developed")
    elif score >= 50:
        print("⚠ Fair. Some components need attention")
    else:
        print("❌ Needs work. Several components missing")
    
    return score


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_markdown_report():
    """Generate comprehensive markdown report"""
    print("\n" + "="*80)
    print("GENERATING MARKDOWN REPORT")
    print("="*80)
    
    report = []
    
    # Header
    report.append("# Project Runtime Audit Report")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Project:** AI Financial Time-Series Analysis")
    report.append("")
    report.append("---")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    score = audit_results['completion_score']
    report.append(f"**Completion Score:** {score}/100 ({score}%)")
    report.append("")
    
    if score >= 90:
        report.append("✅ **Status:** Production-Ready")
    elif score >= 70:
        report.append("✅ **Status:** Well-Developed")
    elif score >= 50:
        report.append("⚠️ **Status:** Needs Attention")
    else:
        report.append("❌ **Status:** Incomplete")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Data Validation
    report.append("## 1. Data Validation")
    report.append("")
    data_val = audit_results['data_validation']
    
    if data_val.get('data_dir_exists'):
        report.append(f"✅ Data directory exists: `{DATA_DIR}`")
        report.append(f"- **CSV Files:** {data_val.get('csv_count', 0)}")
        report.append(f"- **Total Rows:** {data_val.get('total_rows', 0):,}")
        report.append(f"- **Valid Files:** {len(data_val.get('valid_files', []))}")
        
        if data_val.get('date_range'):
            report.append(f"- **Date Range:** {data_val['date_range']['start']} to {data_val['date_range']['end']}")
        
        if data_val.get('tickers'):
            report.append(f"- **Tickers:** {', '.join(data_val['tickers'])}")
        
        if data_val.get('invalid_files'):
            report.append("")
            report.append("⚠️ **Invalid Files:**")
            for invalid in data_val['invalid_files']:
                report.append(f"  - {invalid['file']}: {invalid['reason']}")
    else:
        report.append("❌ Data directory not found")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Feature Validation
    report.append("## 2. Feature Pipeline Validation")
    report.append("")
    feat_val = audit_results['feature_validation']
    
    if feat_val.get('pipeline_works'):
        report.append("✅ Feature pipeline working correctly")
        report.append("")
        report.append(f"**Test File:** {feat_val.get('sample_file', 'N/A')}")
        report.append("")
        report.append("**Generated Features:**")
        for feature in feat_val.get('features_generated', []):
            nan_count = feat_val.get('nan_counts', {}).get(feature, 0)
            report.append(f"- ✅ {feature} ({nan_count} NaN values)")
    else:
        report.append("❌ Feature pipeline has issues")
        if feat_val.get('missing_features'):
            report.append("")
            report.append("**Missing Features:**")
            for feature in feat_val['missing_features']:
                report.append(f"- ❌ {feature}")
    
    report.append("")
    report.append("---")
    report.append("")

    # Model Validation
    report.append("## 3. Model Validation")
    report.append("")
    model_val = audit_results['model_validation']
    
    if model_val.get('models_dir_exists'):
        report.append(f"✅ Models directory exists: `{MODELS_DIR}`")
        report.append("")
        
        if model_val.get('latest_version'):
            report.append(f"**Latest Version:** v{model_val['latest_version']}")
            report.append("")
            
            report.append("**Model Files:**")
            for file, exists in model_val.get('model_files', {}).items():
                status = "✅" if exists else "❌"
                report.append(f"- {status} {file}")
            
            report.append("")
            
            if model_val.get('n_clusters'):
                report.append(f"**Clusters:** {model_val['n_clusters']}")
            
            if model_val.get('training_timestamp'):
                report.append(f"**Training Timestamp:** {model_val['training_timestamp']}")
            
            if model_val.get('metrics'):
                report.append("")
                report.append("**Metrics:**")
                metrics = model_val['metrics']
                if 'silhouette_score' in metrics:
                    report.append(f"- Silhouette Score: {metrics['silhouette_score']:.4f}")
                if 'davies_bouldin_index' in metrics:
                    report.append(f"- Davies-Bouldin Index: {metrics['davies_bouldin_index']:.4f}")
            
            if model_val.get('model_loaded'):
                report.append("")
                report.append("✅ Model loaded successfully")
        else:
            report.append("⚠️ No trained model versions found")
    else:
        report.append("❌ Models directory not found")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Performance Test
    report.append("## 4. Performance Test")
    report.append("")
    perf_test = audit_results['performance_test']
    
    if perf_test.get('test_passed'):
        report.append("✅ Performance test passed")
        report.append("")
        report.append(f"- **Sample Size:** {perf_test.get('sample_size', 0)}")
        report.append(f"- **Runtime:** {perf_test.get('runtime_seconds', 0)}s")
        report.append(f"- **Unique Clusters:** {perf_test.get('unique_clusters', 0)}")
        report.append(f"- **Predictions Generated:** {'Yes' if perf_test.get('predictions_generated') else 'No'}")
    else:
        report.append("❌ Performance test failed or not run")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Experiment Log
    report.append("## 5. Experiment Tracking")
    report.append("")
    exp_log = audit_results['experiment_log']
    
    if exp_log.get('log_exists'):
        report.append(f"✅ Experiment log exists: `{EXPERIMENTS_LOG}`")
        report.append("")
        report.append(f"**Total Experiments:** {exp_log.get('experiment_count', 0)}")
        
        if exp_log.get('last_experiment'):
            report.append("")
            report.append("**Last Experiment:**")
            last = exp_log['last_experiment']
            report.append(f"- Version: v{last.get('version', 'N/A')}")
            report.append(f"- Timestamp: {last.get('timestamp', 'N/A')}")
            report.append(f"- K Selected: {last.get('K_selected', 'N/A')}")
            report.append(f"- Silhouette Score: {last.get('silhouette_score', 0):.4f}")
            report.append(f"- Total Samples: {last.get('total_samples', 0):,}")
    else:
        report.append("⚠️ Experiment log not found")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Drift Check
    report.append("## 6. Data Drift Monitoring")
    report.append("")
    drift = audit_results['drift_check']
    
    if drift.get('drift_report_exists'):
        report.append("✅ Drift report exists")
        report.append("")
        
        if drift.get('has_drift'):
            report.append("⚠️ **Data drift detected!**")
            report.append("")
            report.append("**Drifted Features:**")
            for feature in drift.get('drifted_features', []):
                report.append(f"- {feature}")
        else:
            report.append("✅ No data drift detected")
    else:
        report.append("⚠️ Drift report not found")
    
    report.append("")
    report.append("---")
    report.append("")

    # File Structure
    report.append("## 7. File Structure")
    report.append("")
    file_struct = audit_results['file_structure']
    
    report.append("**Directories:**")
    for dir_name, info in file_struct.get('directories', {}).items():
        if info.get('exists'):
            report.append(f"- ✅ `{dir_name}/` ({info.get('file_count', 0)} items)")
        else:
            report.append(f"- ❌ `{dir_name}/` (not found)")
    
    report.append("")
    report.append("**Key Files:**")
    for file_name, exists in file_struct.get('key_files', {}).items():
        status = "✅" if exists else "❌"
        report.append(f"- {status} `{file_name}`")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Warnings
    if audit_results['warnings']:
        report.append("## ⚠️ Warnings")
        report.append("")
        for warning in audit_results['warnings']:
            report.append(f"- {warning}")
        report.append("")
        report.append("---")
        report.append("")
    
    # Errors
    if audit_results['errors']:
        report.append("## ❌ Errors")
        report.append("")
        for error in audit_results['errors']:
            report.append(f"- {error}")
        report.append("")
        report.append("---")
        report.append("")
    
    # Recommendations
    report.append("## 📋 Recommendations")
    report.append("")
    
    recommendations = []
    
    if not data_val.get('data_dir_exists'):
        recommendations.append("Create `data/real/` directory and add stock CSV files")
    elif data_val.get('csv_count', 0) < 5:
        recommendations.append("Add more stock data files for better model training")
    
    if not feat_val.get('pipeline_works'):
        recommendations.append("Fix feature engineering pipeline")
    
    if not model_val.get('latest_version'):
        recommendations.append("Run `python retrain_real.py` to train a model")
    
    if not exp_log.get('log_exists'):
        recommendations.append("Initialize experiment tracking")
    
    if not drift.get('drift_report_exists'):
        recommendations.append("Run drift monitoring")
    
    if drift.get('has_drift'):
        recommendations.append("Investigate data drift and consider retraining model")
    
    if not perf_test.get('test_passed'):
        recommendations.append("Fix model loading or prediction issues")
    
    if score < 70:
        recommendations.append("Complete missing components to reach production-ready status")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report.append(f"{i}. {rec}")
    else:
        report.append("✅ No critical recommendations. System is healthy!")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Footer
    report.append("## Summary")
    report.append("")
    report.append(f"**Completion Score:** {score}/100")
    report.append("")
    
    if score >= 90:
        report.append("🎉 **Excellent!** Project is production-ready with all major components working.")
    elif score >= 70:
        report.append("✅ **Good!** Project is well-developed with minor improvements needed.")
    elif score >= 50:
        report.append("⚠️ **Fair.** Some components need attention before production deployment.")
    else:
        report.append("❌ **Needs Work.** Several critical components are missing or broken.")
    
    report.append("")
    report.append("---")
    report.append("")
    report.append(f"*Report generated by audit_system.py on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*")
    
    # Write report with UTF-8 encoding
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"\n✓ Report saved to: {REPORT_FILE}")
    
    return report


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main audit execution"""
    print("\n" + "="*80)
    print("AI FINANCIAL TIME-SERIES ANALYSIS - SYSTEM RUNTIME AUDIT")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    try:
        # Run all validation steps
        validate_data()
        validate_features()
        validate_model()
        test_performance()
        validate_experiments()
        check_drift()
        check_file_structure()
        calculate_completion_score()
        
        # Generate report
        generate_markdown_report()
        
        print("\n" + "="*80)
        print("AUDIT COMPLETE")
        print("="*80)
        print(f"Completion Score: {audit_results['completion_score']}/100")
        print(f"Warnings: {len(audit_results['warnings'])}")
        print(f"Errors: {len(audit_results['errors'])}")
        print(f"Report: {REPORT_FILE}")
        print("="*80 + "\n")
        
        # Exit with appropriate code
        if audit_results['errors']:
            sys.exit(1)
        else:
            sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
