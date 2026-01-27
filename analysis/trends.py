from config import SHORT_MA_WINDOW, LONG_MA_WINDOW

def detect_trend_advanced(df):
    df = df.copy()
    
    short_ma = df["Close"].rolling(window=SHORT_MA_WINDOW).mean()
    long_ma = df["Close"].rolling(window=LONG_MA_WINDOW).mean()
    
    trend_score = 0
    
    # Signal 1: MA crossover
    if short_ma.iloc[-1] > long_ma.iloc[-1]:
        trend_score += 1
    else:
        trend_score -= 1
    
    # Signal 2: Recent returns direction
    recent_returns = df["Log_Return"].tail(3).mean()
    if recent_returns > 0:
        trend_score += 1
    else:
        trend_score -= 1
    
    # Signal 3: Volatility regime
    recent_vol = df["Rolling_Volatility"].iloc[-1]
    avg_vol = df["Rolling_Volatility"].mean()
    
    if recent_vol < avg_vol:
        trend_score += 1
    else:
        trend_score -= 1
    
    # Final decision
    if trend_score >= 2:
        return "Strong Uptrend"
    elif trend_score <= -2:
        return "Strong Downtrend"
    else:
        return "Sideways / Uncertain"
