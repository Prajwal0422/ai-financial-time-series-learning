"""
Data Drift Monitor
Detects data drift between model versions
"""

import json
import numpy as np
from pathlib import Path


class DriftMonitor:
    """
    Monitors data drift between model versions.
    """
    
    def __init__(self, threshold=0.1):
        """
        Initialize drift monitor.
        
        Args:
            threshold (float): Threshold for drift detection (default: 0.1 = 10%)
        """
        self.threshold = threshold
    
    def calculate_drift(self, current_means, previous_means):
        """
        Calculate drift between current and previous feature means.
        
        Args:
            current_means (dict): Current feature means
            previous_means (dict): Previous feature means
            
        Returns:
            dict: Drift analysis results
        """
        if previous_means is None:
            return {
                'has_drift': False,
                'message': 'No previous model to compare',
                'drifted_features': []
            }
        
        drifted_features = []
        drift_scores = {}
        
        for feature in current_means.keys():
            if feature not in previous_means:
                continue
            
            current_val = current_means[feature]
            previous_val = previous_means[feature]
            
            # Calculate relative change
            if abs(previous_val) > 1e-10:
                drift_score = abs((current_val - previous_val) / previous_val)
            else:
                drift_score = abs(current_val - previous_val)
            
            drift_scores[feature] = drift_score
            
            if drift_score > self.threshold:
                drifted_features.append({
                    'feature': feature,
                    'drift_score': drift_score,
                    'current_mean': current_val,
                    'previous_mean': previous_val,
                    'change_pct': drift_score * 100
                })
        
        has_drift = len(drifted_features) > 0
        
        return {
            'has_drift': has_drift,
            'num_drifted_features': len(drifted_features),
            'drifted_features': drifted_features,
            'drift_scores': drift_scores,
            'threshold': self.threshold
        }
    
    def check_drift(self, current_feature_stats, version_manager):
        """
        Check for drift against previous model version.
        
        Args:
            current_feature_stats (dict): Current feature statistics
            version_manager: ModelVersionManager instance
            
        Returns:
            dict: Drift analysis results
        """
        print(f"\n{'='*80}")
        print("DATA DRIFT DETECTION")
        print(f"{'='*80}")
        
        current_version = version_manager.get_current_version()
        
        if current_version == 0:
            print("\nNo previous model version to compare.")
            print(f"{'='*80}\n")
            return {
                'has_drift': False,
                'message': 'First model version'
            }
        
        # Load previous version
        try:
            _, _, _, _, prev_metadata = version_manager.load_model_version(current_version)
            
            # Get previous feature means from training config
            prev_config = prev_metadata.get('training_config', {})
            prev_feature_stats = prev_config.get('feature_statistics', {})
            prev_means = prev_feature_stats.get('feature_means', {})
            
            if not prev_means:
                print("\nNo previous feature statistics available.")
                print(f"{'='*80}\n")
                return {
                    'has_drift': False,
                    'message': 'No previous statistics'
                }
            
            # Calculate drift
            current_means = current_feature_stats.get('feature_means', {})
            drift_result = self.calculate_drift(current_means, prev_means)
            
            # Print results
            print(f"\nComparing with version {current_version}")
            print(f"Drift threshold: {self.threshold * 100:.1f}%")
            
            if drift_result['has_drift']:
                print(f"\n⚠ DRIFT DETECTED!")
                print(f"  Drifted features: {drift_result['num_drifted_features']}")
                print(f"\n{'Feature':>20} | {'Drift %':>10} | {'Current':>12} | {'Previous':>12}")
                print("─" * 60)
                
                for drift_info in drift_result['drifted_features']:
                    print(f"{drift_info['feature']:>20} | {drift_info['change_pct']:9.2f}% | "
                          f"{drift_info['current_mean']:12.6f} | {drift_info['previous_mean']:12.6f}")
            else:
                print(f"\n✓ No significant drift detected")
                print(f"  All features within {self.threshold * 100:.1f}% threshold")
            
            print(f"{'='*80}\n")
            
            return drift_result
            
        except Exception as e:
            print(f"\n✗ Error checking drift: {str(e)}")
            print(f"{'='*80}\n")
            return {
                'has_drift': False,
                'message': f'Error: {str(e)}'
            }
    
    def save_drift_report(self, drift_result, output_path='models/real_data/drift_report.json'):
        """
        Save drift report to JSON file.
        
        Args:
            drift_result (dict): Drift analysis results
            output_path (str): Path to save report
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(drift_result, f, indent=2)
        
        print(f"✓ Drift report saved to: {output_file}")
