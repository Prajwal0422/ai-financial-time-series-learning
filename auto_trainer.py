"""
Auto Trainer - Automated ML pipeline for dataset processing and model training
"""
import os
import json
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoTrainer:
    """Automated feature engineering and model training pipeline"""
    
    def __init__(self, dataset_name, base_dir='datasets'):
        self.dataset_name = dataset_name
        self.base_dir = Path(base_dir)
        self.dataset_path = self.base_dir / dataset_name
        self.raw_path = self.dataset_path / 'raw'
        self.processed_path = self.dataset_path / 'processed'
        self.models_path = self.dataset_path / 'models'
    
    def engineer_features(self, df):
        """Apply feature engineering pipeline"""
        logger.info(f"Starting feature engineering for {self.dataset_name}")
        
        # Ensure Date is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Calculate returns
        df['returns'] = df['Close'].pct_change()
        df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Volatility features
        df['volatility_5'] = df['returns'].rolling(window=5).std()
        df['volatility_10'] = df['returns'].rolling(window=10).std()
        df['volatility_20'] = df['returns'].rolling(window=20).std()
        
        # Price momentum
        df['momentum_5'] = df['Close'].pct_change(periods=5)
        df['momentum_10'] = df['Close'].pct_change(periods=10)
        df['momentum_20'] = df['Close'].pct_change(periods=20)
        
        # Moving averages
        df['ma_5'] = df['Close'].rolling(window=5).mean()
        df['ma_10'] = df['Close'].rolling(window=10).mean()
        df['ma_20'] = df['Close'].rolling(window=20).mean()
        df['ma_50'] = df['Close'].rolling(window=50).mean()
        
        # Price relative to moving averages
        df['price_to_ma5'] = df['Close'] / df['ma_5']
        df['price_to_ma20'] = df['Close'] / df['ma_20']
        
        # Volume features
        df['volume_ma_5'] = df['Volume'].rolling(window=5).mean()
        df['volume_ratio'] = df['Volume'] / df['volume_ma_5']
        
        # High-Low range
        df['hl_range'] = (df['High'] - df['Low']) / df['Close']
        df['oc_range'] = (df['Close'] - df['Open']) / df['Open']
        
        # RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_position'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_diff'] = df['macd'] - df['macd_signal']
        
        # Drop NaN rows
        initial_rows = len(df)
        df = df.dropna()
        dropped_rows = initial_rows - len(df)
        
        logger.info(f"Feature engineering complete. Dropped {dropped_rows} rows with NaN values")
        logger.info(f"Final dataset shape: {df.shape}")
        
        return df
    
    def save_processed_data(self, df):
        """Save processed data"""
        processed_file = self.processed_path / 'data_processed.csv'
        df.to_csv(processed_file, index=False)
        logger.info(f"Saved processed data to {processed_file}")
        return processed_file
    
    def select_features_for_clustering(self, df):
        """Select relevant features for clustering"""
        feature_cols = [
            'returns', 'log_returns',
            'volatility_5', 'volatility_10', 'volatility_20',
            'momentum_5', 'momentum_10', 'momentum_20',
            'price_to_ma5', 'price_to_ma20',
            'volume_ratio', 'hl_range', 'oc_range',
            'rsi', 'bb_position',
            'macd', 'macd_signal', 'macd_diff'
        ]
        
        # Filter to only existing columns
        available_features = [col for col in feature_cols if col in df.columns]
        
        X = df[available_features].copy()
        
        # Handle any remaining NaN
        X = X.fillna(X.mean())
        
        logger.info(f"Selected {len(available_features)} features for clustering")
        return X, available_features
    
    def train_clustering_model(self, X, k_range=(3, 9), use_pca=True, n_components=10):
        """Train clustering model with optimal K selection"""
        logger.info("Starting clustering model training")
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Optional PCA
        pca = None
        if use_pca and X_scaled.shape[1] > n_components:
            pca = PCA(n_components=n_components)
            X_transformed = pca.fit_transform(X_scaled)
            logger.info(f"Applied PCA: {X_scaled.shape[1]} -> {n_components} components")
            logger.info(f"Explained variance: {pca.explained_variance_ratio_.sum():.3f}")
        else:
            X_transformed = X_scaled
        
        # Find optimal K
        silhouette_scores = {}
        models = {}
        
        for k in range(k_range[0], k_range[1]):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_transformed)
            score = silhouette_score(X_transformed, labels)
            silhouette_scores[k] = score
            models[k] = kmeans
            logger.info(f"K={k}: Silhouette Score = {score:.4f}")
        
        # Select best K
        best_k = max(silhouette_scores, key=silhouette_scores.get)
        best_score = silhouette_scores[best_k]
        best_model = models[best_k]
        
        logger.info(f"Best K={best_k} with Silhouette Score={best_score:.4f}")
        
        # Get final predictions
        labels = best_model.predict(X_transformed)
        
        return {
            'model': best_model,
            'scaler': scaler,
            'pca': pca,
            'labels': labels,
            'best_k': best_k,
            'silhouette_score': best_score,
            'all_scores': silhouette_scores,
            'X_transformed': X_transformed
        }
    
    def save_model_artifacts(self, results, feature_names):
        """Save all model artifacts"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        version_dir = self.models_path / f'v_{timestamp}'
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_path = version_dir / 'model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(results['model'], f)
        
        # Save scaler
        scaler_path = version_dir / 'scaler.pkl'
        with open(scaler_path, 'wb') as f:
            pickle.dump(results['scaler'], f)
        
        # Save PCA if used
        if results['pca'] is not None:
            pca_path = version_dir / 'pca.pkl'
            with open(pca_path, 'wb') as f:
                pickle.dump(results['pca'], f)
        
        # Save metadata
        metadata = {
            'timestamp': timestamp,
            'best_k': int(results['best_k']),
            'silhouette_score': float(results['silhouette_score']),
            'feature_names': feature_names,
            'n_samples': len(results['labels']),
            'use_pca': results['pca'] is not None,
            'model_version': f'v_{timestamp}'
        }
        
        metadata_path = version_dir / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save K comparison
        k_comparison = pd.DataFrame([
            {'k': k, 'silhouette_score': score}
            for k, score in results['all_scores'].items()
        ])
        k_comparison_path = version_dir / 'k_comparison.csv'
        k_comparison.to_csv(k_comparison_path, index=False)
        
        # Save cluster summary
        cluster_summary = pd.DataFrame({
            'cluster': range(results['best_k']),
            'count': pd.Series(results['labels']).value_counts().sort_index().values
        })
        cluster_summary_path = version_dir / 'cluster_summary.csv'
        cluster_summary.to_csv(cluster_summary_path, index=False)
        
        logger.info(f"Saved all model artifacts to {version_dir}")
        
        return {
            'version_dir': str(version_dir),
            'model_version': f'v_{timestamp}',
            'metadata': metadata
        }
    
    def run_full_pipeline(self):
        """Run complete training pipeline"""
        try:
            logger.info(f"Starting full pipeline for {self.dataset_name}")
            
            # Load raw data
            raw_file = self.raw_path / 'data.csv'
            if not raw_file.exists():
                raise FileNotFoundError(f"Raw data not found: {raw_file}")
            
            df = pd.read_csv(raw_file)
            logger.info(f"Loaded raw data: {df.shape}")
            
            # Feature engineering
            df_processed = self.engineer_features(df)
            
            # Save processed data
            self.save_processed_data(df_processed)
            
            # Select features
            X, feature_names = self.select_features_for_clustering(df_processed)
            
            # Train model
            results = self.train_clustering_model(X)
            
            # Save artifacts
            artifact_info = self.save_model_artifacts(results, feature_names)
            
            # Prepare return info
            pipeline_result = {
                'success': True,
                'dataset_name': self.dataset_name,
                'sample_count': len(df_processed),
                'cluster_count': results['best_k'],
                'silhouette_score': results['silhouette_score'],
                'model_version': artifact_info['model_version'],
                'version_dir': artifact_info['version_dir']
            }
            
            logger.info(f"Pipeline completed successfully for {self.dataset_name}")
            return pipeline_result
            
        except Exception as e:
            logger.error(f"Pipeline failed for {self.dataset_name}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'dataset_name': self.dataset_name
            }
