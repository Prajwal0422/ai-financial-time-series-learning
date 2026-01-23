from flask import Flask, render_template
from analysis.data_loader import load_stock_data
from analysis.summary import get_stock_summary
from analysis.returns import calculate_returns
from analysis.trends import detect_trend_advanced

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    df = load_stock_data("data/sample_stock_data.csv")
    df = calculate_returns(df)
    
    summary = get_stock_summary(df)
    trend = detect_trend_advanced(df)
    
    latest_simple_return = round(df["Simple_Return"].iloc[-1] * 100, 2)
    latest_log_return = round(df["Log_Return"].iloc[-1] * 100, 2)
    latest_volatility = round(df["Rolling_Volatility"].iloc[-1] * 100, 2)
    
    return render_template(
        "dashboard.html",
        summary=summary,
        trend=trend,
        simple_return=latest_simple_return,
        log_return=latest_log_return,
        volatility=latest_volatility
    )

if __name__ == "__main__":
    app.run(debug=True)
