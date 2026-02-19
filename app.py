from flask import Flask, render_template, request, jsonify
from analysis.data_loader import load_stock_data, get_available_datasets
from analysis.summary import get_stock_summary
from analysis.features import build_features
from analysis.trends import detect_trend_advanced
from analysis.regimes import detect_volatility_regime
from analysis.clustering import cluster_market_regimes
from analysis.charts import generate_charts
from analysis.regime_labels import interpret_regimes
from api.analysis_api import analysis_api
from api.realtime_api import realtime_bp  # NEW: Real-time API
from analysis.async_tasks import run_async
from analysis.logger import log_event, log_experiment
from config import DATA_DIR, TABLE_ROWS, N_CLUSTERS
import os
from functools import lru_cache
import time

app = Flask(__name__)
app.register_blueprint(analysis_api, url_prefix="/api")
app.register_blueprint(realtime_bp)  # NEW: Register real-time blueprint

# Performance optimization: Cache dataset lists
@lru_cache(maxsize=32)
def get_cached_datasets():
    """Cache available datasets to avoid repeated filesystem calls"""
    return get_available_datasets()

# Performance optimization: Cache processed data
_data_cache = {}

def get_cached_data(dataset):
    """Cache processed data to avoid repeated computations"""
    current_time = time.time()
    
    # Check if data is cached and not too old (5 minutes)
    if dataset in _data_cache:
        cached_data, timestamp = _data_cache[dataset]
        if current_time - timestamp < 300:  # 5 minutes cache
            return cached_data
    
    # Process and cache data
    csv_path = os.path.join(DATA_DIR, dataset)
    df = load_stock_data(csv_path)
    df = build_features(df)
    df = cluster_market_regimes(df)
    
    _data_cache[dataset] = (df, current_time)
    return df

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    start_time = time.time()
    
    # Get selected dataset from query parameter, default to stock_1.csv
    dataset = request.args.get("dataset", "stock_1.csv")
    
    # Validate dataset parameter
    if not dataset.endswith('.csv'):
        log_event(f"Invalid dataset format: {dataset}")
        return "Invalid dataset format. Must be a CSV file.", 400
    
    # Get cached list of available datasets
    available_datasets = get_cached_datasets()
    
    # Check if dataset exists
    if dataset not in available_datasets:
        log_event(f"Dataset not found: {dataset}")
        return f"Dataset '{dataset}' not found. Available datasets: {', '.join(available_datasets)}", 404
    
    try:
        # Use cached data processing
        df = get_cached_data(dataset)
        
        # Run heavy chart generation asynchronously to keep UI responsive
        run_async(generate_charts, df)
        
        # Calculate metrics (optimized with vectorized operations)
        summary = get_stock_summary(df)
        trend = detect_trend_advanced(df)
        volatility_regime = detect_volatility_regime(df)
        regime_summary = interpret_regimes(df)
        
        # Vectorized calculations for latest values
        latest_simple_return = round(df["Simple_Return"].iloc[-1] * 100, 2)
        latest_log_return = round(df["Log_Return"].iloc[-1] * 100, 2)
        latest_volatility = round(df["Rolling_Volatility"].iloc[-1] * 100, 2)
        
        # Optimized table data preparation
        table_data = (df.tail(TABLE_ROWS)[["Date", "Close", "Simple_Return", "Rolling_Volatility"]]
                      .copy()
                      .assign(Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d"))
                      .assign(Simple_Return=lambda x: (x["Simple_Return"] * 100).round(2))
                      .assign(Rolling_Volatility=lambda x: (x["Rolling_Volatility"] * 100).round(2))
                      .to_dict("records"))
        
        # Log performance metrics
        processing_time = time.time() - start_time
        log_event(f"Dashboard loaded with dataset: {dataset} in {processing_time:.2f}s")
        
        return render_template(
            "dashboard.html",
            summary=summary,
            trend=trend,
            simple_return=latest_simple_return,
            log_return=latest_log_return,
            volatility=latest_volatility,
            volatility_regime=volatility_regime,
            regime_summary=regime_summary,
            table_data=table_data,
            available_datasets=available_datasets,
            current_dataset=dataset
        )
    
    except FileNotFoundError as e:
        log_event(f"Model not found error: {str(e)}")
        return f"Model files not found. Please run 'python train_model.py' first. Error: {str(e)}", 500
    
    except KeyError as e:
        log_event(f"Missing feature error: {str(e)}")
        return f"Missing required feature: {str(e)}. Please regenerate processed data with 'python pipeline.py'", 500
    
    except Exception as e:
        log_event(f"Dashboard error: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route("/api/chart-data")
def chart_data():
    start_time = time.time()
    dataset = request.args.get("dataset", "stock_1.csv")
    
    # Validate dataset parameter
    if not dataset.endswith('.csv'):
        return jsonify({"error": "Invalid dataset format"}), 400
    
    try:
        # Use cached data for better performance
        df = get_cached_data(dataset)
        
        # Vectorized operations for better performance
        payload = {
            "dates": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
            "close": df["Close"].tolist(),
            "ma_short": df["Close"].rolling(3).mean().fillna(0).tolist(),
            "ma_long": df["Close"].rolling(5).mean().fillna(0).tolist(),
            "returns": (df["Simple_Return"] * 100).fillna(0).tolist(),
            "volatility": (df["Rolling_Volatility"] * 100).fillna(0).tolist(),
            "processing_time": time.time() - start_time
        }
        return jsonify(payload)
    
    except FileNotFoundError as e:
        return jsonify({"error": f"Dataset not found: {dataset}"}), 404
    
    except Exception as e:
        log_event(f"Chart data error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Performance monitoring endpoint
@app.route("/api/performance")
def performance_stats():
    """Return performance statistics for monitoring"""
    return jsonify({
        "cache_size": len(_data_cache),
        "cached_datasets": list(_data_cache.keys()),
        "available_datasets": get_cached_datasets()
    })

if __name__ == "__main__":
    log_event("Flask application started with performance optimizations")
    app.run(debug=True)


# NEW: Real-Time Dashboard Route
@app.route("/realtime")
def realtime_dashboard():
    """Real-time market data dashboard"""
    log_event("Real-time dashboard accessed")
    return render_template("realtime.html")
