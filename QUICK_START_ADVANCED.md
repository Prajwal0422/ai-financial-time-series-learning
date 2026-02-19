# Quick Start Guide - Advanced ML Features

**Version:** 3.0.0  
**Date:** February 18, 2026

This guide shows you how to use the new professional ML engineering features.

---

## 🚀 Complete Workflow

### Option 1: Synthetic Data (Fast - for testing)

```bash
# 1. Generate synthetic data
python scripts/generate_realistic_data.py

# 2. Process features
python pipeline.py

# 3. Run advanced training
python train_model_advanced.py

# 4. Start application
python app.py
```

### Option 2: Real Data (Recommended - for production)

```bash
# 1. Download real stock data from Yahoo Finance
python scripts/download_yahoo_data.py

# 2. Process features
python pipeline.py

# 3. Run advanced training pipeline
python train_model_advanced.py

# 4. Run tests to verify
python -m pytest tests/ -v

# 5. Start application
python app.py
```

---

## 📊 Advanced Training Pipeline

When you run `train_model_advanced.py`, it executes 9 steps:

```
Step 1: Data Loading
├── Loads all processed stock data
├── Combines into single dataset
└── Reports: n_samples, n_stocks

Step 2: Statistical Validation
├── ADF stationarity tests on returns/volatility
├── Feature distribution analysis
├── Data quality checks
└── Saves: models/validation_report.json

Step 3: Feature Preparation
├── Selects 7 ML features
├── Handles missing values
├── StandardScaler normalization
└── Reports: feature matrix shape

Step 4: Model Selection
├── Evaluates K=3 to K=8
├── Computes 4 metrics per K
├── Selects optimal K (silhouette)
├── Generates comparison plot
└── Saves: models/model_comparison.json

Step 5: Final Model Training
├── Trains with optimal K
├── Computes final metrics
└── Reports: silhouette, DB, CH scores

Step 6: Stability Analysis
├── Runs clustering 10 times
├── Computes ARI and NMI
├── Statistical summary
└── Saves: models/stability_metrics.json

Step 7: Regime Insights
├── Analyzes regime characteristics
├── Generates interpretations
├── Creates summary report
└── Saves: models/regime_insights.json

Step 8: Model Versioning
├── Creates version tag (v_YYYYMMDD_HHMMSS)
├── Saves all artifacts
├── Updates registry
└── Saves as production model

Step 9: Experiment Tracking
├── Logs parameters
├── Logs metrics
├── Logs metadata
└── Updates: experiments/experiment_log.jsonl
```

**Expected Output:**
```
✓ Model Version: v_20260218_143022
✓ Experiment ID: exp_a3f8c2d1
✓ Optimal K: 4
✓ Silhouette Score: 0.1686
✓ Stability (ARI): 0.8234 ± 0.0156
```

---

## 🔧 Using Individual Modules

### 1. Download Real Data

```python
from scripts.download_yahoo_data import download_multiple_stocks

# Download specific stocks
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
results = download_multiple_stocks(
    tickers=tickers,
    start_date='2020-01-01',
    end_date='2024-12-31'
)

# Check results
for ticker, df in results.items():
    print(f"{ticker}: {len(df)} rows")
```

**Command Line:**
```bash
python scripts/download_yahoo_data.py
```

---

### 2. Model Selection

```python
from analysis.model_selection import (
    evaluate_k_range, 
    select_optimal_k, 
    plot_model_comparison
)
import numpy as np
from sklearn.preprocessing import StandardScaler

# Prepare data
X = df[feature_columns].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Evaluate different K values
results = evaluate_k_range(X_scaled, k_range=(3, 9))

# Select optimal K
optimal_k = select_optimal_k(results, method='silhouette')

# Generate comparison plot
plot_model_comparison(results)
```

**Output:**
- Console: Metrics for each K
- File: `static/charts/model_comparison.png`
- File: `models/model_comparison.json`

---

### 3. Stability Analysis

```python
from analysis.stability import measure_clustering_stability

# Measure stability
stability_metrics = measure_clustering_stability(
    X_scaled, 
    n_clusters=4, 
    n_runs=10
)

print(f"ARI: {stability_metrics['ari_mean']:.4f} ± {stability_metrics['ari_std']:.4f}")
print(f"NMI: {stability_metrics['nmi_mean']:.4f} ± {stability_metrics['nmi_std']:.4f}")
```

**Interpretation:**
- ARI > 0.8: Highly stable
- ARI > 0.6: Moderately stable
- ARI < 0.6: Low stability (consider different K or features)

---

### 4. Statistical Validation

