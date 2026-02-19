"""
Model Evaluator
Handles model evaluation and experiment tracking
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


class ModelEvaluator:
    """
    Evaluates models and tracks experiments.
    """
    
    def __init__(self, experiments_log='experiments_real.csv'):
        self.experiments_log = Path(experiments_log)
    
    def log_experiment(self, version, dataset_count, total_samples, 
                      k_selected, metrics, training_time, model_type):
        """
        Log experiment results to CSV.
        
        Args:
            version (int): Model version
            dataset_count (int): Number of datasets
            total_samples (int): Total samples
            k_selected (int): Selected K value
            metrics (dict): Performance metrics
            training_time (float): Training time in seconds
            model_type (str): Model type (KMeans or MiniBatchKMeans)
        """
        print(f"\n{'='*80}")
        print("LOGGING EXPERIMENT")
        print(f"{'='*80}")
        
        experiment_data = {
            'version': version,
            'timestamp': datetime.now().isoformat(),
            'dataset_count': dataset_count,
            'total_samples': total_samples,
            'K_selected': k_selected,
            'silhouette_score': metrics['silhouette_score'],
            'davies_bouldin': metrics['davies_bouldin_index'],
            'inertia': metrics.get('inertia', 0),
            'training_time': training_time,
            'model_type': model_type
        }
        
        # Append to CSV
        df = pd.DataFrame([experiment_data])
        
        if self.experiments_log.exists():
            df.to_csv(self.experiments_log, mode='a', header=False, index=False)
        else:
            df.to_csv(self.experiments_log, index=False)
        
        print(f"\n✓ Experiment logged to: {self.experiments_log}")
        print(f"  Version: {version}")
        print(f"  Samples: {total_samples:,}")
        print(f"  K: {k_selected}")
        print(f"  Silhouette: {metrics['silhouette_score']:.4f}")
        print(f"  Davies-Bouldin: {metrics['davies_bouldin_index']:.4f}")
        print(f"  Training time: {training_time:.2f}s")
        print(f"{'='*80}\n")
    
    def get_experiment_history(self):
        """Get all experiment history."""
        if not self.experiments_log.exists():
            return pd.DataFrame()
        
        return pd.read_csv(self.experiments_log)
    
    def get_best_experiment(self, metric='silhouette_score'):
        """Get best experiment based on metric."""
        history = self.get_experiment_history()
        
        if history.empty:
            return None
        
        if metric == 'silhouette_score':
            return history.loc[history[metric].idxmax()]
        elif metric == 'davies_bouldin':
            return history.loc[history[metric].idxmin()]
        else:
            return None
    
    def compare_experiments(self, version1, version2):
        """Compare two experiments."""
        history = self.get_experiment_history()
        
        if history.empty:
            return None
        
        exp1 = history[history['version'] == version1]
        exp2 = history[history['version'] == version2]
        
        if exp1.empty or exp2.empty:
            return None
        
        exp1 = exp1.iloc[0]
        exp2 = exp2.iloc[0]
        
        comparison = {
            'version1': version1,
            'version2': version2,
            'silhouette_diff': exp2['silhouette_score'] - exp1['silhouette_score'],
            'davies_bouldin_diff': exp2['davies_bouldin'] - exp1['davies_bouldin'],
            'samples_diff': exp2['total_samples'] - exp1['total_samples'],
            'time_diff': exp2['training_time'] - exp1['training_time']
        }
        
        return comparison
    
    def print_experiment_summary(self):
        """Print summary of all experiments."""
        history = self.get_experiment_history()
        
        if history.empty:
            print("No experiments logged yet.")
            return
        
        print(f"\n{'='*80}")
        print("EXPERIMENT HISTORY")
        print(f"{'='*80}")
        print(f"\nTotal experiments: {len(history)}")
        print(f"\nBest silhouette score: {history['silhouette_score'].max():.4f} (v{history.loc[history['silhouette_score'].idxmax(), 'version']})")
        print(f"Best Davies-Bouldin: {history['davies_bouldin'].min():.4f} (v{history.loc[history['davies_bouldin'].idxmin(), 'version']})")
        print(f"\nLatest 5 experiments:")
        print(history.tail(5).to_string(index=False))
        print(f"{'='*80}\n")
