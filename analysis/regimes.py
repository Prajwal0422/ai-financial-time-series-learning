def detect_volatility_regime(df):
    df = df.copy()
    
    recent_vol = df["Rolling_Volatility"].iloc[-1]
    avg_vol = df["Rolling_Volatility"].mean()
    
    if recent_vol > avg_vol:
        return "High Volatility Regime"
    else:
        return "Low Volatility Regime"
