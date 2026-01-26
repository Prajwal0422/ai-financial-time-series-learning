from flask import Flask, render_template, request, jsonify
from analysis.data_loader import load_stock_data, get_available_datasets
from analysis.summary import get_stock_summary
from analysis.returns import calculate_returns
from analysis.trends import detect_trend_advanced
from analysis.regimes import detect_volatility_regime
from analysis.charts import generate_charts
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    # Get selected dataset from query parameter, default to stock_1.csv
    dataset = request.args.get("dataset", "stock_1.csv")
    
    # Get list of available datasets
    available_datasets = get_available_datasets()
    
    # Load and process data
    csv_path = os.path.join("data", dataset)
    df = load_stock_data(csv_path)
    df = calculate_returns(df)
    
    # Generate static charts
    generate_charts(df)
    
    # Calculate metrics
    summary = get_stock_summary(df)
    trend = detect_trend_advanced(df)
    volatility_regime = detect_volatility_regime(df)
    
    latest_simple_return = round(df["Simple_Return"].iloc[-1] * 100, 2)
    latest_log_return = round(df["Log_Return"].iloc[-1] * 100, 2)
    latest_volatility = round(df["Rolling_Volatility"].iloc[-1] * 100, 2)
    
    # Get last 10 rows for table display
    table_data = df.tail(10)[["Date", "Close", "Simple_Return", "Rolling_Volatility"]].copy()
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
        table_data=table_data,
        available_datasets=available_datasets,
        current_dataset=dataset
    )

@app.route("/api/chart-data")
def chart_data():
    dataset = request.args.get("dataset", "stock_1.csv")
    csv_path = os.path.join("data", dataset)
    df = load_stock_data(csv_path)
    df = calculate_returns(df)
    
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
    app.run(debug=True)