```python
from analysis.statistical_validation import run_statistical_validation

# Run comprehensive validation
validation_report = run_statistical_validation(df)

# Check stationarity
for feature, result in validation_report['stationarity_tests'].items():
    status = "Stationary" if result['stationary'] else "Non-stationary"
    print(f"{feature}: {status} (p={result['p_value']:.4f})")

# Check data quality
quality = validation_report['data_quality']
print(f"Total rows: {quality['total_rows']}")
print(f"Missing values: {len(quality['missing_values'])} columns")
```

---

### 5. Experiment Tracking

```python
from analysis.experiment_tracker import ExperimentTracker

# Initialize tracker
tracker = ExperimentTracker()

# Log an experiment
exp_id = tracker.log_experiment(
    experiment_name="KMeans_K4_7features",
    parameters={
        'n_clusters': 4,
        'n_features': 7,
        'features': ['Log_Return', 'Volatility_10', ...],
        'n_init': 20,
        'random_state': 42
    },
    metrics={
        'silhouette_score': 0.1686,
        'davies_bouldin_index': 1.4894,
        'ari_mean': 0.8234
    },
    metadata={
        'n_samples': 36010,
        'n_stocks': 10
    }
)

print(f"Experiment logged: {exp_id}")

# View experiment history
tracker.print_summary()

# Get best experiment
best = tracker.get_best_experiment('silhouette_score', maximize=True)
print(f"Best experiment: {best['experiment_id']}")

# Compare experiments
comparison = tracker.compare_experiments(['exp_abc123', 'exp_def456'])
print(comparison)
```

---

### 6. Model Versioning

```python
from analysis.model_versioning import ModelVersionManager

# Initialize manager
manager = ModelVersionManager()

# Save a new version
version_tag = manager.save_model(
    model=kmeans_model,
    scaler=scaler,
    features=feature_list,
    metrics=metrics_dict,
    description="Optimal K=4 selected via systematic comparison"
)

print(f"Model saved as: {version_tag}")

# Load a specific version
model, scaler, features, metrics, metadata = manager.load_model(version_tag)

# Load latest version
model, scaler, features, metrics, metadata = manager.load_model()

# List all versions
versions = manager.list_versions()
for v in versions:
    print(f"{v['version']}: K={v['n_clusters']}, Silhouette={v['metrics']['silhouette_score']:.4f}")

# Compare versions
comparison = manager.compare_versions(['v_20260218_120000', 'v_20260218_143022'])
print(comparison)

# Print registry
manager.print_registry()
```

---

### 7. Regime Insights

```python
from analysis.regime_insights import (
    create_regime_summary_report,
    get_regime_interpretation
)

# Create comprehensive report
report = create_regime_summary_report(df_with_regimes)

# Get interpretation for specific regime
interpretation = get_regime_interpretation(regime_id=0)

print(f"Regime {interpretation['regime_id']}: {interpretation['label']}")
print(f"Description: {interpretation['description']}")
print(f"Frequency: {interpretation['percentage']:.1f}%")
print("Characteristics:")
for char in interpretation['characteristics']:
    print(f"  • {char}")
```

**Example Output:**
```
Regime 0: Stable Growth
Description: Positive returns with low volatility - steady upward movement
Frequency: 33.0%
Characteristics:
  • Positive average return (0.082%)
  • Low volatility (1.23%)
  • Positive momentum
  • Price above moving average (bullish)
```

---

## 📁 Generated Artifacts

After running the advanced pipeline, you'll have:

```
models/
├── versions/
│   └── v_20260218_143022/
│       ├── model.pkl              # Trained K-Means model
│       ├── scaler.pkl             # StandardScaler
│       ├── features.pkl           # Feature list
│       ├── metrics.pkl            # Performance metrics
│       └── metadata.json          # Version metadata
├── model_registry.json            # All versions
├── model_comparison.json          # K comparison results
├── stability_metrics.json         # Stability analysis
├── validation_report.json         # Statistical validation
└── regime_insights.json           # Regime interpretations

experiments/
├── experiment_log.jsonl           # Detailed log (append-only)
└── experiments_summary.csv        # Tabular summary

static/charts/
└── model_comparison.png           # K comparison visualization
```

---

## 🔍 Inspecting Results

### View Model Comparison

```python
import json

with open('models/model_comparison.json', 'r') as f:
    comparison = json.load(f)

print(f"Optimal K: {comparison['optimal_k']}")
for k, sil in zip(comparison['k_values'], comparison['silhouette_scores']):
    print(f"K={k}: Silhouette={sil:.4f}")
```

### View Stability Metrics

```python
import json

with open('models/stability_metrics.json', 'r') as f:
    stability = json.load(f)

print(f"ARI: {stability['ari_mean']:.4f} ± {stability['ari_std']:.4f}")
print(f"NMI: {stability['nmi_mean']:.4f} ± {stability['nmi_std']:.4f}")
```

