# Real Historical Stock Data

This directory contains real historical stock data for training the ML pipeline.

## Data Format

Each CSV file should contain OHLCV (Open, High, Low, Close, Volume) data:

```csv
Date,Open,High,Low,Close,Volume
2020-01-02,300.35,302.50,299.00,301.25,1234567
2020-01-03,301.50,305.00,301.00,304.75,1456789
...
```

## Required Columns

- **Date**: Trading date (YYYY-MM-DD format)
- **Open**: Opening price
- **High**: Highest price of the day
- **Low**: Lowest price of the day
- **Close**: Closing price
- **Volume**: Trading volume

## File Naming

Name files after the ticker symbol:
- `AAPL.csv` - Apple Inc.
- `MSFT.csv` - Microsoft Corporation
- `AMZN.csv` - Amazon.com Inc.
- etc.

## Data Sources

You can download real data using:

1. **Yahoo Finance Script** (included):
   ```bash
   python scripts/download_market_data.py --mode all
   ```

2. **Manual Download**:
   - Yahoo Finance: https://finance.yahoo.com
   - Alpha Vantage: https://www.alphavantage.co
   - Quandl: https://www.quandl.com

3. **yfinance Library**:
   ```python
   import yfinance as yf
   df = yf.download("AAPL MSFT AMZN", start="2000-01-01", group_by="ticker")
   ```

## Data Quality

The training pipeline will:
- ✓ Validate schema (check for required columns)
- ✓ Parse dates properly
- ✓ Sort by date
- ✓ Drop rows with missing critical values
- ✓ Handle NaN values from feature engineering

## Usage

Once you have CSV files in this directory, run:

```bash
python train_real_model.py
```

The pipeline will:
1. Load all CSV files
2. Validate data format
3. Engineer features
4. Train clustering models
5. Save versioned models
6. Log experiments

## Example Data Structure

```
data/real/
├── AAPL.csv      (Apple, 5000 rows)
├── MSFT.csv      (Microsoft, 5000 rows)
├── AMZN.csv      (Amazon, 5000 rows)
├── GOOGL.csv     (Google, 5000 rows)
├── META.csv      (Meta, 5000 rows)
├── TSLA.csv      (Tesla, 3000 rows)
├── NVDA.csv      (NVIDIA, 4000 rows)
├── JPM.csv       (JPMorgan, 5000 rows)
├── V.csv         (Visa, 4000 rows)
└── WMT.csv       (Walmart, 5000 rows)
```

Total: ~45,000 rows across 10 stocks

## Scalability

The pipeline handles:
- **Small**: 10k - 100k rows (KMeans)
- **Medium**: 100k - 500k rows (MiniBatchKMeans)
- **Large**: 500k - 1M+ rows (MiniBatchKMeans with optimizations)

## Notes

- Files are processed independently then combined
- Each ticker is feature-engineered separately (no cross-contamination)
- Missing values are handled gracefully
- Invalid files are skipped with warnings

---

**Ready to train?** Run `python train_real_model.py`
