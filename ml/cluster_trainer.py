"""
Cluster Trainer
Handles model training with automatic K selection
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import time


class ClusterTrainer:
    """
    Trains clustering models with automatic K selection.
    """
    
    def __init__(self, k_range=range(3, 9), random_state=42, 
                 n_init=20, large_dataset_threshold=100_000):
        """
        Initialize cluster trainer.
        
        Args:
            k_range (range): Range of K values to test
            random_state (int): Random state for reproducibility
            n_init (int): Number of initializations for KMeans
            large_dataset_threshold (int): Threshold for using MiniBatchKMeans
        """
        self.k_range = k_range
        self.random_state = random_state
        self.n_init = n_init
        self.large_dataset_threshold = large_dataset_threshold
    
    def scale_features(self, X):
        """
        Scale features using StandardScaler.
        
        Args:
            X (pd.DataFrame): Feature matrix
            
        Returns:
            tuple: (X_scaled, scaler)
        """
        print(f"\n{'='*80}")
        print("FEATURE SCALING")
        print(f"{'='*80}")
        
        print(f"\nScaling features with StandardScaler...")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        print(f"✓ Features scaled successfully")
        print(f"✓ Mean: {X_scaled.mean():.6f}")
        print(f"✓ Std: {X_scaled.std():.6f}")
        print(f"{'='*80}\n")
        
        return X_scaled, scaler
    
    def compare_k_values(self, X_scaled):
        """
        Compare different K values and select optimal.
        
        Args:
            X_scaled (np.ndarray): Scaled feature matrix
            
        Returns:
            dict: Comparison results with best model
        """
        print(f"\n{'='*80}")
        print("MODEL COMPARISON (K SELECTION)")
        print(f"{'='*80}")
        
        n_samples = X_scaled.shape[0]
        use_minibatch = n_samples > self.large_dataset_threshold
        model_type = "MiniBatchKMeans" if use_minibatch else "KMeans"
        
        print(f"\nComparing K values: {list(self.k_range)}")
        print(f"Model type: {model_type}")
        print(f"Samples: {n_samples:,}")
        print(f"Random state: {self.random_state}")
        print(f"\n{'K':>3} | {'Silhouette':>11} | {'Davies-Bouldin':>15} | {'Inertia':>12} | {'Time (s)':>9}")
        print("─" * 70)
        
        results = []
        
        for k in self.k_range:
            start_time = time.time()
            
            # Choose model based on dataset size
            if use_minibatch:
                model = MiniBatchKMeans(
                    n_clusters=k,
                    random_state=self.random_state,
                    batch_size=1024,
                    n_init=3,
                    max_iter=100
                )
            else:
                model = KMeans(
                    n_clusters=k,
                    random_state=self.random_state,
                    n_init=self.n_init,
                    max_iter=300
                )
            
            # Train
            labels = model.fit_predict(X_scaled)
            
            # Evaluate
            silhouette = silhouette_score(X_scaled, labels)
            davies_bouldin = davies_bouldin_score(X_scaled, labels)
            inertia = model.inertia_
            
            training_time = time.time() - start_time
            
            results.append({
                'k': k,
                'silhouette': silhouette,
                'davies_bouldin': davies_bouldin,
                'inertia': inertia,
                'training_time': training_time,
                'model': model,
                'labels': labels
            })
            
            print(f"{k:3d} | {silhouette:11.4f} | {davies_bouldin:15.4f} | {inertia:12.0f} | {training_time:9.2f}")
        
        print("─" * 70)
        
        # Select best K (highest silhouette score)
        best_result = max(results, key=lambda x: x['silhouette'])
        best_k = best_result['k']
        
        print(f"\n✓ Optimal K: {best_k}")
        print(f"  Silhouette: {best_result['silhouette']:.4f}")
        print(f"  Davies-Bouldin: {best_result['davies_bouldin']:.4f}")
        print(f"  Training time: {best_result['training_time']:.2f}s")
        print(f"{'='*80}\n")
        
        # Create comparison dataframe
        k_comparison_df = pd.DataFrame([
            {
                'K': r['k'],
                'Silhouette': r['silhouette'],
                'Davies_Bouldin': r['davies_bouldin'],
                'Inertia': r['inertia'],
                'Training_Time': r['training_time']
            }
            for r in results
        ])
        
        return {
            'results': results,
            'best_k': best_k,
            'best_model': best_result['model'],
            'best_labels': best_result['labels'],
            'best_metrics': {
                'silhouette_score': best_result['silhouette'],
                'davies_bouldin_index': best_result['davies_bouldin'],
                'inertia': best_result['inertia'],
                'training_time': best_result['training_time']
            },
            'k_comparison_df': k_comparison_df,
            'model_type': model_type
        }
    
    def analyze_clusters(self, X_scaled, labels, feature_names):
        """
        Analyze cluster characteristics.
        
        Args:
            X_scaled (np.ndarray): Scaled features
            labels (np.ndarray): Cluster labels
            feature_names (list): Feature names
            
        Returns:
            tuple: (cluster_summary_df, cluster_means_df)
        """
        print(f"\n{'='*80}")
        print("CLUSTER ANALYSIS")
        print(f"{'='*80}")
        
        # Cluster distribution
        unique, counts = np.unique(labels, return_counts=True)
        
        print(f"\nCluster Distribution:")
        print(f"{'Cluster':>8} | {'Count':>10} | {'Percentage':>10}")
        print("─" * 35)
        
        for cluster, count in zip(unique, counts):
            percentage = (count / len(labels)) * 100
            print(f"{cluster:8d} | {count:10,} | {percentage:9.2f}%")
        
        # Compute mean feature values per cluster
        X_df = pd.DataFrame(X_scaled, columns=feature_names)
        X_df['Cluster'] = labels
        
        cluster_means = X_df.groupby('Cluster').mean()
        
        print(f"\nCluster Feature Means (scaled):")
        print(cluster_means.to_string())
        
        # Create summary dataframe
        summary_df = pd.DataFrame({
            'Cluster': unique,
            'Count': counts,
            'Percentage': (counts / len(labels)) * 100
        })
        
        print(f"{'='*80}\n")
        
        return summary_df, cluster_means