### View Validation Report

```python
import json

with open('models/validation_report.json', 'r') as f:
    validation = json.load(f)

# Stationarity tests
for feature, result in validation['stationarity_tests'].items():
    print(f"{feature}: {result['interpretation']} (p={result['p_value']:.4f})")

# Data quality
quality = validation['data_quality']
print(f"\nData Quality:")
print(f"  Total rows: {quality['total_rows']}")
print(f"  Duplicates: {quality['duplicate_rows']}")
print(f"  Missing values: {len(quality['missing_values'])} columns")
```

### View Regime Insights

```python
import json

with open('models/regime_insights.json', 'r') as f:
    insights = json.load(f)

for regime_key, interp in insights['interpretations'].items():
    print(f"\n{regime_key.upper()}: {interp['label']}")
    print(f"  {interp['description']}")
    print(f"  Frequency: {interp['percentage']:.1f}%")
```

### View Experiment Log

```python
import pandas as pd

# Read CSV summary
df = pd.read_csv('experiments/experiments_summary.csv')
print(df[['experiment_id', 'experiment_name', 'metric_silhouette_score']])

# Or read JSONL for full details
import json

with open('experiments/experiment_log.jsonl', 'r') as f:
    for line in f:
        exp = json.load(line)
        print(f"{exp['experiment_id']}: {exp['experiment_name']}")
```

---

## 🧪 Testing

Run tests to verify everything works:

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_clustering.py -v

# With coverage
python -m pytest tests/ --cov=analysis --cov-report=html
```

**Expected:** 18 tests passed

---

## 🎯 Common Workflows

### Workflow 1: Quick Experiment

```bash
# 1. Download data
python scripts/download_yahoo_data.py

# 2. Process
python pipeline.py

# 3. Train
python train_model_advanced.py

# 4. View results
python -c "from analysis.experiment_tracker import ExperimentTracker; ExperimentTracker().print_summary()"
```

### Workflow 2: Compare Different Configurations

```python
from analysis.experiment_tracker import ExperimentTracker

tracker = ExperimentTracker()

# Train with different K values
for k in [3, 4, 5]:
    # Train model with K=k
    # ...
    
    # Log experiment
    tracker.log_experiment(
        experiment_name=f"KMeans_K{k}",
        parameters={'n_clusters': k},
        metrics={'silhouette': silhouette_score}
    )

# Find best
best = tracker.get_best_experiment('silhouette', maximize=True)
print(f"Best K: {best['parameters']['n_clusters']}")
```

### Workflow 3: Model Deployment

```python
from analysis.model_versioning import ModelVersionManager

manager = ModelVersionManager()

# Load latest production model
model, scaler, features, metrics, metadata = manager.load_model()

# Use for inference
X_new = new_data[features]
X_scaled = scaler.transform(X_new)
predictions = model.predict(X_scaled)
```

---

## 💡 Tips & Best Practices

### 1. Always Run Validation First
```python
# Check data quality before training
validation_report = run_statistical_validation(df)
```

### 2. Use Stability Analysis
```python
# Verify clustering is stable
stability = measure_clustering_stability(X_scaled, n_clusters=optimal_k)
if stability['ari_mean'] < 0.6:
    print("Warning: Low stability - consider different K or features")
```

### 3. Track All Experiments
```python
# Log every training run
tracker.log_experiment(name, parameters, metrics, metadata)
```

### 4. Version All Models
```python
# Save with descriptive tags
manager.save_model(model, scaler, features, metrics, 
                   description="Production model - validated on 10 years data")
```

### 5. Document Regime Insights
```python
# Generate interpretations for stakeholders
report = create_regime_summary_report(df_with_regimes)
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Issue: "No module named 'statsmodels'"
```bash
pip install statsmodels
```

### Issue: "Model file not found"
```bash
# Train model first
python train_model_advanced.py
```

### Issue: "Feature mismatch"
```python
# Check feature alignment
print(f"Training features: {joblib.load('models/features.pkl')}")
print(f"Data features: {df.columns.tolist()}")
```

### Issue: "Low stability (ARI < 0.6)"
- Try different K values
- Try different features
- Check data quality
- Increase n_runs for more reliable estimate

---

## 📚 Further Reading

- [PROFESSIONAL_UPGRADES.md](PROFESSIONAL_UPGRADES.md) - Complete upgrade details
- [README.md](README.md) - Full project documentation
- [PROJECT_COMPLETE_SUMMARY.md](PROJECT_COMPLETE_SUMMARY.md) - Comprehensive summary

---

**Last Updated:** February 18, 2026  
**Version:** 3.0.0  
**Status:** ✅ Production Ready

---

*Happy experimenting! 🚀*
