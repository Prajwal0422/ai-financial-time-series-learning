import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
from config import CHARTS_DIR

def generate_charts(df):
    """
    Generate professional analytical charts for the dashboard.
    This creates the visual evidence for the pattern recognition system.
    """
    os.makedirs(CHARTS_DIR, exist_ok=True)
    
    # 1. Price + Moving Averages
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Close"], label="Close Price", color="#2c3e50", linewidth=1.5, alpha=0.8)
    plt.plot(df["Date"], df["Close"].rolling(3).mean(), label="3-Day SMA", color="#3498db", linestyle="--")
    plt.plot(df["Date"], df["Close"].rolling(5).mean(), label="5-Day SMA", color="#e67e22", linestyle="--")
    plt.title("Price & Trend Analysis (Moving Averages)", fontsize=14, pad=15)
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "price_ma.png"), dpi=100)
    plt.close()

    # 2. Returns Analysis
    plt.figure(figsize=(12, 4))
    plt.bar(df["Date"], df["Simple_Return"] * 100, color="#16a085", alpha=0.7)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Day-over-Day Returns (%)", fontsize=14, pad=15)
    plt.ylabel("Return (%)")
    plt.grid(True, alpha=0.2, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "returns.png"), dpi=100)
    plt.close()

    # 3. Volatility Analysis
    plt.figure(figsize=(12, 4))
    plt.plot(df["Date"], df["Rolling_Volatility"] * 100, color="#c0392b", linewidth=2)
    plt.fill_between(df["Date"], df["Rolling_Volatility"] * 100, color="#c0392b", alpha=0.1)
    plt.title("Market Volatility (Rolling Std Dev)", fontsize=14, pad=15)
    plt.ylabel("Volatility (%)")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "volatility.png"), dpi=100)
    plt.close()

    # 4. Market Regimes (Clustered Analysis)
    plt.figure(figsize=(12, 6))
    for r in sorted(df["Regime"].dropna().unique()):
        subset = df[df["Regime"] == r]
        plt.scatter(
            subset["Date"],
            subset["Close"],
            label=f"Regime {int(r)}",
            s=60,
            alpha=0.8,
            edgecolors='white',
            linewidths=0.5
        )
    plt.title("Detected Market Regimes (Behavioral Clusters)", fontsize=14, pad=15)
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "regimes.png"), dpi=100)
    plt.close()
