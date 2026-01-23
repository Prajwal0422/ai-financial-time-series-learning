def get_stock_summary(df):
    summary = {
        "start_date": df["Date"].min().date(),
        "end_date": df["Date"].max().date(),
        "total_days": len(df),
        "avg_close": round(df["Close"].mean(), 2),
        "max_close": df["Close"].max(),
        "min_close": df["Close"].min()
    }
    
    return summary
