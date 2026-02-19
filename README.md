# AI Financial Time-Series Pattern Analysis
### Professional Mid-Level ML Engineering System for Market Behavior Discovery

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-18%20passed-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](PROFESSIONAL_UPGRADES.md)

> **A professional machine learning system with model selection, stability analysis, experiment tracking, and statistical validation. Features real data integration, model versioning, and interpretable regime insights. This is NOT a trading bot—it's a research-grade analytical tool.**

---

## 🎯 Project Purpose

This application demonstrates professional ML engineering practices applied to financial time-series analysis. It identifies market behavioral regimes using unsupervised learning, calculates statistical metrics, and presents insights through a premium dark-mode dashboard.

**What This System Does:**
- ✅ Systematically selects optimal clustering parameters (K=3 to K=8)
- ✅ Validates clustering stability across multiple runs
- ✅ Downloads real stock data from Yahoo Finance
- ✅ Performs statistical validation (ADF tests, distributions)
- ✅ Tracks experiments with full reproducibility
- ✅ Manages model versions with metadata
- ✅ Generates interpretable regime insights
- ✅ Visualizes patterns with professional charts

**What This System Does NOT Do:**
- ❌ Predict future prices
- ❌ Provide trading signals
- ❌ Make investment recommendations
- ❌ Guarantee any financial outcomes

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Flask Web Application                    │
├─────────────────────────────────────────────────────────────┤
│  Landing Page  │  Dashboard  │  API Endpoints  │  Charts    │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Analysis Layer                             │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Data Loader  │  Features    │  Clustering  │  Regime Labels │
│ Returns      │  Trends      │  Charts      │  Validation    │
└──────────────┴──────────────┴──────────────┴────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer                                 │
├──────────────┬──────────────┬──────────────────────────────┤
│  data/raw/   │ data/processed/ │  data/features/           │
│  (36,500     │  (36,010 rows,  │  (Reserved)               │
│   rows)      │   20 features)  │                           │
└──────────────┴──────────────┴───────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                   ML Pipeline                                │
├──────────────┬──────────────┬──────────────────────────────┤
│ pipeline.py  │ train_model.py│  models/                    │
│ (Feature     │ (K-Means      │  (Persisted artifacts)      │
│  Engineering)│  Training)    │                             │
└──────────────┴──────────────┴───────────────────────────────┘
```

---

## 📊 Key Features

### 🎯 Professional ML Engineering (NEW in v3.0)

#### 1. Model Selection & Comparison
- **Systematic K Selection:** Tests K=3 to K=8
- **Multiple Metrics:** Silhouette, Davies-Bouldin, Calinski-Harabasz, Inertia
- **Visual Comparison:** 4-panel comparison chart
- **Optimal Selection:** Automatic best K identification

#### 2. Clustering Stability Analysis
- **Multiple Runs:** 10 independent clustering runs
- **Similarity Metrics:** Adjusted Rand Index (ARI), Normalized Mutual Information (NMI)
- **Statistical Summary:** Mean, std, min, max
- **Stability Rating:** High/Moderate/Low classification

#### 3. Real Data Integration
- **Yahoo Finance:** Download real stock data via yfinance
- **Batch Download:** Multiple stocks at once
- **Configurable:** Any ticker, any date range
- **Error Handling:** Robust validation and reporting

#### 4. Statistical Validation
- **Stationarity Tests:** Augmented Dickey-Fuller (ADF) test
- **Distribution Analysis:** Comprehensive feature statistics
- **Normality Testing:** Shapiro-Wilk test
- **Data Quality:** Missing values, infinites, duplicates

#### 5. Experiment Tracking
- **Unique IDs:** MD5-based experiment identification
- **Full Logging:** Parameters, metrics, metadata
- **Dual Storage:** JSONL log + CSV summary
- **Query Tools:** Retrieve, compare, find best experiments

#### 6. Model Versioning
- **Version Tags:** Timestamp-based versioning
- **Artifact Management:** Model, scaler, features, metrics
- **Registry:** Central version tracking
- **Operations:** Save, load, compare, rollback

#### 7. Regime Interpretation
- **Automatic Labeling:** Rule-based regime naming
- **Characteristics:** Statistical summaries per regime
- **Natural Language:** Business-friendly descriptions
- **Insights:** Actionable market behavior explanations

### 📊 Core Features

#### 1. Professional Data Pipeline
- **Raw Data:** 10 major stocks, 10 years, 36,500 data points
- **Processed Data:** 36,010 rows with 20 engineered features
- **Proper Separation:** Raw/Processed/Features directories
- **Data Validation:** Comprehensive quality checks

#### 2. Feature Engineering (20 Features)
- **Returns:** Log returns, simple returns
- **Moving Averages:** 10, 30, 50-day MAs
- **Volatility:** 10, 30-day rolling standard deviation
- **Momentum:** 5, 10-day momentum indicators
- **Relative Position:** Price/MA ratios
- **Volume:** Volume moving averages and ratios
- **Range:** High-low range indicators
- **Trend Signals:** MA crossover signals

#### 3. Unsupervised ML (K-Means Clustering)
- **Algorithm:** K-Means with optimal K selection
- **Features Used:** 7 carefully selected features
- **Evaluation:** Multiple quality metrics
- **Interpretation:** Interpretable regime labels
- **Persistence:** Models saved with versioning

#### 4. Premium Dark UI
- **Design:** Bloomberg-inspired professional interface
- **Effects:** Glassmorphism, subtle animations
- **Responsive:** Mobile-friendly design
- **Components:** KPI cards, chart cards, regime table, methodology panel

#### 5. Professional Engineering
- **Configuration Management:** Centralized config.py
- **Logging:** Event and experiment tracking
- **Caching:** LRU cache for performance
- **Async Processing:** Non-blocking chart generation
- **Error Handling:** Comprehensive validation
- **Testing:** 18 unit tests (100% pass rate)

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Prajwal0422/ai-financial-time-series-learning.git
cd ai-financial-time-series-learning
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Basic Usage (Synthetic Data)

3. **Generate synthetic data**
```bash
python scripts/generate_realistic_data.py
```

4. **Process features**
```bash
python pipeline.py
```

5. **Train model (basic)**
```bash
python train_model.py
```

6. **Run application**
```bash
python app.py
```

7. **Open browser**
```
http://127.0.0.1:5000
```

### Advanced Usage (Real Data + Full Pipeline)

3. **Download real stock data**
```bash
python scripts/download_yahoo_data.py
```

4. **Process features**
```bash
python pipeline.py
```

5. **Run advanced training pipeline**
```bash
python train_model_advanced.py
```
This will:
- Perform statistical validation
- Compare K=3 to K=8
- Select optimal K
- Analyze stability
- Generate regime insights
- Version the model
- Track the experiment

6. **Run tests**
```bash
python -m pytest tests/ -v
```

7. **Start application**
```bash
python app.py
```

### Quick Commands

```bash
# View experiment history
python -c "from analysis.experiment_tracker import ExperimentTracker; ExperimentTracker().print_summary()"

