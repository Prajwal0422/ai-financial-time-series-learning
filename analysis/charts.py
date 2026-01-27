import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
from config import CHARTS_DIR

def generate_regime_chart(df):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    
    plt.figure(figsize=(10, 5))
    
    # Plot each regime with different colors
    for r in sorted(df["Regime"].dropna().unique()):
        subset = df[df["Regime"] == r]
        plt.scatter(
            subset["Date"],
            subset["Close"],
            label=f"Regime {int(r)}",
            s=50,
            alpha=0.7
        )
    
    plt.title("Market Regimes (Clustered Days)", fontsize=14, fontweight='bold')
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("Close Price", fontsize=11)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "regimes.png"), dpi=100)
    plt.close()
