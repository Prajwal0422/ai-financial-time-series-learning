from flask import Blueprint, jsonify, request
from analysis.data_loader import load_stock_data
from analysis.features import build_features
from analysis.clustering import cluster_market_regimes
from analysis.regime_labels import interpret_regimes
import os
from config import DATA_DIR

analysis_api = Blueprint("analysis_api", __name__)

@analysis_api.route("/analyze", methods=["GET"])
def analyze():
    dataset = request.args.get("dataset", "sample_stock_data.csv")
    csv_path = os.path.join(DATA_DIR, dataset)

    df = load_stock_data(csv_path)
    df = build_features(df)
    df = cluster_market_regimes(df)

    regimes = interpret_regimes(df)

    return jsonify({
        "rows": len(df),
        "regimes": regimes
    })
