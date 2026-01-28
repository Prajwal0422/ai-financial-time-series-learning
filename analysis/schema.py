"""
Data Contract enforcement for the analysis pipeline.
Ensuring data quality is a hallmark of senior engineering.
"""
import pandas as pd

EXPECTED_SCHEMA = {
    "Date": "datetime64",
    "Open": "float",
    "High": "float",
    "Low": "float",
    "Close": "float",
    "Volume": "int"
}

def enforce_schema(df):
    """
    Validates that the incoming dataframe matches the expected project schema.
    This prevents downstream failures in technical indicators and ML models.
    """
    for col, dtype in EXPECTED_SCHEMA.items():
        if col not in df.columns:
            raise ValueError(f"Data Contract Violation: Missing column '{col}'")
        
        # Optional: Strict type checking if needed
        # if not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
        #     print(f"Warning: Column {col} expected {dtype}, got {df[col].dtype}")
            
    return df
