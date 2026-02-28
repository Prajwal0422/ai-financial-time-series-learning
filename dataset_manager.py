"""
Dataset Manager - Handles dataset upload, validation, processing, and registry
"""
import os
import json
import pandas as pd
import pdfplumber
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetManager:
    """Manages dataset lifecycle: upload, validation, processing, registration"""
    
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'pdf'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    REQUIRED_COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    def __init__(self, base_dir='datasets'):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.registry_path = self.base_dir / 'datasets_registry.json'
        self._init_registry()
    
    def _init_registry(self):
        """Initialize registry file if not exists"""
        if not self.registry_path.exists():
            with open(self.registry_path, 'w') as f:
                json.dump({}, f, indent=2)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def validate_dataset_name(self, dataset_name):
        """Validate dataset name"""
        if not dataset_name or len(dataset_name.strip()) == 0:
            return False, "Dataset name cannot be empty"
        
        if len(dataset_name) > 50:
            return False, "Dataset name too long (max 50 characters)"
        
        # Check for invalid characters
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in dataset_name for char in invalid_chars):
            return False, f"Dataset name contains invalid characters: {invalid_chars}"
        
        # Check if already exists
        if self.dataset_exists(dataset_name):
            return False, f"Dataset '{dataset_name}' already exists"
        
        return True, "Valid"
    
    def dataset_exists(self, dataset_name):
        """Check if dataset already exists"""
        dataset_path = self.base_dir / dataset_name
        return dataset_path.exists()
    
    def create_dataset_structure(self, dataset_name):
        """Create directory structure for dataset"""
        dataset_path = self.base_dir / dataset_name
        
        # Create subdirectories
        (dataset_path / 'raw').mkdir(parents=True, exist_ok=True)
        (dataset_path / 'processed').mkdir(parents=True, exist_ok=True)
        (dataset_path / 'models').mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created directory structure for {dataset_name}")
        return dataset_path
    
    def parse_csv(self, file_path):
        """Parse CSV file"""
        try:
            df = pd.read_csv(file_path)
            return df, None
        except Exception as e:
            return None, f"CSV parsing error: {str(e)}"
    
    def parse_excel(self, file_path):
        """Parse Excel file"""
        try:
            df = pd.read_excel(file_path)
            return df, None
        except Exception as e:
            return None, f"Excel parsing error: {str(e)}"
    
    def parse_pdf(self, file_path):
        """Parse PDF file and extract tables"""
        try:
            tables = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        tables.append(table)
            
            if not tables:
                return None, "No tables found in PDF"
            
            # Convert first table to DataFrame
            df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
            return df, None
        except Exception as e:
            return None, f"PDF parsing error: {str(e)}"
    
    def parse_file(self, file_path, file_extension):
        """Parse file based on extension"""
        if file_extension == 'csv':
            return self.parse_csv(file_path)
        elif file_extension == 'xlsx':
            return self.parse_excel(file_path)
        elif file_extension == 'pdf':
            return self.parse_pdf(file_path)
        else:
            return None, f"Unsupported file type: {file_extension}"
    
    def validate_dataframe(self, df):
        """Validate DataFrame has required columns"""
        if df is None or df.empty:
            return False, "DataFrame is empty"
        
        # Check required columns
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {missing_cols}"
        
        # Check data types
        try:
            # Try to convert Date column
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Check numeric columns
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Check for too many NaN values
            if df[numeric_cols].isna().sum().sum() > len(df) * 0.5:
                return False, "Too many invalid numeric values in dataset"
            
        except Exception as e:
            return False, f"Data validation error: {str(e)}"
        
        return True, "Valid"
    
    def save_raw_data(self, df, dataset_name, original_filename):
        """Save raw data to dataset directory"""
        dataset_path = self.base_dir / dataset_name / 'raw'
        
        # Save as CSV
        csv_path = dataset_path / 'data.csv'
        df.to_csv(csv_path, index=False)
        
        # Save metadata
        metadata = {
            'original_filename': original_filename,
            'uploaded_at': datetime.now().isoformat(),
            'rows': len(df),
            'columns': list(df.columns)
        }
        
        metadata_path = dataset_path / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved raw data for {dataset_name}")
        return csv_path
    
    def register_dataset(self, dataset_name, metadata):
        """Register dataset in registry"""
        registry = self.load_registry()
        
        registry[dataset_name] = {
            'created_at': datetime.now().isoformat(),
            'sample_count': metadata.get('sample_count', 0),
            'cluster_count': metadata.get('cluster_count', 0),
            'silhouette_score': metadata.get('silhouette_score', 0.0),
            'model_version': metadata.get('model_version', 'v1'),
            'status': metadata.get('status', 'uploaded')
        }
        
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
        
        logger.info(f"Registered dataset: {dataset_name}")
    
    def load_registry(self):
        """Load dataset registry"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_all_datasets(self):
        """Get list of all registered datasets"""
        registry = self.load_registry()
        return list(registry.keys())
    
    def get_dataset_info(self, dataset_name):
        """Get information about a specific dataset"""
        registry = self.load_registry()
        return registry.get(dataset_name, None)
    
    def update_dataset_status(self, dataset_name, status, additional_info=None):
        """Update dataset status in registry"""
        registry = self.load_registry()
        
        if dataset_name in registry:
            registry[dataset_name]['status'] = status
            registry[dataset_name]['updated_at'] = datetime.now().isoformat()
            
            if additional_info:
                registry[dataset_name].update(additional_info)
            
            with open(self.registry_path, 'w') as f:
                json.dump(registry, f, indent=2)
            
            logger.info(f"Updated {dataset_name} status to: {status}")
