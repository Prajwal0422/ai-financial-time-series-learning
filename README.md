# AI Financial Time-Series Pattern Analysis
### Professional Analytical ML System for Market Behavior Discovery

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A professional machine learning system for analyzing financial time-series data through unsupervised pattern discovery and statistical analysis. This is NOT a trading bot or prediction system—it's an analytical tool focused on interpretability and insight.**

---

## 🎯 Project Purpose

This application demonstrates professional ML engineering practices applied to financial time-series analysis. It identifies market behavioral regimes using unsupervised learning, calculates statistical metrics, and presents insights through a premium dark-mode dashboard.

**What This System Does:**
- ✅ Analyzes historical market behavior patterns
- ✅ Discovers market regimes through clustering
- ✅ Calculates returns, volatility, and momentum
- ✅ Visualizes patterns and trends
- ✅ Provides interpretable insights

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

### 1. Professional Data Pipeline
- **Raw Data:** 10 major stocks, 10 years, 36,500 data points
- **Processed Data:** 36,010 rows with 20 engineered features
- **Proper Separation:** Raw/Processed/Features directories
- **Data Validation:** Comprehensive quality checks

### 2. Feature Engineering (20 Features)
- **Returns:** Log returns, simple returns
- **Moving Averages:** 10, 30, 50-day MAs
- **Volatility:** 10, 30-day rolling standard deviation
- **Momentum:** 5, 10-day momentum indicators
- **Relative Position:** Price/MA ratios
- **Volume:** Volume moving averages and ratios
- **Range:** High-low range indicators
- **Trend Signals:** MA crossover signals

### 3. Unsupervised ML (K-Means Clustering)
- **Algorithm:** K-Means with 4 clusters
- **Features Used:** 7 carefully selected features
- **Evaluation:** Silhouette score (0.1832), Davies-Bouldin index (1.5266)
- **Interpretation:** Regime labels (Stable Growth, Volatile Growth, etc.)
- **Persistence:** Models saved with joblib

### 4. Premium Dark UI
- **Design:** Bloomberg-inspired professional interface
- **Effects:** Glassmorphism, subtle animations
- **Responsive:** Mobile-friendly design
- **Components:** KPI cards, chart cards, regime table, methodology panel

### 5. Professional Engineering
- **Configuration Management:** Centralized config.py
- **Logging:** Event and experiment tracking
- **Caching:** LRU cache for performance
- **Async Processing:** Non-blocking chart generation
- **Error Handling:** Comprehensive validation
- **Testing:** Unit test framework (pytest)

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

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://127.0.0.1:5000
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
