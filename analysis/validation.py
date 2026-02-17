"""
Data Validation Module
Ensures data quality and integrity throughout the pipeline

Professional ML systems validate data at every stage to prevent
silent failures and ensure reproducible results.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict


class DataValidator:
    """
    Validates stock market time-series data for quality and completeness.
    
    This class implements defensive programming practices to catch
    data issues early before they propagate through the pipeline.
    """
    
    REQUIRED_COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    @staticmethod
    def validate_raw_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate raw stock data meets minimum requirements.
        
        Args:
            df: Raw dataframe to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check 1: Required columns exist
        missing_cols = set(DataValidator.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
        
        # Check 2: Sufficient data points
        if len(df) < 50:
            errors.append(f"Insufficient data: {len(df)} rows (minimum 50 required)")
        
        # Check 3: No all-null columns
        null_cols = df.columns[df.isnull().all()].tolist()
        if null_cols:
            errors.append(f"Columns with all null values: {null_cols}")
        
        # Check 4: Date column is datetime
        if 'Date' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Date']):
            errors.append("Date column must be datetime type")
        
        # Check 5: Numeric columns are numeric
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Column {col} must be numeric")
        
        # Check 6: OHLC relationships
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            invalid_ohlc = (
                (df['High'] < df['Low']) |
                (df['High'] < df['Open']) |
                (df['High'] < df['Close']) |
                (df['Low'] > df['Open']) |
                (df['Low'] > df['Close'])
            ).sum()
            
            if invalid_ohlc > 0:
                errors.append(f"Invalid OHLC relationships in {invalid_ohlc} rows")
        
        # Check 7: Positive prices
        price_cols = ['Open', 'High', 'Low', 'Close']
        for col in price_cols:
            if col in df.columns and (df[col] <= 0).any():
                errors.append(f"Non-positive values found in {col}")
        
        # Check 8: Positive volume
        if 'Volume' in df.columns and (df['Volume'] < 0).any():
            errors.append("Negative volume values found")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @staticmethod
    def validate_features(df: pd.DataFrame, required_features: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that required features exist and are valid.
        
        Args:
            df: Dataframe with engineered features
            required_features: List of feature names that must exist
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check 1: Required features exist
        missing_features = set(required_features) - set(df.columns)
        if missing_features:
            errors.append(f"Missing required features: {missing_features}")
        
        # Check 2: Features are numeric
        for feature in required_features:
            if feature in df.columns and not pd.api.types.is_numeric_dtype(df[feature]):
                errors.append(f"Feature {feature} must be numeric")
        
        # Check 3: Check for infinite values
        for feature in required_features:
            if feature in df.columns and np.isinf(df[feature]).any():
                errors.append(f"Infinite values found in {feature}")
        
        # Check 4: Excessive NaN values (>50%)
        for feature in required_features:
            if feature in df.columns:
                nan_pct = df[feature].isnull().sum() / len(df) * 100
                if nan_pct > 50:
                    errors.append(f"Feature {feature} has {nan_pct:.1f}% null values")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @staticmethod
    def get_data_quality_report(df: pd.DataFrame) -> Dict:
        """
        Generate comprehensive data quality report.
        
        Args:
            df: Dataframe to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'null_counts': df.isnull().sum().to_dict(),
            'null_percentages': (df.isnull().sum() / len(df) * 100).to_dict(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'date_range': None,
            'duplicates': df.duplicated().sum()
        }
        
        # Add date range if Date column exists
        if 'Date' in df.columns:
            report['date_range'] = {
                'start': str(df['Date'].min()),
                'end': str(df['Date'].max()),
                'days': (df['Date'].max() - df['Date'].min()).days
            }
        
        return report
    
    @staticmethod
    def check_data_drift(df1: pd.DataFrame, df2: pd.DataFrame, columns: List[str]) -> Dict:
        """
        Check for statistical drift between two datasets.
        
        Useful for monitoring data quality over time or comparing
        training data to new data.
        
        Args:
            df1: First dataframe (e.g., training data)
            df2: Second dataframe (e.g., new data)
            columns: Columns to compare
            
        Returns:
            Dictionary with drift metrics
        """
        drift_report = {}
        
        for col in columns:
            if col in df1.columns and col in df2.columns:
                drift_report[col] = {
                    'mean_diff': abs(df1[col].mean() - df2[col].mean()),
                    'std_diff': abs(df1[col].std() - df2[col].std()),
                    'min_diff': abs(df1[col].min() - df2[col].min()),
                    'max_diff': abs(df1[col].max() - df2[col].max())
                }
        
        return drift_report


def validate_and_report(df: pd.DataFrame, stage: str = "raw") -> pd.DataFrame:
    """
    Convenience function to validate data and print report.
    
    Args:
        df: Dataframe to validate
        stage: Pipeline stage name for logging
        
    Returns:
        Original dataframe (unchanged)
        
    Raises:
        ValueError: If validation fails
    """
    validator = DataValidator()
    
    # Validate
    is_valid, errors = validator.validate_raw_data(df)
    
    if not is_valid:
        error_msg = f"Data validation failed at {stage} stage:\n" + "\n".join(f"  - {e}" for e in errors)
        raise ValueError(error_msg)
    
    # Generate quality report
    report = validator.get_data_quality_report(df)
    
    print(f"\n{'='*60}")
    print(f"Data Quality Report - {stage.upper()} Stage")
    print(f"{'='*60}")
    print(f"Rows: {report['total_rows']:,}")
    print(f"Columns: {report['total_columns']}")
    print(f"Memory: {report['memory_usage_mb']:.2f} MB")
    print(f"Duplicates: {report['duplicates']}")
    
    if report['date_range']:
        print(f"Date Range: {report['date_range']['start']} to {report['date_range']['end']}")
        print(f"Days: {report['date_range']['days']}")
    
    # Show columns with high null percentages
    high_null_cols = {k: v for k, v in report['null_percentages'].items() if v > 10}
    if high_null_cols:
        print(f"\nColumns with >10% null values:")
        for col, pct in high_null_cols.items():
            print(f"  {col}: {pct:.1f}%")
    
    print(f"{'='*60}\n")
    
    return df
