# Financial Time-Series Pattern Analysis

A professional web application for analyzing stock market time-series data using data science techniques. This project demonstrates exploratory data analysis, statistical metrics, and unsupervised machine learning — without making predictions or trading recommendations.

## 🎯 Project Overview

This application analyzes historical stock market data to identify patterns, trends, and behavioral regimes. It is designed as an educational tool and portfolio project showcasing real-world data science skills.

**Key Features:**
- Time-series data loading and processing
- Statistical analysis (returns, volatility, trends)
- Unsupervised machine learning (market regime clustering)
- Interactive web dashboard with modern UI
- Multi-dataset support

## 🎯 Design Philosophy

This project prioritizes:
- **Interpretability over black-box prediction**: Every metric is traceable and explainable
- **Exploratory pattern discovery**: Focus on understanding historical behavior
- **Reproducible data pipelines**: Config-driven, modular architecture
- **Clear separation of concerns**: Each module has a single responsibility
- **Data validation**: Professional-grade input validation and error handling

The goal is to reflect how data science systems are designed in real-world analytical teams, 
not just academic exercises.

## 🤖 Unsupervised Learning: Market Regimes

The project uses **K-Means clustering** to group trading days into market regimes based on behavioral similarity.

### Features Used
- **Log returns** (price movement direction and magnitude)
- **Rolling volatility** (risk and uncertainty measure)

### Why Unsupervised Learning?
- No labels exist for market regimes
- Avoids prediction and future leakage
- Focuses on exploratory pattern discovery
- Reveals hidden behavioral patterns in historical data

### Interpretation
Clusters are mapped to human-readable regimes such as:
- **Stable Growth**: Positive returns with low volatility
- **Volatile Growth**: Positive returns with high volatility
- **Stable Decline**: Negative returns with low volatility
- **High-Risk / Uncertain**: Negative returns with high volatility

This demonstrates the ability to transform raw ML output into actionable insights.

## 🛠 Technology Stack

**Backend:**
- Python 3.14
- Flask (web framework)
- pandas (data processing)
- NumPy (numerical computing)
- scikit-learn (machine learning)
- matplotlib (visualization)

**Frontend:**
- HTML5
- CSS3 (modern grid layouts, gradients)
- Vanilla JavaScript (minimal, no frameworks)

## 📁 Project Structure


```
ai-financial-time-series-learning/
│
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── analysis/                   # Core data science modules
│   ├── data_loader.py         # CSV loading and dataset management
│   ├── returns.py             # Return calculations (simple & log)
│   ├── summary.py             # Statistical summaries
│   ├── trends.py              # Multi-signal trend detection
│   ├── regimes.py             # Volatility regime classification
│   ├── clustering.py          # K-Means market regime clustering
│   ├── regime_labels.py       # Regime interpretation logic
│   └── charts.py              # Matplotlib chart generation
│
├── data/                       # Sample datasets
│   ├── stock_1.csv
│   ├── stock_2.csv
│   └── README.md
│
├── templates/                  # HTML templates
│   ├── index.html             # Homepage
│   └── dashboard.html         # Main dashboard
│
└── static/                     # Static assets
    ├── css/
    │   ├── style.css          # Homepage styles
    │   └── dashboard.css      # Dashboard styles
    ├── js/
    │   └── dashboard.js       # Dashboard interactions
    └── charts/
        └── regimes.png        # Generated regime chart
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python app.py
```

4. Open your browser to:
```
http://127.0.0.1:5000
```

## 📊 Features Explained

### Statistical Analysis
- **Simple Returns**: Day-over-day percentage change
- **Log Returns**: Logarithmic returns (additive, preferred in finance)
- **Rolling Volatility**: 3-day standard deviation of returns
- **Moving Averages**: Short-term (3-day) and long-term (5-day)

### Trend Detection
Multi-signal approach combining:
1. Moving average crossover
2. Recent returns direction
3. Volatility regime analysis

### Market Regimes
Unsupervised clustering identifies behavioral patterns without labels.

## ⚠️ Important Disclaimers

- **No Predictions**: This application performs descriptive analysis only
- **No Trading Advice**: Not intended for actual trading decisions
- **Educational Purpose**: Designed for learning and portfolio demonstration
- **Sample Data**: Uses simulated data for demonstration

## 🎓 Learning Outcomes

This project demonstrates:
- Time-series data processing
- Feature engineering (returns, volatility)
- Unsupervised machine learning (K-Means)
- Data visualization
- Full-stack web development
- Clean code architecture
- Professional documentation

## 📝 License

This project is for educational purposes only.

## 👤 Author

Created as a data science portfolio project demonstrating real-world analytical skills.

---

**Note**: This application does not predict future prices or provide investment advice. It is purely for educational and analytical purposes.


## 🗺 Roadmap

- [x] Time-series feature engineering
- [x] Volatility & trend analysis
- [x] Unsupervised regime discovery
- [x] Configuration management
- [x] Data validation pipeline
- [x] Experiment logging
- [ ] Cross-asset regime comparison
- [ ] Interactive visualization layer
- [ ] API endpoints for programmatic access

## 🔧 Configuration

All configurable parameters are centralized in `config.py`:
- Window sizes for moving averages and rolling statistics
- Number of clusters for regime detection
- Data paths and display settings

This allows easy experimentation without modifying core logic.

## 📊 Code Quality

This project follows professional standards:
- Functions under 30 lines
- Clear, descriptive variable names
- No magic numbers (all in config)
- Comments explain "why", not "what"
- Modular architecture with single responsibility
- Input validation and error handling

## 🧪 Experiment Tracking

The application logs key events to `experiment.log`:
- Dataset selections
- Clustering runs
- Application starts

This provides an audit trail for analysis decisions.

---

**Last Updated**: January 27, 2026
