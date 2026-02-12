# Sample Stock Data

This directory contains sample CSV files for time-series analysis.

## Dataset Structure

Each CSV file should have the following columns:
- Date: Trading date (YYYY-MM-DD format)
- Open: Opening price
- High: Highest price
- Low: Lowest price
- Close: Closing price
- Volume: Trading volume

## Available Datasets

### Original Datasets (10 days)
- `stock_1.csv`: Sample stock data (Tech sector simulation)
- `stock_2.csv`: Sample stock data (Finance sector simulation)

### Extended Datasets (50 days - Q1 2023)
- `stock_volatile_crypto.csv`: High volatility cryptocurrency-style asset with extreme price swings
- `stock_tech_growth.csv`: Steady growth technology stock with consistent upward trend
- `stock_stable_dividend.csv`: Low volatility dividend stock with gradual appreciation
- `stock_bear_market.csv`: Declining market with sustained downward pressure
- `stock_recovery_trend.csv`: Recovery pattern showing strong upward momentum

## Dataset Characteristics

| Dataset | Behavior | Volatility | Trend | Data Points |
|---------|----------|------------|-------|-------------|
| stock_1 | Mixed | Low | Neutral | 10 |
| stock_2 | Mixed | Low | Neutral | 10 |
| stock_volatile_crypto | Extreme swings | Very High | Bearish | 50 |
| stock_tech_growth | Steady growth | Low | Bullish | 50 |
| stock_stable_dividend | Gradual rise | Very Low | Bullish | 50 |
| stock_bear_market | Declining | High | Bearish | 50 |
| stock_recovery_trend | Strong recovery | Medium | Bullish | 50 |

## Dataset Versioning

- **Source**: Simulated data for educational purposes
- **Frequency**: Daily
- **Time Span**: 
  - Original: 2024-01-01 to 2024-01-10 (10 days)
  - Extended: 2023-01-03 to 2023-03-15 (50 days)
- **Last Updated**: 2026-02-12

## Usage

These datasets are for educational and demonstration purposes only.
They do not represent real trading data and should not be used for actual trading decisions.

## Adding New Datasets

To add a new dataset:
1. Ensure it follows the required column structure
2. Save as CSV in this directory
3. The application will automatically detect it