# View model versions
python -c "from analysis.model_versioning import ModelVersionManager; ModelVersionManager().print_registry()"

# Run all tests
python -m pytest tests/ -v

# Check model metrics
python -c "import joblib; print(joblib.load('models/metrics.pkl'))"
```

---

## 📁 Project Structure

```
ai-financial-time-series-learning/
│
├── app.py                          # Flask application entry point
├── config.py                       # Centralized configuration
├── pipeline.py                     # Feature engineering pipeline
├── train_model.py                  # Model training script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── analysis/                       # Core analysis modules
│   ├── data_loader.py             # Data loading and management
│   ├── features.py                # Feature engineering (ENHANCED)
│   ├── returns.py                 # Return calculations
│   ├── clustering.py              # K-Means clustering
│   ├── regime_labels.py           # Regime interpretation
│   ├── trends.py                  # Trend detection
│   ├── regimes.py                 # Volatility regimes
│   ├── charts.py                  # Visualization
│   ├── summary.py                 # Statistical summaries
│   ├── validation.py              # Data validation (NEW)
│   ├── logger.py                  # Logging utilities
│   └── async_tasks.py             # Async processing
│
├── data/                          # Data storage
│   ├── raw/                       # Original datasets (36,500 rows)
│   ├── processed/                 # Engineered features (36,010 rows)
│   ├── features/                  # Reserved for feature storage
│   └── README.md                  # Data documentation
│
├── models/                        # Trained models
│   ├── kmeans.pkl                # K-Means model
│   ├── scaler.pkl                # StandardScaler
│   ├── metrics.pkl               # Evaluation metrics
│   └── features.pkl              # Feature names
│
├── scripts/                       # Utility scripts
│   ├── generate_realistic_data.py # Data generation
│   └── download_data.py          # Yahoo Finance downloader
│
├── templates/                     # HTML templates
│   ├── index.html                # Landing page (Premium dark)
│   └── dashboard.html            # Dashboard (Premium dark)
│
├── static/                        # Static assets
│   ├── css/
│   │   ├── dark-theme.css        # Premium dark theme
│   │   ├── design-system.css     # Design system
│   │   └── layout.css            # Layout styles
│   ├── js/
│   │   └── effects.js            # Premium interactions
│   └── charts/                   # Generated charts
│
├── tests/                         # Test suite (NEW)
│   ├── __init__.py
│   └── test_features.py          # Feature engineering tests
│
└── api/                           # API endpoints
    └── analysis_api.py           # REST API
