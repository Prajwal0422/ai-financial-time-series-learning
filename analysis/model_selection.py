"""
Model Selection Module
Compares different K values for K-Means clustering and selects optimal configuration
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import matplotlib.pyplot as plt
from pathlib import Path
import json


def evaluate_k_range(X, k_range=(3, 9), n_init=20, random_state=42):
    """
    Evaluate K-Means clustering for different values of K.
    
    Args:
        X (np.ndarray): Scaled feature matrix
        k_range (tuple): Range of K values to test (min, max)
        n_init (int): Number of initializations per K
        random_state (int): Random seed for reproducibility
        
    Returns:
        dict: Results containing metrics for each K value
    """
    results = {
        'k_values': [],
        'silhouette_scores': [],
        'davies_bouldin_scores': [],
        'calinski_harabasz_scores': [],
        'inertias': []
    }
    
    print(f"\nEvaluating K-Means for K = {k_range[0]} to {k_range[1]-1}")
    print("=" * 60)
    
    for k in range(k_range[0], k_range[1]):
        print(f"Testing K={k}...", end=" ")
        
        # Train K-Means
        kmeans = KMeans(n_clusters=k, n_init=n_init, random_state=random_state, max_iter=300)
        labels = kmeans.fit_predict(X)
        
        # Calculate metrics
        silhouette = silhouette_score(X, labels)
        davies_bouldin = davies_bouldin_score(X, labels)
        calinski_harabasz = calinski_harabasz_score(X, labels)
        inertia = kmeans.inertia_
        
        # Store results
        results['k_values'].append(k)
        results['silhouette_scores'].append(silhouette)
        results['davies_bouldin_scores'].append(davies_bouldin)
        results['calinski_harabasz_scores'].append(calinski_harabasz)
        results['inertias'].append(inertia)
        
        print(f"Silhouette: {silhouette:.4f}, DB: {davies_bouldin:.4f}")
    
    print("=" * 60)
    return results


def select_optimal_k(results, method='silhouette'):
    """
    Select optimal K based on specified metric.
    
    Args:
        results (dict): Results from evaluate_k_range
        method (str): Selection method ('silhouette', 'davies_bouldin', 'elbow')
        
    Returns:
        int: Optimal K value
    """
    if method == 'silhouette':
        # Higher is better
        idx = np.argmax(results['silhouette_scores'])
        optimal_k = results['k_values'][idx]
        score = results['silhouette_scores'][idx]
        print(f"\nOptimal K by Silhouette Score: {optimal_k} (score: {score:.4f})")
        
    elif method == 'davies_bouldin':
        # Lower is better
        idx = np.argmin(results['davies_bouldin_scores'])
        optimal_k = results['k_values'][idx]
        score = results['davies_bouldin_scores'][idx]
        print(f"\nOptimal K by Davies-Bouldin Index: {optimal_k} (score: {score:.4f})")
        
    elif method == 'elbow':
        # Use elbow method on inertia
        inertias = np.array(results['inertias'])
        # Calculate rate of change
        diffs = np.diff(inertias)
        diffs_pct = np.abs(diffs / inertias[:-1])
        # Find elbow (where improvement drops below threshold)
        threshold = 0.1
        elbow_idx = np.where(diffs_pct < threshold)[0]
        if len(elbow_idx) > 0:
            optimal_k = results['k_values'][elbow_idx[0]]
        else:
            optimal_k = results['k_values'][len(results['k_values'])//2]
        print(f"\nOptimal K by Elbow Method: {optimal_k}")
    
    return optimal_k


def plot_model_comparison(results, output_dir='static/charts'):
    """
    Create visualization comparing different K values.
    
    Args:
        results (dict): Results from evaluate_k_range
        output_dir (str): Directory to save plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('K-Means Model Comparison', fontsize=16, fontweight='bold')
    
    k_values = results['k_values']
    
    # Silhouette Score
    axes[0, 0].plot(k_values, results['silhouette_scores'], 'o-', linewidth=2, markersize=8)
    axes[0, 0].set_xlabel('Number of Clusters (K)')
    axes[0, 0].set_ylabel('Silhouette Score')
    axes[0, 0].set_title('Silhouette Score (Higher is Better)')
    axes[0, 0].grid(True, alpha=0.3)
    best_k_sil = k_values[np.argmax(results['silhouette_scores'])]
    axes[0, 0].axvline(best_k_sil, color='red', linestyle='--', alpha=0.5, label=f'Best K={best_k_sil}')
    axes[0, 0].legend()
    
    # Davies-Bouldin Index
    axes[0, 1].plot(k_values, results['davies_bouldin_scores'], 'o-', linewidth=2, markersize=8, color='orange')
    axes[0, 1].set_xlabel('Number of Clusters (K)')
    axes[0, 1].set_ylabel('Davies-Bouldin Index')
    axes[0, 1].set_title('Davies-Bouldin Index (Lower is Better)')
    axes[0, 1].grid(True, alpha=0.3)
    best_k_db = k_values[np.argmin(results['davies_bouldin_scores'])]
    axes[0, 1].axvline(best_k_db, color='red', linestyle='--', alpha=0.5, label=f'Best K={best_k_db}')
    axes[0, 1].legend()
    
    # Calinski-Harabasz Score
    axes[1, 0].plot(k_values, results['calinski_harabasz_scores'], 'o-', linewidth=2, markersize=8, color='green')
    axes[1, 0].set_xlabel('Number of Clusters (K)')
    axes[1, 0].set_ylabel('Calinski-Harabasz Score')
    axes[1, 0].set_title('Calinski-Harabasz Score (Higher is Better)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Elbow Plot (Inertia)
    axes[1, 1].plot(k_values, results['inertias'], 'o-', linewidth=2, markersize=8, color='purple')
    axes[1, 1].set_xlabel('Number of Clusters (K)')
    axes[1, 1].set_ylabel('Inertia')
    axes[1, 1].set_title('Elbow Method (Inertia)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / 'model_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Model comparison plot saved to {output_path / 'model_comparison.png'}")


def save_comparison_results(results, optimal_k, output_path='models/model_comparison.json'):
    """
    Save model comparison results to JSON file.
    
    Args:
        results (dict): Results from evaluate_k_range
        optimal_k (int): Selected optimal K value
        output_path (str): Path to save JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy types to Python types for JSON serialization
    comparison_data = {
        'optimal_k': int(optimal_k),
        'k_values': [int(k) for k in results['k_values']],
        'silhouette_scores': [float(s) for s in results['silhouette_scores']],
        'davies_bouldin_scores': [float(d) for d in results['davies_bouldin_scores']],
        'calinski_harabasz_scores': [float(c) for c in results['calinski_harabasz_scores']],
        'inertias': [float(i) for i in results['inertias']]
    }
    
    with open(output_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"✓ Comparison results saved to {output_file}")
