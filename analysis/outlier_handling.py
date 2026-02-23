"""
Outlier Detection and Handling for Clustering
Removes extreme values that can distort cluster formation
"""

import numpy as np
import pandas as pd
from scipy import stats


def detect_outliers_zscore(X, threshold=3.0):
    """
    Detect outliers using Z-score method.
    
    Args:
        X (np.ndarray): Feature matrix
        threshold (float): Z-score threshold (default 3.0)
        
    Returns:
        np.ndarray: Boolean mask (True = outlier)
    """
    z_scores = np.abs(stats.zscore(X, axis=0, nan_policy='omit'))
    outlier_mask = (z_scores > threshold).any(axis=1)
    return outlier_mask


def remove_extreme_percentiles(X, lower=0.5, upper=99.5):
    """
    Remove extreme percentiles from data.
    
    Args:
        X (np.ndarray): Feature matrix
        lower (float): Lower percentile to remove
        upper (float): Upper percentile to remove
        
    Returns:
        np.ndarray: Boolean mask (True = keep)
    """
    keep_mask = np.ones(X.shape[0], dtype=bool)
    
    for col_idx in range(X.shape[1]):
        col_data = X[:, col_idx]
        lower_bound = np.percentile(col_data, lower)
        upper_bound = np.percentile(col_data, upper)
        
        col_mask = (col_data >= lower_bound) & (col_data <= upper_bound)
        keep_mask &= col_mask
    
    return keep_mask



def filter_outliers(X, method='zscore', **kwargs):
    """
    Filter outliers from feature matrix.
    
    Args:
        X (np.ndarray): Feature matrix
        method (str): 'zscore' or 'percentile'
        **kwargs: Additional arguments for specific methods
        
    Returns:
        tuple: (X_filtered, keep_mask)
    """
    if method == 'zscore':
        threshold = kwargs.get('threshold', 3.0)
        outlier_mask = detect_outliers_zscore(X, threshold)
        keep_mask = ~outlier_mask
        
    elif method == 'percentile':
        lower = kwargs.get('lower', 0.5)
        upper = kwargs.get('upper', 99.5)
        keep_mask = remove_extreme_percentiles(X, lower, upper)
        
    else:
        raise ValueError(f"Unknown method: {method}")
    
    X_filtered = X[keep_mask]
    
    n_removed = np.sum(~keep_mask)
    pct_removed = (n_removed / len(X)) * 100
    
    print(f"  Outliers removed: {n_removed:,} ({pct_removed:.2f}%)")
    print(f"  Samples remaining: {len(X_filtered):,}")
    
    return X_filtered, keep_mask