```

---

## 🤖 Machine Learning Methodology

### Unsupervised Learning: Why K-Means?

**Problem:** Financial markets don't come with labels. We don't know in advance what constitutes a "regime."

**Solution:** K-Means clustering discovers natural groupings in the data based on behavioral similarity.

**Features Used for Clustering:**
1. `Log_Return` - Direction and magnitude of price movement
2. `Volatility_10` - Short-term risk measure
3. `Volatility_30` - Long-term risk measure
4. `Momentum_5` - Recent price momentum
5. `Price_to_MA10` - Position relative to short-term trend
6. `Price_to_MA30` - Position relative to long-term trend
7. `HL_Range` - Intraday volatility

**Why These Features?**
- Capture different aspects of market behavior
- Low correlation with each other
- Interpretable and explainable
- Stable across different market conditions

### Model Evaluation

**Silhouette Score:** 0.1832
- Range: -1 to 1 (higher is better)
- Interpretation: Moderate cluster separation
- Indicates distinct but overlapping regimes

**Davies-Bouldin Index:** 1.5266
- Lower is better
- Interpretation: Reasonable clustering quality

**Cluster Distribution:**
- Cluster 0: 42.75% (Largest - likely normal market)
- Cluster 1: 16.54%
- Cluster 2: 11.59% (Smallest - likely extreme events)
- Cluster 3: 29.12%

### Regime Interpretation

Clusters are mapped to human-readable labels:

| Regime | Characteristics | Interpretation |
|--------|----------------|----------------|
| **Stable Growth** | Positive returns, low volatility | Healthy uptrend |
| **Volatile Growth** | Positive returns, high volatility | Risky uptrend |
| **Stable Decline** | Negative returns, low volatility | Controlled downtrend |
| **High Risk** | Negative returns, high volatility | Market stress |

---

## 📈 Feature Engineering Details

### Returns
- **Log Returns:** `ln(P_t / P_{t-1})` - Time-additive, preferred in finance
- **Simple Returns:** `(P_t - P_{t-1}) / P_{t-1}` - Intuitive percentage change

### Volatility
- **Rolling Standard Deviation:** Measures price fluctuation magnitude
- **Volatility Clustering:** Periods of high volatility tend to cluster together

### Momentum
- **Rate of Change:** `P_t - P_{t-n}` - Captures trend strength

### Moving Averages
- **Trend Identification:** Smooth price action to reveal structural trends
- **Support/Resistance:** Often act as dynamic support/resistance levels

---

## 🔧 Configuration

All parameters are centralized in `config.py`:

```python
# Data paths
DATA_DIR = "data"
CHARTS_DIR = "static/charts"

# Moving average windows
SHORT_MA_WINDOW = 3
LONG_MA_WINDOW = 5

# Rolling statistics windows
VOLATILITY_WINDOW = 3
RETURN_WINDOW = 3

