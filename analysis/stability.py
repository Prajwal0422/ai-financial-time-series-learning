"""
Clustering Stability Analysis
Measures consistency of clustering results across multiple runs
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.metrics.cluster import contingency_matrix
import json
from pathlib import Path


def measure_clustering_stability(X, n_clusters=4, n_runs=10, n_init=20, random_state_base=42):
    """
    Run clustering multiple times and measure consistency.
    
    Args:
        X (np.ndarray): Scaled feature matrix
        n_clusters (int): Number of clusters
        n_runs (int): Number of independent runs
        n_init (int): Number of initializations per run
        random_state_base (int): Base random seed
        
    Returns:
        dict: Stability metrics
    """
    print(f"\nMeasuring clustering stability ({n_runs} runs)...")
    print("=" * 60)
    
    all_labels = []
    
    # Run clustering multiple times with different random states
    for run in range(n_runs):
        random_state = random_state_base + run
        kmeans = KMeans(n_clusters=n_clusters, n_init=n_init, random_state=random_state, max_iter=300)
        labels = kmeans.fit_predict(X)
        all_labels.append(labels)
        print(f"Run {run+1}/{n_runs} complete")
    
    # Calculate pairwise similarity between runs
    ari_scores = []
    nmi_scores = []
    
    for i in range(n_runs):
        for j in range(i+1, n_runs):
            ari = adjusted_rand_score(all_labels[i], all_labels[j])
            nmi = normalized_mutual_info_score(all_labels[i], all_labels[j])
            ari_scores.append(ari)
            nmi_scores.append(nmi)
    
    # Calculate statistics
    stability_metrics = {
        'n_runs': n_runs,
        'n_clusters': n_clusters,
        'ari_mean': float(np.mean(ari_scores)),
        'ari_std': float(np.std(ari_scores)),
        'ari_min': float(np.min(ari_scores)),
        'ari_max': float(np.max(ari_scores)),
        'nmi_mean': float(np.mean(nmi_scores)),
        'nmi_std': float(np.std(nmi_scores)),
        'nmi_min': float(np.min(nmi_scores)),
        'nmi_max': float(np.max(nmi_scores))
    }
    
    print("=" * 60)
    print(f"Adjusted Rand Index (ARI):")
    print(f"  Mean: {stability_metrics['ari_mean']:.4f} ± {stability_metrics['ari_std']:.4f}")
    print(f"  Range: [{stability_metrics['ari_min']:.4f}, {stability_metrics['ari_max']:.4f}]")
    print(f"\nNormalized Mutual Information (NMI):")
    print(f"  Mean: {stability_metrics['nmi_mean']:.4f} ± {stability_metrics['nmi_std']:.4f}")
    print(f"  Range: [{stability_metrics['nmi_min']:.4f}, {stability_metrics['nmi_max']:.4f}]")
    print("=" * 60)
    
    # Interpretation
    if stability_metrics['ari_mean'] > 0.8:
        print("✓ Clustering is HIGHLY STABLE")
    elif stability_metrics['ari_mean'] > 0.6:
        print("✓ Clustering is MODERATELY STABLE")
    else:
        print("⚠ Clustering shows LOW STABILITY - consider different K or features")
    
    return stability_metrics


def save_stability_results(stability_metrics, output_path='models/stability_metrics.json'):
    """
    Save stability analysis results to JSON file.
    
    Args:
        stability_metrics (dict): Stability metrics from measure_clustering_stability
        output_path (str): Path to save JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(stability_metrics, f, indent=2)
    
    print(f"✓ Stability metrics saved to {output_file}")
