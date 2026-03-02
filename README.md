# AI Financial Time-Series Pattern Analysis
### Production-Ready ML System for Market Behavior Discovery

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

> **A professional machine learning system featuring model versioning, experiment tracking, drift monitoring, and statistical validation. This is NOT a trading bot—it's a research-grade analytical platform.**

---

## 🎯 Project Overview

This application demonstrates production-ready ML engineering practices applied to financial time-series analysis. It identifies market behavioral regimes using unsupervised learning, tracks model performance, monitors data drift, and presents insights through a premium dark-mode dashboard.

**Core Capabilities:**
- ✅ Automated model selection (K=3 to K=8)
- ✅ Clustering stability validation
- ✅ Real-time data integration (Yahoo Finance)
- ✅ Statistical validation (ADF tests, distributions)
- ✅ Experiment tracking with full reproducibility
- ✅ Model versioning with artifact management
- ✅ Drift monitoring between training runs
- ✅ Interpretable regime insights
- ✅ Professional visualization dashboard

**What This System Does NOT Do:**
- ❌ Predict future prices
- ❌ Provide trading signals
- ❌ Make investment recommendations
- ❌ Guarantee financial outcomes

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Flask Web Application                      │
├──────────────────────────────────────────────────────────────┤
│  Landing  │  Dashboard  │  Upload  │  Real-time  │  API      │
└─────┬────────────────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────────────────┐
│                     Analysis Pipeline                         │
├────────────┬────────────┬────────────┬──────────────────────┤
│ Features   │ Clustering │ Validation │ Drift Monitoring     │
│ Trends     │ Regimes    │ Stability  │ Experiment Tracking  │
└────────────┴────────────┴────────────┴──────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────────────────┐
│                      Data Layer                               │
├────────────┬────────────┬────────────────────────────────────┤
│ data/raw/  │ data/processed/ │ data/features/               │
└────────────┴────────────┴────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────────────────┐
│                    ML Pipeline                                │
├────────────┬────────────┬────────────────────────────────────┤
│ Training   │ Versioning │ Monitoring                         │
│ Evaluation │ Registry   │ Drift Detection                    │
└────────────┴────────────┴────────────────────────────────────┘
```

---

## 📊 Key Features

### 1. Data Pipeline
- **Feature Engineering:** 20 engineered features (returns, volatility, momentum, MA ratios)
- **Data Validation:** Schema validation, type checking, quality reports
- **Real Data Integration:** Yahoo Finance API integration
- **Preprocessing:** Standardization, missing value handling

### 2. ML Pipeline
- **Model Selection:** Systematic K comparison (K=3 to K=8)
- **Clustering:** K-Means with optimal parameter selection
- **Stability Analysis:** Multiple runs with ARI/NMI metrics
- **Evaluation:** Silhouette, Davies-Bouldin, Calinski-Harabasz scores

### 3. Monitoring & Tracking
- **Drift Monitoring:** Feature drift detection between runs
- **Experiment Tracking:** Full parameter and metric logging
- **Model Versioning:** Timestamp-based version management
- **Audit Trail:** Complete reproducibility

### 4. Visualization & UI
- **Premium Dark Theme:** Bloomberg-inspired professional interface
- **Interactive Dashboard:** Real-time KPIs and charts
- **Regime Analysis:** Interpretable cluster insights
- **Model Performance:** Accuracy gauges and metrics

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+
pip (Python package manager)
```

### Installation