# Machine learning parameters
N_CLUSTERS = 3
RANDOM_STATE = 42

# Display settings
TABLE_ROWS = 10
```

**Benefits:**
- No magic numbers in code
- Easy experimentation
- Reproducible results
- Clear parameter documentation

---

## 🧪 Testing

Run the test suite:

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_features.py -v

# Run with coverage
pytest tests/ --cov=analysis --cov-report=html
```

---

## 📊 Data Quality

### Data Validation
- **Schema Validation:** Ensures required columns exist
- **Type Checking:** Validates data types
- **Range Validation:** Checks for reasonable values
- **Relationship Validation:** Verifies OHLC relationships
- **Quality Reports:** Generates comprehensive quality metrics

### Data Organization
- **Raw Data:** Never modified, preserved as-is
- **Processed Data:** Feature-engineered, ready for ML
- **Features:** Reserved for extracted feature storage

---

## 🎨 UI/UX Design

### Premium Dark Theme
- **Inspiration:** Bloomberg Terminal, Stripe dashboards
- **Color Palette:** Deep charcoal (#0f172a), teal accent (#06b6d4)
- **Effects:** Glassmorphism, subtle glows, smooth animations
- **Typography:** Inter font family for readability

### Components
- **KPI Cards:** Statistical summary with hover effects
- **Chart Cards:** Visualizations with dark frames
- **Regime Table:** Cluster performance summary
- **Methodology Panel:** Transparent explanation of approach

---

## ⚠️ Important Disclaimers

### Educational Purpose Only
This application is designed for:
- Learning data science and ML concepts
- Portfolio demonstration
- Understanding market behavior analysis
- Exploring unsupervised learning applications

### Not for Trading
This application is NOT:
- A trading system
- Investment advice
- A prediction tool
- Guaranteed to be accurate

### Risk Warning
- Financial markets involve risk
- Past performance ≠ future results
- Consult qualified professionals before investing
- Use at your own risk

---

## 🎓 Learning Outcomes

This project demonstrates:

**Data Science Skills:**
- Time-series analysis
- Feature engineering
- Unsupervised machine learning
- Statistical analysis
- Data visualization

**Engineering Skills:**
- Clean code architecture
- Modular design
- Configuration management
- Error handling
- Testing practices
- Documentation

**ML Engineering:**
- Model training pipelines
- Model persistence
- Evaluation metrics
- Reproducibility
- Scalability considerations

---

## 🗺️ Roadmap

- [x] Time-series feature engineering
- [x] Volatility & trend analysis
- [x] Unsupervised regime discovery
- [x] Configuration management
- [x] Data validation pipeline
- [x] Experiment logging
- [x] Premium dark UI
- [x] Model persistence
- [x] Testing framework
- [ ] API documentation (Swagger)
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] MLflow integration
- [ ] Cross-validation
- [ ] Hyperparameter tuning

---

## 📝 License

This project is for educational purposes only. MIT License.

---

## 👤 Author

**Prajwal Y Jain**  
Portfolio project demonstrating professional ML engineering practices

---

## 🙏 Acknowledgments

- Inspired by professional analytical platforms
- Built with industry-standard tools and practices
- Designed for educational and portfolio purposes

---

**Last Updated:** February 16, 2026  
**Version:** 2.0.0  
**Status:** Production-Ready Portfolio Project


---

## 🆕 What's New in v3.0 (Professional ML Engineering Upgrade)

### Advanced ML Modules

#### `analysis/model_selection.py`
Systematic model comparison and selection:
- Evaluates K=3 to K=8 with multiple metrics
- Generates comparison visualizations
- Automatic optimal K selection
- Exports results to JSON

#### `analysis/stability.py`
Clustering stability analysis:
- Runs clustering 10 times with different seeds
- Computes ARI and NMI similarity metrics
- Statistical summary (mean ± std)
- Stability classification

#### `analysis/statistical_validation.py`
Statistical rigor and validation:
- ADF stationarity tests
- Feature distribution analysis
- Normality testing (Shapiro-Wilk)
- Data quality checks

