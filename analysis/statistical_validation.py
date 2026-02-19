"""
Statistical Validation Module
Performs statistical tests and validation on time-series data
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from scipy import stats
import json
from pathlib import Path


def adf_stationarity_test(series, name='Series'):
    """
    Perform Augmented Dickey-Fuller test for stationarity.
    
    Args:
        series (pd.Series): Time series data
        name (str): Name of the series for reporting
        
    Returns:
        dict: Test results
    """
    # Remove NaN values
    series_clean = series.dropna()
    
    if len(series_clean) < 10:
        return {
            'name': name,
            'stationary': None,
            'error': 'Insufficient data for ADF test'
        }
    
    # Perform ADF test
    result = adfuller(series_clean, autolag='AIC')
    
    adf_stat = result[0]
    p_value = result[1]
    critical_values = result[4]
    
    # Determine stationarity (p-value < 0.05 indicates stationarity)
    is_stationary = p_value < 0.05
    
    test_results = {
        'name': name,
        'adf_statistic': float(adf_stat),
        'p_value': float(p_value),
        'critical_values': {k: float(v) for k, v in critical_values.items()},
        'stationary': bool(is_stationary),
        'interpretation': 'Stationary' if is_stationary else 'Non-stationary'
    }
    
    return test_results


def feature_distribution_summary(df, features):
    """
    Generate statistical summary of feature distributions.
    
    Args:
        df (pd.DataFrame): DataFrame with features
        features (list): List of feature names to analyze
        
    Returns:
        dict: Distribution statistics for each feature
    """
    summaries = {}
    
    for feature in features:
        if feature not in df.columns:
            continue
        
        series = df[feature].dropna()
        
        if len(series) == 0:
            continue
        
        # Calculate statistics
        summary = {
            'count': int(len(series)),
            'mean': float(series.mean()),
            'std': float(series.std()),
            'min': float(series.min()),
            'q25': float(series.quantile(0.25)),
            'median': float(series.median()),
            'q75': float(series.quantile(0.75)),
            'max': float(series.max()),
            'skewness': float(series.skew()),
            'kurtosis': float(series.kurtosis())
        }
        
        # Normality test (Shapiro-Wilk for small samples, Anderson-Darling for large)
        if len(series) < 5000:
            stat, p_value = stats.shapiro(series)
            summary['normality_test'] = 'Shapiro-Wilk'
        else:
            # Use sample for large datasets
            sample = series.sample(n=5000, random_state=42)
            stat, p_value = stats.shapiro(sample)
            summary['normality_test'] = 'Shapiro-Wilk (sampled)'
        
        summary['normality_p_value'] = float(p_value)
        summary['appears_normal'] = bool(p_value > 0.05)
        
        summaries[feature] = summary
    
    return summaries


def validate_data_quality(df):
    """
    Perform comprehensive data quality checks.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        
    Returns:
        dict: Data quality report
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': {},
        'infinite_values': {},
        'duplicate_rows': int(df.duplicated().sum()),
        'date_range': {}
    }
    
    # Check for missing values
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            report['missing_values'][col] = {
                'count': int(missing_count),
                'percentage': float(missing_count / len(df) * 100)
            }
    
    # Check for infinite values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        inf_count = np.isinf(df[col]).sum()
        if inf_count > 0:
            report['infinite_values'][col] = int(inf_count)
    
    # Check date range if Date column exists
    if 'Date' in df.columns:
        report['date_range'] = {
            'start': str(df['Date'].min()),
            'end': str(df['Date'].max()),
            'days': int((df['Date'].max() - df['Date'].min()).days)
        }
    
    return report


def run_statistical_validation(df, features_to_test=None):
    """
    Run comprehensive statistical validation on dataset.
    
    Args:
        df (pd.DataFrame): DataFrame with features
        features_to_test (list): Features to test for stationarity (default: returns and volatility)
        
    Returns:
        dict: Complete validation report
    """
    print("\nRunning Statistical Validation...")
    print("=" * 60)
    
    # Default features to test
    if features_to_test is None:
        features_to_test = ['Log_Return', 'Simple_Return', 'Volatility_10', 'Volatility_30']
    
    validation_report = {
        'data_quality': validate_data_quality(df),
        'stationarity_tests': {},
        'feature_distributions': {}
    }
    
    # Stationarity tests
    print("\n1. Stationarity Tests (ADF):")
    print("-" * 60)
    for feature in features_to_test:
        if feature in df.columns:
            result = adf_stationarity_test(df[feature], name=feature)
            validation_report['stationarity_tests'][feature] = result
            
            if result.get('stationary') is not None:
                status = "✓ Stationary" if result['stationary'] else "✗ Non-stationary"
                print(f"{feature:20s}: {status} (p={result['p_value']:.4f})")
    
    # Feature distributions
    print("\n2. Feature Distribution Summary:")
    print("-" * 60)
    all_features = [col for col in df.columns if col not in ['Date', 'Regime']]
    distributions = feature_distribution_summary(df, all_features)
    validation_report['feature_distributions'] = distributions
    
    for feature, summary in list(distributions.items())[:5]:  # Show first 5
        print(f"{feature:20s}: μ={summary['mean']:8.4f}, σ={summary['std']:8.4f}, skew={summary['skewness']:6.2f}")
    
    if len(distributions) > 5:
        print(f"... and {len(distributions) - 5} more features")
    
    # Data quality summary
    print("\n3. Data Quality:")
    print("-" * 60)
    quality = validation_report['data_quality']
    print(f"Total rows: {quality['total_rows']:,}")
    print(f"Total columns: {quality['total_columns']}")
    print(f"Duplicate rows: {quality['duplicate_rows']}")
    print(f"Missing values: {len(quality['missing_values'])} columns affected")
    print(f"Infinite values: {len(quality['infinite_values'])} columns affected")
    
    if quality['date_range']:
        print(f"Date range: {quality['date_range']['start']} to {quality['date_range']['end']}")
        print(f"Total days: {quality['date_range']['days']}")
    
    print("=" * 60)
    
    return validation_report


def save_validation_report(validation_report, output_path='models/validation_report.json'):
    """
    Save validation report to JSON file.
    
    Args:
        validation_report (dict): Validation report from run_statistical_validation
        output_path (str): Path to save JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(validation_report, f, indent=2)
    
    print(f"✓ Validation report saved to {output_file}")
