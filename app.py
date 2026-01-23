from flask import Flask, render_template
from analysis.data_loader import load_stock_data
from analysis.summary import get_stock_summary

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    df = load_stock_data("data/sample_stock_data.csv")
    summary = get_stock_summary(df)
    return render_template("dashboard.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