#### `analysis/experiment_tracker.py`
Full experiment tracking:
- Unique experiment IDs
- Parameter and metric logging
- JSONL + CSV dual storage
- Query and comparison tools

#### `analysis/model_versioning.py`
Enterprise-grade model versioning:
- Timestamp-based version tags
- Artifact management (model, scaler, features, metrics)
- Version registry
- Load, compare, rollback operations

#### `analysis/regime_insights.py`
Interpretable regime analysis:
- Automatic regime labeling
- Statistical characterization
- Natural language descriptions
- Business-friendly insights

#### `scripts/download_yahoo_data.py`
Real data integration:
- Yahoo Finance data download
- Batch processing for multiple stocks
- Configurable date ranges
- Error handling and validation

#### `train_model_advanced.py`
Complete professional ML pipeline:
- 9-step comprehensive workflow
- Statistical validation → Model selection → Stability analysis
- Regime insights → Versioning → Experiment tracking
- Full reproducibility

### Usage Examples

**Download Real Data:**
```python
from scripts.download_yahoo_data import download_multiple_stocks

tickers = ['AAPL', 'MSFT', 'GOOGL']
results = download_multiple_stocks(tickers, start_date='2020-01-01')
```

**Track Experiments:**
```python
from analysis.experiment_tracker import ExperimentTracker

tracker = ExperimentTracker()
exp_id = tracker.log_experiment(
    experiment_name="KMeans_K4_7features",
    parameters={'n_clusters': 4, 'n_features': 7},
    metrics={'silhouette': 0.1686, 'ari': 0.8234}
)
```

**Version Models:**
```python
from analysis.model_versioning import ModelVersionManager

manager = ModelVersionManager()
version = manager.save_model(
    model=kmeans,
    scaler=scaler,
    features=feature_list,
    metrics=metrics_dict,
    description="Optimal K=4 selected via comparison"
)
```

**Get Regime Insights:**
```python
from analysis.regime_insights import get_regime_interpretation

interpretation = get_regime_interpretation(regime_id=0)
print(f"{interpretation['label']}: {interpretation['description']}")
# Output: "Stable Growth: Positive returns with low volatility"
```

### New Artifacts Generated

```
models/
├── versions/                    # Model versions
│   └── v_20260218_143022/      # Timestamped version
│       ├── model.pkl
│       ├── scaler.pkl
│       ├── features.pkl
│       ├── metrics.pkl
│       └── metadata.json
├── model_registry.json          # Version registry
├── model_comparison.json        # K comparison results
├── stability_metrics.json       # Stability analysis
├── validation_report.json       # Statistical validation
└── regime_insights.json         # Regime interpretations

experiments/
├── experiment_log.jsonl         # Detailed experiment log
└── experiments_summary.csv      # Tabular summary

static/charts/
└── model_comparison.png         # K comparison visualization
```

### Documentation

See [PROFESSIONAL_UPGRADES.md](PROFESSIONAL_UPGRADES.md) for complete details on:
- Implementation details for each module
- Professional ML practices demonstrated
- Before/after comparison
- Interview talking points
- Technical depth analysis

---

## 🎓 Skills Demonstrated

### Machine Learning
- ✅ Unsupervised learning (K-Means clustering)
- ✅ Hyperparameter selection (systematic K comparison)
- ✅ Model evaluation (multiple metrics)
- ✅ Stability analysis (ARI, NMI)
- ✅ Feature engineering (20 features)
- ✅ Feature selection (7 ML features)
- ✅ Model persistence and versioning

### Statistics
- ✅ Time-series analysis
- ✅ Stationarity testing (ADF)
- ✅ Distribution analysis
- ✅ Normality testing (Shapiro-Wilk)
- ✅ Similarity metrics (ARI, NMI)
- ✅ Quality metrics (Silhouette, Davies-Bouldin)

### Software Engineering
- ✅ Modular architecture (25+ modules)
- ✅ Configuration management
- ✅ Error handling and validation
- ✅ Logging and monitoring
- ✅ Unit testing (18 tests, 100% pass)
- ✅ Documentation (comprehensive)
- ✅ Version control (Git)

