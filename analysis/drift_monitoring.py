"""
Drift Monitoring Module
Detects feature drift between model training runs
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class DriftMonitor:
    """Monitor feature drift between training runs"""
    
    def __init__(self, threshold: float = 0.15):
        """
        Initialize drift monitor
        
        Args:
            threshold: Percentage threshold for drift detection (default 15%)
        """
        self.threshold = threshold
        self.drift_report_path = Path("models/real_data/drift_report.json")
    
    def calculate_drift(self, 
                       current_features: pd.DataFrame, 
                       previous_features: pd.DataFrame) -> Dict:
        """
        Calculate drift between current and previous feature sets
        
        Args:
            current_features: Current training features
            previous_features: Previous training features
            
        Returns:
            Dictionary with drift metrics
        """
        drift_results = {
            'timestamp': datetime.now().isoformat(),
            'threshold': self.threshold,
            'features': {},
            'overall_drift': False,
            'drifted_features': []
        }
        
        # Calculate mean drift for each feature
        for col in current_features.columns:
            if col in previous_features.columns:
                current_mean = current_features[col].mean()
                previous_mean = previous_features[col].mean()
                
                # Calculate percentage change
                if previous_mean != 0:
                    drift_pct = abs((current_mean - previous_mean) / previous_mean)
                else:
                    drift_pct = 0.0
                
                is_drifted = drift_pct > self.threshold
                
                drift_results['features'][col] = {
                    'current_mean': float(current_mean),
                    'previous_mean': float(previous_mean),
                    'drift_percentage': float(drift_pct),
                    'is_drifted': is_drifted
                }
                
                if is_drifted:
                    drift_results['drifted_features'].append(col)
        
        # Overall drift if any feature drifted
        drift_results['overall_drift'] = len(drift_results['drifted_features']) > 0
        drift_results['num_drifted_features'] = len(drift_results['drifted_features'])
        drift_results['total_features'] = len(drift_results['features'])
        
        return drift_results
    
    def save_drift_report(self, drift_results: Dict):
        """Save drift report to JSON file"""
        self.drift_report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.drift_report_path, 'w') as f:
            json.dump(drift_results, f, indent=2)
        
        logger.info(f"Drift report saved to {self.drift_report_path}")
    
    def load_drift_report(self) -> Dict:
        """Load latest drift report"""
        if self.drift_report_path.exists():
            with open(self.drift_report_path, 'r') as f:
                return json.load(f)
        return {}
    
    def log_drift_warning(self, drift_results: Dict):
        """Log warning if drift detected"""
        if drift_results['overall_drift']:
            logger.warning(
                f"⚠️ DRIFT DETECTED: {drift_results['num_drifted_features']} "
                f"out of {drift_results['total_features']} features drifted "
                f"beyond {self.threshold*100}% threshold"
            )
            logger.warning(f"Drifted features: {', '.join(drift_results['drifted_features'])}")
        else:
            logger.info(
                f"✓ No significant drift detected. All features within "
                f"{self.threshold*100}% threshold"
            )


def monitor_drift_between_runs(current_data_path: str, 
                               previous_data_path: str,
                               threshold: float = 0.15) -> Dict:
    """
    Convenience function to monitor drift between two data files
    
    Args:
        current_data_path: Path to current processed data
        previous_data_path: Path to previous processed data
        threshold: Drift detection threshold
        
    Returns:
        Drift report dictionary
    """
    monitor = DriftMonitor(threshold=threshold)
    
    # Load data
    current_df = pd.read_csv(current_data_path)
    previous_df = pd.read_csv(previous_data_path)
    
    # Select numeric features only
    numeric_cols = current_df.select_dtypes(include=[np.number]).columns
    current_features = current_df[numeric_cols]
    previous_features = previous_df[numeric_cols]
    
    # Calculate drift
    drift_results = monitor.calculate_drift(current_features, previous_features)
    
    # Save report
    monitor.save_drift_report(drift_results)
    
    # Log warnings
    monitor.log_drift_warning(drift_results)
    
    return drift_results


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    print("Drift Monitoring Module")
    print("=" * 50)
    print("This module detects feature drift between training runs")
    print("Usage: Import and call monitor_drift_between_runs()")
