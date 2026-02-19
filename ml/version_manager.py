"""
Model Version Manager
Handles automatic versioning, artifact storage, and version tracking
"""

import json
from pathlib import Path
from datetime import datetime
import joblib
import shutil


class ModelVersionManager:
    """
    Manages model versions with automatic incrementing and artifact storage.
    """
    
    def __init__(self, base_dir='models/real_data'):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.versions_file = self.base_dir / 'versions.json'
        self.versions_data = self._load_versions()
    
    def _load_versions(self):
        """Load version tracking data."""
        if self.versions_file.exists():
            with open(self.versions_file, 'r') as f:
                return json.load(f)
        return {
            'current_version': 0,
            'versions': []
        }
    
    def _save_versions(self):
        """Save version tracking data."""
        with open(self.versions_file, 'w') as f:
            json.dump(self.versions_data, f, indent=2)
    
    def get_next_version(self):
        """Get next version number."""
        return self.versions_data['current_version'] + 1
    
    def get_current_version(self):
        """Get current version number."""
        return self.versions_data['current_version']
    
    def get_version_dir(self, version=None):
        """Get directory for specific version."""
        if version is None:
            version = self.get_current_version()
        return self.base_dir / f"v{version}"
    
    def save_model_version(self, model, scaler, features, metrics, 
                          cluster_summary, cluster_means, k_comparison,
                          training_config):
        """
        Save a new model version with all artifacts.
        
        Args:
            model: Trained clustering model
            scaler: Fitted StandardScaler
            features (list): Feature names
            metrics (dict): Performance metrics
            cluster_summary (pd.DataFrame): Cluster distribution
            cluster_means (pd.DataFrame): Mean features per cluster
            k_comparison (pd.DataFrame): K comparison results
            training_config (dict): Training configuration
            
        Returns:
            int: Version number
        """
        # Get next version
        version = self.get_next_version()
        version_dir = self.get_version_dir(version)
        version_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*80}")
        print(f"SAVING MODEL VERSION {version}")
        print(f"{'='*80}")
        print(f"Directory: {version_dir}")
        
        # Save model artifacts
        joblib.dump(model, version_dir / 'model.pkl')
        print(f"✓ model.pkl")
        
        joblib.dump(scaler, version_dir / 'scaler.pkl')
        print(f"✓ scaler.pkl")
        
        joblib.dump(features, version_dir / 'features.pkl')
        print(f"✓ features.pkl")
        
        # Save metrics as JSON
        with open(version_dir / 'metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"✓ metrics.json")
        
        # Save cluster summary
        cluster_summary.to_csv(version_dir / 'cluster_summary.csv', index=False)
        print(f"✓ cluster_summary.csv")
        
        # Save cluster means
        cluster_means.to_csv(version_dir / 'cluster_means.csv')
        print(f"✓ cluster_means.csv")
        
        # Save K comparison
        k_comparison.to_csv(version_dir / 'k_comparison.csv', index=False)
        print(f"✓ k_comparison.csv")
        
        # Save training config
        with open(version_dir / 'training_config.json', 'w') as f:
            json.dump(training_config, f, indent=2)
        print(f"✓ training_config.json")
        
        # Create version metadata
        metadata = {
            'version': version,
            'timestamp': datetime.now().isoformat(),
            'model_type': type(model).__name__,
            'n_clusters': int(model.n_clusters),
            'n_features': len(features),
            'features': features,
            'metrics': metrics,
            'training_config': training_config
        }
        
        with open(version_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ metadata.json")
        
        # Update version tracking
        self.versions_data['current_version'] = version
        self.versions_data['versions'].append({
            'version': version,
            'timestamp': metadata['timestamp'],
            'n_clusters': metadata['n_clusters'],
            'silhouette_score': metrics.get('silhouette_score', 0),
            'davies_bouldin_index': metrics.get('davies_bouldin_index', 0)
        })
        self._save_versions()
        
        # Also save as "latest" for easy access
        self._save_as_latest(model, scaler, features, metrics)
        
        print(f"{'='*80}")
        print(f"✓ Model version {version} saved successfully")
        print(f"{'='*80}\n")
        
        return version
    
    def _save_as_latest(self, model, scaler, features, metrics):
        """Save model as 'latest' for production use."""
        latest_dir = self.base_dir / 'latest'
        latest_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(model, latest_dir / 'model.pkl')
        joblib.dump(scaler, latest_dir / 'scaler.pkl')
        joblib.dump(features, latest_dir / 'features.pkl')
        
        with open(latest_dir / 'metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Also update old location for backward compatibility
        joblib.dump(model, self.base_dir.parent / 'kmeans.pkl')
        joblib.dump(scaler, self.base_dir.parent / 'scaler.pkl')
        joblib.dump(features, self.base_dir.parent / 'features.pkl')
    
    def load_model_version(self, version=None):
        """
        Load a specific model version.
        
        Args:
            version (int): Version number (None for latest)
            
        Returns:
            tuple: (model, scaler, features, metrics, metadata)
        """
        if version is None:
            version = self.get_current_version()
        
        version_dir = self.get_version_dir(version)
        
        if not version_dir.exists():
            raise ValueError(f"Version {version} not found")
        
        model = joblib.load(version_dir / 'model.pkl')
        scaler = joblib.load(version_dir / 'scaler.pkl')
        features = joblib.load(version_dir / 'features.pkl')
        
        with open(version_dir / 'metrics.json', 'r') as f:
            metrics = json.load(f)
        
        with open(version_dir / 'metadata.json', 'r') as f:
            metadata = json.load(f)
        
        return model, scaler, features, metrics, metadata
    
    def list_versions(self):
        """List all available versions."""
        return self.versions_data['versions']
    
    def get_version_info(self, version=None):
        """Get information about a specific version."""
        if version is None:
            version = self.get_current_version()
        
        version_dir = self.get_version_dir(version)
        
        if not version_dir.exists():
            return None
        
        with open(version_dir / 'metadata.json', 'r') as f:
            return json.load(f)
    
    def compare_versions(self, version1, version2):
        """Compare two model versions."""
        info1 = self.get_version_info(version1)
        info2 = self.get_version_info(version2)
        
        if info1 is None or info2 is None:
            return None
        
        comparison = {
            'version1': version1,
            'version2': version2,
            'timestamp1': info1['timestamp'],
            'timestamp2': info2['timestamp'],
            'metrics_diff': {
                'silhouette': info2['metrics']['silhouette_score'] - info1['metrics']['silhouette_score'],
                'davies_bouldin': info2['metrics']['davies_bouldin_index'] - info1['metrics']['davies_bouldin_index']
            },
            'n_clusters1': info1['n_clusters'],
            'n_clusters2': info2['n_clusters']
        }
        
        return comparison