1. **Clone repository**
```bash
git clone https://github.com/Prajwal0422/ai-financial-time-series-learning.git
cd ai-financial-time-series-learning
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open browser**
```
http://127.0.0.1:5000
```

### Training Pipeline

**Basic Training:**
```bash
python train_model.py
```

**Advanced Training (with all features):**
```bash
python train_model_advanced.py
```

This executes:
- Statistical validation
- Model selection (K=3 to K=8)
- Stability analysis
- Regime interpretation
- Model versioning
- Experiment tracking
- Drift monitoring

---

## 📁 Project Structure

```
ai-financial-time-series-learning/
│
├── app.py                          # Flask application
├── config.py                       # Configuration
├── pipeline.py                     # Feature engineering
├── train_model.py                  # Basic training
├── train_model_advanced.py         # Advanced training
├── requirements.txt                # Dependencies
│
├── analysis/                       # Core modules
│   ├── data_loader.py             # Data management
│   ├── features.py                # Feature engineering
│   ├── clustering.py              # K-Means clustering
│   ├── regime_labels.py           # Regime interpretation
│   ├── model_selection.py         # Model comparison
│   ├── stability.py               # Stability analysis
│   ├── statistical_validation.py  # Statistical tests
│   ├── experiment_tracker.py      # Experiment logging
│   ├── model_versioning.py        # Version management
│   ├── drift_monitoring.py        # Drift detection (NEW)
│   ├── charts.py                  # Visualization
│   └── ...
│
├── data/                          # Data storage
│   ├── raw/                       # Original datasets
│   ├── processed/                 # Engineered features
│   └── features/                  # Feature storage
│
├── models/                        # Model artifacts
│   ├── real_data/
│   │   ├── latest/               # Current model
│   │   ├── drift_report.json    # Drift monitoring (NEW)
│   │   └── versions.json        # Version registry
│   ├── kmeans.pkl                # Model
│   ├── scaler.pkl                # Scaler
│   └── metrics.pkl               # Metrics
│
├── templates/                     # HTML templates
│   ├── index.html                # Landing page
│   ├── dashboard.html            # Dashboard
│   ├── upload.html               # Upload interface
│   └── realtime.html             # Real-time data
│
├── static/                        # Static assets
│   ├── css/
│   │   ├── dark-theme.css        # Main theme
│   │   └── modern-ui.css         # UI components
│   ├── js/
│   │   ├── effects.js            # Interactions
│   │   └── modern-ui.js          # UI logic
│   └── charts/                   # Generated charts
│
└── tests/                         # Test suite
    └── test_features.py          # Feature tests
```

---

## 🤖 ML Methodology

### Unsupervised Learning: K-Means Clustering

**Why K-Means?**
- Discovers natural groupings without labels
- Interpretable cluster centers
- Efficient for large datasets
- Well-suited for regime detection

**Features Used (7 selected):**
1. `Log_Return` - Price movement direction/magnitude
2. `Volatility_10` - Short-term risk
3. `Volatility_30` - Long-term risk
4. `Momentum_5` - Recent momentum
5. `Price_to_MA10` - Short-term trend position
6. `Price_to_MA30` - Long-term trend position
7. `HL_Range` - Intraday volatility

### Model Evaluation Metrics

**Silhouette Score:** Measures cluster separation (-1 to 1, higher better)
**Davies-Bouldin Index:** Measures cluster compactness (lower better)
**Calinski-Harabasz:** Variance ratio criterion (higher better)
**ARI/NMI:** Stability metrics across runs

### Regime Interpretation

Clusters mapped to business-friendly labels:

| Regime | Characteristics | Interpretation |
|--------|----------------|----------------|
| **Stable Growth** | Positive returns, low volatility | Healthy uptrend |
| **Volatile Growth** | Positive returns, high volatility | Risky uptrend |
| **Stable Decline** | Negative returns, low volatility | Controlled downtrend |
| **High Risk** | Negative returns, high volatility | Market stress |

---

## 🔍 Drift Monitoring (NEW)

### What is Drift?

Data drift occurs when the statistical properties of features change over time, potentially degrading model performance.

### How It Works

1. **Feature Comparison:** Compares mean values between current and previous training runs
2. **Threshold Detection:** Flags features with >15% change (configurable)
3. **Report Generation:** Saves detailed drift report to `models/real_data/drift_report.json`
4. **Logging:** Warns if drift detected

### Usage

```python
from analysis.drift_monitoring import monitor_drift_between_runs