### Data Engineering
- ✅ Data pipeline design
- ✅ ETL processes (raw → processed → features)
- ✅ Data quality validation
- ✅ Real data integration (Yahoo Finance)
- ✅ Efficient data processing (pandas)

### MLOps
- ✅ Experiment tracking
- ✅ Model versioning
- ✅ Artifact management
- ✅ Reproducibility (random seeds, logging)
- ✅ Model registry pattern

### Full-Stack Development
- ✅ Backend (Flask, Python)
- ✅ Frontend (HTML, CSS, JavaScript)
- ✅ API design (RESTful endpoints)
- ✅ UI/UX (Bloomberg-inspired design)
- ✅ Responsive design

---

## 📈 Project Evolution

### v1.0 - Initial Implementation
- Basic Flask application
- Simple data loading
- K-Means clustering (hardcoded K=3)
- Basic dashboard

### v2.0 - Professional Polish
- Premium dark theme UI
- 20 feature engineering functions
- Comprehensive testing (18 tests)
- Professional documentation
- Model persistence

### v3.0 - ML Engineering Upgrade (Current)
- ✅ Model selection (K=3 to K=8)
- ✅ Stability analysis
- ✅ Real data integration
- ✅ Statistical validation
- ✅ Experiment tracking
- ✅ Model versioning
- ✅ Regime insights
- ✅ Advanced training pipeline

---

## 🏆 Portfolio Highlights

This project demonstrates skills suitable for:

**ML Engineer Roles:**
- Model selection and evaluation
- Stability analysis
- Experiment tracking
- Model versioning
- Production-ready pipelines

**Data Scientist Roles:**
- Statistical validation
- Feature engineering
- Unsupervised learning
- Interpretable insights
- Research methodology

**Quantitative Analyst Roles:**
- Financial time-series analysis
- Regime detection
- Statistical rigor
- Real data integration
- Risk-aware design

**Full-Stack ML Roles:**
- End-to-end ML pipeline
- Backend + Frontend
- API design
- Professional UI/UX
- Comprehensive testing

---

## 📚 Additional Documentation

- [PROFESSIONAL_UPGRADES.md](PROFESSIONAL_UPGRADES.md) - Complete v3.0 upgrade details
- [PROJECT_COMPLETE_SUMMARY.md](PROJECT_COMPLETE_SUMMARY.md) - Comprehensive project summary
- [PROFESSIONAL_ML_PIPELINE_SUMMARY.md](PROFESSIONAL_ML_PIPELINE_SUMMARY.md) - ML pipeline details
- [PREMIUM_DARK_THEME_SUMMARY.md](PREMIUM_DARK_THEME_SUMMARY.md) - UI design documentation
- [DATA_SUMMARY.md](DATA_SUMMARY.md) - Data structure documentation

---

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome! Feel free to:
- Open issues for bugs or suggestions
- Submit pull requests for improvements
- Star the repository if you find it useful

---

## ⚠️ Disclaimer

**IMPORTANT:** This project is for educational and research purposes only.

- This is NOT financial advice
- This is NOT a trading system
- This does NOT predict future prices
- Past performance does NOT guarantee future results
- Always consult qualified financial professionals
- Use at your own risk

The author assumes no responsibility for any financial decisions made based on this software.

---

## 📞 Contact

**Repository:** https://github.com/Prajwal0422/ai-financial-time-series-learning  
**Author:** Prajwal  
**Version:** 3.0.0  
**Status:** ✅ Production Ready - Mid-Level ML Engineering

---

## 📊 Project Statistics

- **Total Files:** 100+
- **Python Modules:** 32
- **Lines of Code:** 6,500+
- **Test Cases:** 18 (100% pass rate)
- **Documentation Files:** 9
- **Features Engineered:** 20
- **ML Features Used:** 7
- **Data Points:** 36,500 (raw) → 36,010 (processed)
- **Stocks Analyzed:** 10
- **Time Period:** 10 years
- **Model Versions:** Tracked with registry
- **Experiments:** Logged with full metadata

---

**Last Updated:** February 18, 2026  
**License:** MIT  
**Status:** ✅ PRODUCTION READY - MID-LEVEL ML ENGINEERING

---

*Built with ❤️ for learning, research, and professional development*
