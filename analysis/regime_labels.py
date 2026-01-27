def interpret_regimes(df):
    """
    Map ML cluster labels to human-readable regime interpretations.
    
    This transforms raw cluster numbers into actionable insights
    by analyzing the behavioral characteristics of each regime.
    """
    summary = {}
    
    for r in sorted(df["Regime"].dropna().unique()):
        subset = df[df["Regime"] == r]
        
        avg_return = subset["Log_Return"].mean()
        avg_vol = subset["Rolling_Volatility"].mean()
        
        # Interpret regime based on return and volatility characteristics
        if avg_return > 0 and avg_vol < df["Rolling_Volatility"].mean():
            label = "Stable Growth Regime"
        elif avg_return > 0 and avg_vol >= df["Rolling_Volatility"].mean():
            label = "Volatile Growth Regime"
        elif avg_return <= 0 and avg_vol < df["Rolling_Volatility"].mean():
            label = "Stable Decline Regime"
        else:
            label = "High Risk / Uncertain Regime"
        
        summary[int(r)] = {
            "label": label,
            "avg_return": round(avg_return * 100, 2),
            "avg_volatility": round(avg_vol * 100, 2)
        }
    
    return summary
