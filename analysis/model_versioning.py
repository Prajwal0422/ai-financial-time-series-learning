"""
Model Versioning Module
Manages model versions with metadata and lineage tracking
"""

import joblib
import json
from pathlib import Path
from datetime import datetime
import shutil


class ModelVersionManager:
    """
    Manage model versions with metadata and lineage.
    """
    
    def __init__(self, models_dir='models'):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.versions_dir = self.models_dir / 'versions'
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.models_dir / 'model_registry.json'
        self.registry = self._load_registry()
    
    def _load_registry(self):
        """Load model registry from file."""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return {'models': [], 'latest_version': None}
    
    def _save_registry(self):
        """Save model registry to file."""
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def save_model(self, model, scaler, features, metrics, version_tag=None, description=''):
        """
        Save model with version tag and metadata.
        
        Args:
            model: Trained model object
            scaler: Fitted scaler object
            features (list): List of feature names
            metrics (dict): Performance metrics
            version_tag (str): Version tag (default: auto-generated)
            description (str): Description of this version
            
        Returns:
            str: Version tag
        """
        # Generate version tag if not provided
        if version_tag is None:
            version_tag = self._generate_version_tag()
        
        # Create version directory
        version_dir = self.versions_dir / version_tag
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model artifacts
        joblib.dump(model, version_dir / 'model.pkl')
        joblib.dump(scaler, version_dir / 'scaler.pkl')
        joblib.dump(features, version_dir / 'features.pkl')
        joblib.dump(metrics, version_dir / 'metrics.pkl')
        
        # Create metadata
        metadata = {
            'version': version_tag,
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'n_clusters': int(model.n_clusters),
            'n_features': len(features),
            'features': features,
            'metrics': metrics,
            'model_type': type(model).__name__,
            'files': {
                'model': str(version_dir / 'model.pkl'),
                'scaler': str(version_dir / 'scaler.pkl'),
                'features': str(version_dir / 'features.pkl'),
                'metrics': str(version_dir / 'metrics.pkl')
            }
        }
        
        # Save metadata
        with open(version_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update registry
        self.registry['models'].append(metadata)
        self.registry['latest_version'] = version_tag
        self._save_registry()
        
        # Also save as current production model
        self._save_as_production(model, scaler, features, metrics)
        
        print(f"✓ Model saved as version: {version_tag}")
        print(f"  Location: {version_dir}")
        print(f"  Clusters: {metadata['n_clusters']}")
        print(f"  Features: {metadata['n_features']}")
        
        return version_tag
    
    def _generate_version_tag(self):
        """Generate version tag based on timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"v_{timestamp}"
    
    def _save_as_production(self, model, scaler, features, metrics):
        """Save model as current production version."""
        joblib.dump(model, self.models_dir / 'kmeans.pkl')
        joblib.dump(scaler, self.models_dir / 'scaler.pkl')
        joblib.dump(features, self.models_dir / 'features.pkl')
        joblib.dump(metrics, self.models_dir / 'metrics.pkl')
    
    def load_model(self, version_tag=None):
        """
        Load a specific model version.
        
        Args:
            version_tag (str): Version to load (default: latest)
            
        Returns:
            tuple: (model, scaler, features, metrics, metadata)
        """
        if version_tag is None:
            version_tag = self.registry.get('latest_version')
            if version_tag is None:
                raise ValueError("No models found in registry")
        
        version_dir = self.versions_dir / version_tag
        
        if not version_dir.exists():
            raise ValueError(f"Version {version_tag} not found")
        
        # Load artifacts
        model = joblib.load(version_dir / 'model.pkl')
        scaler = joblib.load(version_dir / 'scaler.pkl')
        features = joblib.load(version_dir / 'features.pkl')
        metrics = joblib.load(version_dir / 'metrics.pkl')
        
        # Load metadata
        with open(version_dir / 'metadata.json', 'r') as f:
            metadata = json.load(f)
        
        print(f"✓ Loaded model version: {version_tag}")
        
        return model, scaler, features, metrics, metadata
    
    def list_versions(self):
        """
        List all model versions.
        
        Returns:
            list: List of version metadata
        """
        return self.registry.get('models', [])
    
    def get_latest_version(self):
        """
        Get latest model version tag.
        
        Returns:
            str: Latest version tag
        """
        return self.registry.get('latest_version')
    
    def compare_versions(self, version_tags):
        """
        Compare multiple model versions.
        
        Args:
            version_tags (list): List of version tags to compare
            
        Returns:
            dict: Comparison data
        """
        comparison = {}
        
        for version_tag in version_tags:
            version_dir = self.versions_dir / version_tag
            if not version_dir.exists():
                continue
            
            with open(version_dir / 'metadata.json', 'r') as f:
                metadata = json.load(f)
            
            comparison[version_tag] = {
                'timestamp': metadata['timestamp'],
                'n_clusters': metadata['n_clusters'],
                'n_features': metadata['n_features'],
                'metrics': metadata['metrics']
            }
        
        return comparison
    
    def print_registry(self):
        """Print model registry summary."""
        print("\n" + "=" * 80)
        print("MODEL REGISTRY")
        print("=" * 80)
        print(f"Total versions: {len(self.registry['models'])}")
        print(f"Latest version: {self.registry.get('latest_version', 'None')}")
        print(f"Registry file: {self.registry_file}")
        print("\nVersions:")
        print("-" * 80)
        
        for model_info in self.registry['models']:
            print(f"\n{model_info['version']}")
            print(f"  Timestamp: {model_info['timestamp']}")
            print(f"  Description: {model_info.get('description', 'N/A')}")
            print(f"  Clusters: {model_info['n_clusters']}")
            print(f"  Features: {model_info['n_features']}")
            print(f"  Metrics:")
            for metric_name, metric_value in model_info['metrics'].items():
                print(f"    {metric_name}: {metric_value}")
        
        print("=" * 80)
