from flask import Flask, render_template, request, jsonify
from analysis.data_loader import load_stock_data, get_available_datasets
from analysis.summary import get_stock_summary
from analysis.features import build_features
from analysis.trends import detect_trend_advanced
from analysis.regimes import detect_volatility_regime
from analysis.clustering import cluster_market_regimes
from analysis.charts import generate_regime_chart
from analysis.regime_labels import interpret_regimes
from api.analysis_api import analysis_api
from analysis.async_tasks import run_async
from analysis.logger import log_event, log_experiment
from config import DATA_DIR, TABLE_ROWS, N_CLUSTERS
import os

app = Flask(__name__)
app.register_blueprint(analysis_api, url_prefix="/api")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    # Get selected dataset from query parameter, default to stock_1.csv
    dataset = request.args.get("dataset", "stock_1.csv")
    
    # Log the analysis run
    log_event(f"Dashboard loaded with dataset: {dataset}")
    
    # Get list of available datasets
    available_datasets = get_available_datasets()
    
    # Load and process data using feature pipeline
    csv_path = os.path.join(DATA_DIR, dataset)
    df = load_stock_data(csv_path)
    df = build_features(df)
    df = cluster_market_regimes(df)
    
    # Run heavy chart generation asynchronously to keep UI responsive
    run_async(generate_regime_chart, df)
    
    # Log the clustering experiment for DS tracking
    log_experiment(
        name="Market Regime Discovery",
        params=f"clusters={N_CLUSTERS}, data={dataset}",
        notes="Automated run from dashboard"
    )
    
    # Log clustering completion
    log_event(f"Clustering completed with {df['Regime'].nunique()} regimes")
    
    # Calculate metrics
    summary = get_stock_summary(df)
    trend = detect_trend_advanced(df)
    volatility_regime = detect_volatility_regime(df)
    regime_summary = interpret_regimes(df)
    
    latest_simple_return = round(df["Simple_Return"].iloc[-1] * 100, 2)
    latest_log_return = round(df["Log_Return"].iloc[-1] * 100, 2)
    latest_volatility = round(df["Rolling_Volatility"].iloc[-1] * 100, 2)
    
    # Get last N rows for table display (using config)
    table_data = df.tail(TABLE_ROWS)[["Date", "Close", "Simple_Return", "Rolling_Volatility"]].copy()
    table_data["Date"] = table_data["Date"].dt.strftime("%Y-%m-%d")
    table_data["Simple_Return"] = (table_data["Simple_Return"] * 100).round(2)
    table_data["Rolling_Volatility"] = (table_data["Rolling_Volatility"] * 100).round(2)
    table_data = table_data.to_dict("records")
    
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

@app.route("/api/chart-data")
def chart_data():
    dataset = request.args.get("dataset", "stock_1.csv")
    csv_path = os.path.join(DATA_DIR, dataset)
    df = load_stock_data(csv_path)
    df = build_features(df)
    
    payload = {
        "dates": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "close": df["Close"].tolist(),
        "ma_short": df["Close"].rolling(3).mean().fillna(None).tolist(),
        "ma_long": df["Close"].rolling(5).mean().fillna(None).tolist(),
        "returns": (df["Simple_Return"] * 100).fillna(0).tolist(),
        "volatility": (df["Rolling_Volatility"] * 100).fillna(0).tolist(),
    }
    return jsonify(payload)

if __name__ == "__main__":
    log_event("Flask application started")
    app.run(debug=True)