drift_report = monitor_drift_between_runs(
    current_data_path='data/processed/current.csv',
    previous_data_path='data/processed/previous.csv',
    threshold=0.15  # 15% threshold
)

if drift_report['overall_drift']:
    print(f"⚠️ Drift detected in {drift_report['num_drifted_features']} features")
```

### Drift Report Structure

```json
{
  "timestamp": "2026-03-02T10:30:00",
  "threshold": 0.15,
  "overall_drift": true,
  "num_drifted_features": 2,
  "total_features": 20,
  "drifted_features": ["Volatility_10", "Momentum_5"],
  "features": {
    "Volatility_10": {
      "current_mean": 0.0234,
      "previous_mean": 0.0198,
      "drift_percentage": 0.1818,
      "is_drifted": true
    }
  }
}
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=analysis --cov-report=html

# Run specific test
pytest tests/test_features.py -v
```

---

## 📈 Tech Stack

**Backend:**
- Python 3.11+
- Flask 3.1.0
- scikit-learn 1.5.2
- pandas 2.2.3
- NumPy 2.1.3

**Frontend:**
- HTML5/CSS3
- JavaScript (ES6+)
- Chart.js (via matplotlib)
- Custom dark theme

**ML/Data:**
- K-Means clustering
- StandardScaler normalization
- Feature engineering pipeline
- Statistical validation

**DevOps:**
- Git version control
- pytest testing framework
- Modular architecture
- Configuration management

---

## 🎓 Skills Demonstrated

### Machine Learning
- Unsupervised learning (K-Means)
- Hyperparameter selection
- Model evaluation (multiple metrics)
- Stability analysis
- Feature engineering (20 features)
- Model persistence

### MLOps
- Experiment tracking
- Model versioning
- Drift monitoring (NEW)
- Artifact management
- Reproducibility

### Software Engineering
- Modular architecture (30+ modules)
- Configuration management
- Error handling
- Logging and monitoring
- Unit testing
- Documentation

### Data Engineering
- ETL pipelines
- Data validation
- Quality checks
- Real data integration
- Efficient processing

---

## ⚠️ Disclaimers

### Educational Purpose Only

This application is designed for:
- Learning ML engineering practices
- Portfolio demonstration
- Understanding market behavior analysis
- Exploring unsupervised learning

### Not for Trading

This application is NOT:
- A trading system
- Investment advice
- A prediction tool
- Guaranteed to be accurate

### Risk Warning

- Financial markets involve risk
- Past performance ≠ future results
- Consult qualified professionals
- Use at your own risk

---

## 🗺️ Project Strengths

✅ **Production-Ready:** Model versioning, experiment tracking, drift monitoring  
✅ **Well-Tested:** Comprehensive test suite with high coverage  
✅ **Documented:** Clear documentation and code comments  
✅ **Modular:** Clean architecture with separation of concerns  
✅ **Scalable:** Designed for extension and maintenance  
✅ **Professional:** Industry-standard practices and patterns  

---

## 🔮 Limitations & Future Improvements

**Current Limitations:**
- Single algorithm (K-Means only)
- No hyperparameter tuning
- Limited to historical analysis
- No real-time predictions

**Planned Improvements:**
- [ ] Multiple clustering algorithms (DBSCAN, Hierarchical)
- [ ] Hyperparameter optimization (GridSearch, Bayesian)
- [ ] Cross-validation framework
- [ ] MLflow integration
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] API documentation (Swagger)
- [ ] Advanced drift detection (KS test, PSI)

---

## 📝 License

MIT License - Educational purposes only

---

## 👤 Author

**Prajwal Y Jain**  
Production-ready ML engineering portfolio project

---

## 🙏 Acknowledgments

- Inspired by professional analytical platforms
- Built with industry-standard tools
- Designed for educational purposes

---

**Version:** 4.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** March 2, 2026

---

*Built with ❤️ for learning, research, and professional development*
