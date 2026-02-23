"""
Clustering Algorithm Comparison
Tests multiple algorithms to find best performer
"""

import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score
import warnings
warnings.filterwarnings('ignore')


def train_kmeans(X, n_clusters, random_state=42):
    """Train KMeans model."""
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=20,
        max_iter=300
    )
    labels = model.fit_predict(X)
    return model, labels


def train_minibatch_kmeans(X, n_clusters, random_state=42):
    """Train MiniBatchKMeans model."""
    model = MiniBatchKMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        batch_size=1024,
        n_init=10,
        max_iter=100
    )
    labels = model.fit_predict(X)
    return model, labels


def train_gaussian_mixture(X, n_clusters, random_state=42):
    """Train Gaussian Mixture Model."""
    model = GaussianMixture(
        n_components=n_clusters,
        random_state=random_state,
        covariance_type='full',
        n_init=10,
        max_iter=100
    )
    labels = model.fit_predict(X)
    return model, labels



def train_agglomerative(X, n_clusters):
    """Train Agglomerative Clustering model."""
    model = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage='ward'
    )
    labels = model.fit_predict(X)
    return model, labels


def compare_algorithms(X, n_clusters, random_state=42):
    """
    Compare multiple clustering algorithms.
    
    Args:
        X (np.ndarray): Feature matrix
        n_clusters (int): Number of clusters
        random_state (int): Random seed
        
    Returns:
        dict: Comparison results
    """
    print(f"\n  Comparing algorithms with K={n_clusters}...")
    print(f"  {'Algorithm':<25} | {'Silhouette':>11} | {'Davies-Bouldin':>15}")
    print("  " + "─" * 60)
    
    results = []
    
    # 1. KMeans
    try:
        model, labels = train_kmeans(X, n_clusters, random_state)
        sil = silhouette_score(X, labels)
        db = davies_bouldin_score(X, labels)
        results.append({
            'algorithm': 'KMeans',
            'model': model,
            'labels': labels,
            'silhouette': sil,
            'davies_bouldin': db
        })
        print(f"  {'KMeans':<25} | {sil:11.4f} | {db:15.4f}")
    except Exception as e:
        print(f"  {'KMeans':<25} | Error: {str(e)}")

    
    # 2. MiniBatchKMeans
    try:
        model, labels = train_minibatch_kmeans(X, n_clusters, random_state)
        sil = silhouette_score(X, labels)
        db = davies_bouldin_score(X, labels)
        results.append({
            'algorithm': 'MiniBatchKMeans',
            'model': model,
            'labels': labels,
            'silhouette': sil,
            'davies_bouldin': db
        })
        print(f"  {'MiniBatchKMeans':<25} | {sil:11.4f} | {db:15.4f}")
    except Exception as e:
        print(f"  {'MiniBatchKMeans':<25} | Error: {str(e)}")
    
    # 3. Gaussian Mixture
    try:
        model, labels = train_gaussian_mixture(X, n_clusters, random_state)
        sil = silhouette_score(X, labels)
        db = davies_bouldin_score(X, labels)
        results.append({
            'algorithm': 'GaussianMixture',
            'model': model,
            'labels': labels,
            'silhouette': sil,
            'davies_bouldin': db
        })
        print(f"  {'GaussianMixture':<25} | {sil:11.4f} | {db:15.4f}")
    except Exception as e:
        print(f"  {'GaussianMixture':<25} | Error: {str(e)}")
    
    # 4. Agglomerative Clustering
    try:
        model, labels = train_agglomerative(X, n_clusters)
        sil = silhouette_score(X, labels)
        db = davies_bouldin_score(X, labels)
        results.append({
            'algorithm': 'AgglomerativeClustering',
            'model': model,
            'labels': labels,
            'silhouette': sil,
            'davies_bouldin': db
        })
        print(f"  {'AgglomerativeClustering':<25} | {sil:11.4f} | {db:15.4f}")
    except Exception as e:
        print(f"  {'AgglomerativeClustering':<25} | Error: {str(e)}")
    
    print("  " + "─" * 60)
    
    # Select best algorithm
    if results:
        best = max(results, key=lambda x: x['silhouette'])
        print(f"\n  ✓ Best algorithm: {best['algorithm']}")
        print(f"    Silhouette: {best['silhouette']:.4f}")
        print(f"    Davies-Bouldin: {best['davies_bouldin']:.4f}")
        return best, results
    else:
        raise ValueError("All algorithms failed")
