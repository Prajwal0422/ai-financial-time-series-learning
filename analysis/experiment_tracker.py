"""
Experiment Tracking Module
Logs parameters, metrics, and results for reproducibility
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib


class ExperimentTracker:
    """
    Track ML experiments with parameters, metrics, and metadata.
    """
    
    def __init__(self, experiment_dir='experiments'):
        self.experiment_dir = Path(experiment_dir)
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.experiment_dir / 'experiment_log.jsonl'
        self.summary_file = self.experiment_dir / 'experiments_summary.csv'
    
    def log_experiment(self, experiment_name, parameters, metrics, metadata=None):
        """
        Log a single experiment with all details.
        
        Args:
            experiment_name (str): Name/description of experiment
            parameters (dict): Model parameters and configuration
            metrics (dict): Performance metrics
            metadata (dict): Additional metadata (optional)
            
        Returns:
            str: Experiment ID
        """
        timestamp = datetime.now().isoformat()
        
        # Generate experiment ID
        exp_id = self._generate_experiment_id(experiment_name, timestamp)
        
        experiment_record = {
            'experiment_id': exp_id,
            'experiment_name': experiment_name,
            'timestamp': timestamp,
            'parameters': parameters,
            'metrics': metrics,
            'metadata': metadata or {}
        }
        
        # Append to JSONL log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(experiment_record) + '\n')
        
        # Update summary CSV
        self._update_summary(experiment_record)
        
        print(f"✓ Experiment logged: {exp_id}")
        return exp_id
    
    def _generate_experiment_id(self, name, timestamp):
        """Generate unique experiment ID."""
        hash_input = f"{name}_{timestamp}".encode()
        hash_short = hashlib.md5(hash_input).hexdigest()[:8]
        return f"exp_{hash_short}"
    
    def _update_summary(self, record):
        """Update summary CSV with experiment record."""
        # Flatten record for CSV
        flat_record = {
            'experiment_id': record['experiment_id'],
            'experiment_name': record['experiment_name'],
            'timestamp': record['timestamp']
        }
        
        # Add parameters
        for key, value in record['parameters'].items():
            flat_record[f'param_{key}'] = value
        
        # Add metrics
        for key, value in record['metrics'].items():
            flat_record[f'metric_{key}'] = value
        
        # Convert to DataFrame
        df_new = pd.DataFrame([flat_record])
        
        # Append to existing CSV or create new
        if self.summary_file.exists():
            df_existing = pd.read_csv(self.summary_file)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        
        df_combined.to_csv(self.summary_file, index=False)
    
    def get_experiment(self, experiment_id):
        """
        Retrieve a specific experiment by ID.
        
        Args:
            experiment_id (str): Experiment ID
            
        Returns:
            dict: Experiment record or None
        """
        if not self.log_file.exists():
            return None
        
        with open(self.log_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record['experiment_id'] == experiment_id:
                    return record
        
        return None
    
    def list_experiments(self, n=10):
        """
        List recent experiments.
        
        Args:
            n (int): Number of recent experiments to show
            
        Returns:
            list: List of experiment records
        """
        if not self.log_file.exists():
            return []
        
        experiments = []
        with open(self.log_file, 'r') as f:
            for line in f:
                experiments.append(json.loads(line))
        
        # Return most recent n experiments
        return experiments[-n:]
    
    def compare_experiments(self, experiment_ids):
        """
        Compare multiple experiments side by side.
        
        Args:
            experiment_ids (list): List of experiment IDs to compare
            
        Returns:
            pd.DataFrame: Comparison table
        """
        experiments = [self.get_experiment(exp_id) for exp_id in experiment_ids]
        experiments = [exp for exp in experiments if exp is not None]
        
        if not experiments:
            return None
        
        # Create comparison DataFrame
        comparison_data = []
        for exp in experiments:
            row = {
                'experiment_id': exp['experiment_id'],
                'name': exp['experiment_name'],
                'timestamp': exp['timestamp']
            }
            row.update({f'param_{k}': v for k, v in exp['parameters'].items()})
            row.update({f'metric_{k}': v for k, v in exp['metrics'].items()})
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def get_best_experiment(self, metric_name, maximize=True):
        """
        Find best experiment based on a specific metric.
        
        Args:
            metric_name (str): Name of metric to optimize
            maximize (bool): True to maximize, False to minimize
            
        Returns:
            dict: Best experiment record
        """
        if not self.summary_file.exists():
            return None
        
        df = pd.read_csv(self.summary_file)
        metric_col = f'metric_{metric_name}'
        
        if metric_col not in df.columns:
            return None
        
        if maximize:
            best_idx = df[metric_col].idxmax()
        else:
            best_idx = df[metric_col].idxmin()
        
        best_exp_id = df.loc[best_idx, 'experiment_id']
        return self.get_experiment(best_exp_id)
    
    def print_summary(self):
        """Print summary of all experiments."""
        if not self.summary_file.exists():
            print("No experiments logged yet.")
            return
        
        df = pd.read_csv(self.summary_file)
        
        print("\n" + "=" * 80)
        print("EXPERIMENT SUMMARY")
        print("=" * 80)
        print(f"Total experiments: {len(df)}")
        print(f"Log file: {self.log_file}")
        print(f"Summary file: {self.summary_file}")
        print("\nRecent experiments:")
        print("-" * 80)
        
        # Show last 5 experiments
        recent = df.tail(5)
        for _, row in recent.iterrows():
            print(f"\n{row['experiment_id']}: {row['experiment_name']}")
            print(f"  Timestamp: {row['timestamp']}")
            
            # Show parameters
            param_cols = [col for col in row.index if col.startswith('param_')]
            if param_cols:
                print("  Parameters:")
                for col in param_cols:
                    param_name = col.replace('param_', '')
                    print(f"    {param_name}: {row[col]}")
            
            # Show metrics
            metric_cols = [col for col in row.index if col.startswith('metric_')]
            if metric_cols:
                print("  Metrics:")
                for col in metric_cols:
                    metric_name = col.replace('metric_', '')
                    print(f"    {metric_name}: {row[col]}")
        
        print("=" * 80)


def log_training_experiment(tracker, n_clusters, features, metrics, data_info):
    """
    Convenience function to log a training experiment.
    
    Args:
        tracker (ExperimentTracker): Tracker instance
        n_clusters (int): Number of clusters
        features (list): List of feature names
        metrics (dict): Performance metrics
        data_info (dict): Information about training data
        
    Returns:
        str: Experiment ID
    """
    parameters = {
        'n_clusters': n_clusters,
        'n_features': len(features),
        'features': features,
        'algorithm': 'KMeans',
        'n_init': 20,
        'max_iter': 300,
        'random_state': 42
    }
    
    metadata = {
        'n_samples': data_info.get('n_samples', 0),
        'n_stocks': data_info.get('n_stocks', 0),
        'date_range': data_info.get('date_range', 'unknown')
    }
    
    experiment_name = f"KMeans_K{n_clusters}_{len(features)}features"
    
    return tracker.log_experiment(
        experiment_name=experiment_name,
        parameters=parameters,
        metrics=metrics,
        metadata=metadata
    )
