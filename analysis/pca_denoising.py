"""
PCA-based Denoising for Clustering
Reduces noise and dimensionality while preserving variance
"""

import numpy as np
from sklearn.decomposition import PCA


def apply_pca_denoising(X_scaled, variance_threshold=0.95):
    """
    Apply PCA to denoise features.
    
    Args:
        X_scaled (np.ndarray): Scaled feature matrix
        variance_threshold (float): Cumulative variance to preserve
        
    Returns:
        tuple: (X_pca, pca_model, n_components)
    """
    print(f"\n  Applying PCA denoising...")
    print(f"  Target variance: {variance_threshold*100:.1f}%")
    
    # Fit PCA
    pca = PCA(n_components=variance_threshold, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    n_components = pca.n_components_
    explained_var = pca.explained_variance_ratio_.sum()
    
    print(f"  ✓ Components selected: {n_components}")
    print(f"  ✓ Variance explained: {explained_var*100:.2f}%")
    print(f"  ✓ Dimensionality: {X_scaled.shape[1]} → {n_components}")
    
    # Show component importance
    print(f"\n  Component variance breakdown:")
    for i, var in enumerate(pca.explained_variance_ratio_[:5], 1):
        print(f"    PC{i}: {var*100:.2f}%")
    if n_components > 5:
        print(f"    ... ({n_components-5} more components)")
    
    return X_pca, pca, n_components
