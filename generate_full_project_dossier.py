"""
Full Project Intelligence Extraction Tool
Comprehensive ML System Audit and Analysis
"""
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import pandas as pd
import pickle
from collections import defaultdict

class ProjectDossierGenerator:
    """Comprehensive project analysis and documentation generator"""
    
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root)
        self.report = []
        self.scores = {}
        self.stats = defaultdict(int)
        
    def add_section(self, title, level=1):
        """Add markdown section header"""
        self.report.append(f"\n{'#' * level} {title}\n")
    
    def add_content(self, content):
        """Add content to report"""
        self.report.append(f"{content}\n")
    
    def scan_repository(self):
        """Scan entire repository structure"""
        self.add_section("Repository Structure Analysis", 2)
        
        # Count files by type
        file_counts = defaultdict(int)
        total_lines = 0
        python_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden and cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                ext = Path(file).suffix
                file_counts[ext] += 1
                
                file_path = Path(root) / file
                
                # Count Python lines
                if ext == '.py':
                    python_files.append(str(file_path))
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = len(f.readlines())
                            total_lines += lines
                    except:
                        pass
        
        self.stats['total_python_files'] = file_counts['.py']
        self.stats['total_lines_of_code'] = total_lines
        
        self.add_content(f"**Total Files:** {sum(file_counts.values())}")
        self.add_content(f"**Python Files:** {file_counts['.py']}")
        self.add_content(f"**Total Lines of Code:** {total_lines:,}")
        self.add_content(f"**HTML Templates:** {file_counts['.html']}")
        self.add_content(f"**CSS Files:** {file_counts['.css']}")
        self.add_content(f"**JavaScript Files:** {file_counts['.js']}")
        self.add_content(f"**Markdown Docs:** {file_counts['.md']}")
        self.add_content(f"**CSV Data Files:** {file_counts['.csv']}")
        self.add_content(f"**JSON Config Files:** {file_counts['.json']}")
        
        # List key directories
        self.add_content("\n**Key Directories:**")
        key_dirs = ['analysis', 'api', 'ml', 'models', 'data', 'templates', 'static', 'tests', 'datasets']
        for dir_name in key_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                self.add_content(f"- ✅ `{dir_name}/`")
            else:
                self.add_content(f"- ❌ `{dir_name}/` (missing)")
        
        return python_files
    
    def analyze_data(self):
        """Analyze data files and structure"""
        self.add_section("Data Analysis", 2)
        
        data_dir = self.project_root / 'data' / 'real'
        
        if not data_dir.exists():
            self.add_content("⚠️ Data directory not found")
            self.scores['data'] = 0
            return
        
        csv_files = list(data_dir.glob('*.csv'))
        self.add_content(f"**CSV Files Found:** {len(csv_files)}")
        
        total_rows = 0
        date_ranges = []
        
        for csv_file in csv_files[:5]:  # Analyze first 5
            try:
                df = pd.read_csv(csv_file)
                total_rows += len(df)
                
                self.add_content(f"\n**{csv_file.name}:**")
                self.add_content(f"- Rows: {len(df):,}")
                self.add_content(f"- Columns: {list(df.columns)}")
                
                # Check OHLCV schema
                required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                has_schema = all(col in df.columns for col in required_cols)
                self.add_content(f"- OHLCV Schema: {'✅ Valid' if has_schema else '❌ Invalid'}")
                
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                    date_range = f"{df['Date'].min()} to {df['Date'].max()}"
                    self.add_content(f"- Date Range: {date_range}")
                    date_ranges.append(date_range)
            except Exception as e:
                self.add_content(f"- Error reading: {str(e)}")
        
        self.add_content(f"\n**Total Rows Across Files:** {total_rows:,}")
        self.stats['total_data_rows'] = total_rows
        
        # Score data
        score = 0
        if len(csv_files) > 0: score += 10
        if total_rows > 1000: score += 10
        self.scores['data'] = score
    
    def analyze_features(self):
        """Analyze feature engineering"""
        self.add_section("Feature Engineering Analysis", 2)
        
        # Check for processed data
        processed_files = list(self.project_root.glob('**/data_processed.csv'))
        
        if not processed_files:
            self.add_content("⚠️ No processed data files found")
            return
        
        try:
            df = pd.read_csv(processed_files[0])
            
            # Identify feature columns
            base_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            feature_cols = [col for col in df.columns if col not in base_cols]
            
            self.add_content(f"**Total Features Engineered:** {len(feature_cols)}")
            self.add_content(f"\n**Feature List:**")
            
            # Categorize features
            categories = {
                'Returns': ['return', 'log_return'],
                'Volatility': ['volatility', 'vol'],
                'Momentum': ['momentum', 'mom'],
                'Moving Averages': ['ma_', 'sma', 'ema'],
                'Technical': ['rsi', 'macd', 'bb_', 'bollinger'],
                'Volume': ['volume_'],
                'Price Ratios': ['price_to_']
            }
            
            for category, keywords in categories.items():
                matching = [col for col in feature_cols if any(kw in col.lower() for kw in keywords)]
                if matching:
                    self.add_content(f"\n**{category}:** ({len(matching)})")
                    for feat in matching[:10]:  # Show first 10
                        self.add_content(f"- {feat}")
            
            # Check NaN levels
            nan_pct = (df[feature_cols].isna().sum() / len(df) * 100).mean()
            self.add_content(f"\n**Average NaN %:** {nan_pct:.2f}%")
            
            self.stats['total_features'] = len(feature_cols)
            
        except Exception as e:
            self.add_content(f"Error analyzing features: {str(e)}")
    
    def analyze_ml_pipeline(self):
        """Analyze ML pipeline and models"""
        self.add_section("ML Pipeline Analysis", 2)
        
        # Find model directories
        model_dirs = list(self.project_root.glob('models/**/metadata.json'))
        
        if not model_dirs:
            self.add_content("⚠️ No model metadata found")
            self.scores['ml_pipeline'] = 0
            return
        
        # Analyze latest model
        latest_model = sorted(model_dirs, key=lambda x: x.stat().st_mtime, reverse=True)[0]
        
        try:
            with open(latest_model, 'r') as f:
                metadata = json.load(f)
            
            self.add_content(f"**Model Version:** {metadata.get('model_version', 'N/A')}")
            self.add_content(f"**Algorithm:** {metadata.get('model_type', 'KMeans')}")
            self.add_content(f"**Number of Clusters (K):** {metadata.get('n_clusters', 'N/A')}")
            self.add_content(f"**Training Timestamp:** {metadata.get('timestamp', 'N/A')}")
            self.add_content(f"**Total Samples:** {metadata.get('total_samples', 'N/A'):,}")
            
            # Metrics
            metrics = metadata.get('metrics', {})
            self.add_content(f"\n**Performance Metrics:**")
            self.add_content(f"- Silhouette Score: {metrics.get('silhouette_score', 'N/A')}")
            self.add_content(f"- Davies-Bouldin Index: {metrics.get('davies_bouldin_index', 'N/A')}")
            self.add_content(f"- Calinski-Harabasz Score: {metrics.get('calinski_harabasz_score', 'N/A')}")
            
            # Training config
            config = metadata.get('training_config', {})
            self.add_content(f"\n**Training Configuration:**")
            self.add_content(f"- Scaling: {config.get('scaling_method', 'StandardScaler')}")
            self.add_content(f"- PCA: {config.get('use_pca', False)}")
            if config.get('use_pca'):
                self.add_content(f"- PCA Components: {config.get('n_components', 'N/A')}")
            self.add_content(f"- Training Time: {config.get('training_time', 'N/A')}s")
            
            # Cluster distribution
            cluster_file = latest_model.parent / 'cluster_summary.csv'
            if cluster_file.exists():
                cluster_df = pd.read_csv(cluster_file)
                self.add_content(f"\n**Cluster Distribution:**")
                for _, row in cluster_df.iterrows():
                    self.add_content(f"- Cluster {row['Cluster']}: {row['Count']} samples ({row['Percentage']:.1f}%)")
            
            # Score ML pipeline
            score = 0
            if metadata.get('n_clusters'): score += 5
            if metrics.get('silhouette_score', 0) > 0.3: score += 5
            if config.get('use_pca'): score += 5
            if metadata.get('total_samples', 0) > 1000: score += 5
            self.scores['ml_pipeline'] = score
            
        except Exception as e:
            self.add_content(f"Error analyzing ML pipeline: {str(e)}")
            self.scores['ml_pipeline'] = 0
    
    def analyze_experiments(self):
        """Analyze experiment tracking"""
        self.add_section("Experiment Tracking", 2)
        
        exp_file = self.project_root / 'experiments_real.csv'
        
        if not exp_file.exists():
            self.add_content("⚠️ No experiment tracking file found")
            self.scores['experiments'] = 0
            return
        
        try:
            df = pd.read_csv(exp_file)
            
            self.add_content(f"**Total Experiments:** {len(df)}")
            self.add_content(f"**Tracked Metrics:** {list(df.columns)}")
            
            # Show last 3 experiments
            self.add_content(f"\n**Recent Experiments:**")
            for idx, row in df.tail(3).iterrows():
                self.add_content(f"\n**Experiment {idx + 1}:**")
                for col in df.columns:
                    self.add_content(f"- {col}: {row[col]}")
            
            # Score experiments
            score = 0
            if len(df) > 0: score += 5
            if len(df) > 5: score += 5
            self.scores['experiments'] = score
            
        except Exception as e:
            self.add_content(f"Error analyzing experiments: {str(e)}")
            self.scores['experiments'] = 0
    
    def analyze_drift(self):
        """Analyze drift monitoring"""
        self.add_section("Drift Monitoring", 2)
        
        drift_file = self.project_root / 'drift_report.json'
        
        if not drift_file.exists():
            self.add_content("⚠️ No drift monitoring found")
            self.scores['drift'] = 0
            return
        
        try:
            with open(drift_file, 'r') as f:
                drift_data = json.load(f)
            
            self.add_content(f"**Drift Report Generated:** {drift_data.get('timestamp', 'N/A')}")
            
            drifted = drift_data.get('drifted_features', [])
            self.add_content(f"**Drifted Features:** {len(drifted)}")
            
            if drifted:
                self.add_content("\n**Features with Drift:**")
                for feat in drifted[:10]:
                    self.add_content(f"- {feat}")
            
            # Score drift monitoring
            self.scores['drift'] = 10 if drift_file.exists() else 0
            
        except Exception as e:
            self.add_content(f"Error analyzing drift: {str(e)}")
            self.scores['drift'] = 0
    
    def analyze_tests(self):
        """Analyze test suite"""
        self.add_section("Test Suite Analysis", 2)
        
        test_dir = self.project_root / 'tests'
        
        if not test_dir.exists():
            self.add_content("⚠️ No test directory found")
            self.scores['testing'] = 0
            return
        
        test_files = list(test_dir.glob('test_*.py'))
        
        self.add_content(f"**Test Files:** {len(test_files)}")
        
        total_tests = 0
        for test_file in test_files:
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                    test_count = content.count('def test_')
                    total_tests += test_count
                    self.add_content(f"- {test_file.name}: {test_count} tests")
            except:
                pass
        
        self.add_content(f"\n**Total Tests:** {total_tests}")
        
        # Estimate coverage
        if total_tests > 0:
            coverage_estimate = min(100, (total_tests / self.stats.get('total_python_files', 1)) * 100)
            self.add_content(f"**Estimated Coverage:** ~{coverage_estimate:.0f}%")
        
        # Score testing
        score = 0
        if len(test_files) > 0: score += 5
        if total_tests > 10: score += 5
        self.scores['testing'] = score
    
    def analyze_frontend(self):
        """Analyze frontend components"""
        self.add_section("Frontend Analysis", 2)
        
        templates_dir = self.project_root / 'templates'
        static_dir = self.project_root / 'static'
        
        if templates_dir.exists():
            templates = list(templates_dir.glob('*.html'))
            self.add_content(f"**HTML Templates:** {len(templates)}")
            for tmpl in templates:
                self.add_content(f"- {tmpl.name}")
        
        if static_dir.exists():
            css_files = list(static_dir.glob('**/*.css'))
            js_files = list(static_dir.glob('**/*.js'))
            self.add_content(f"\n**CSS Files:** {len(css_files)}")
            self.add_content(f"**JavaScript Files:** {len(js_files)}")
        
        # Check for INR formatter
        app_file = self.project_root / 'app.py'
        if app_file.exists():
            with open(app_file, 'r') as f:
                content = f.read()
                has_inr = 'format_inr' in content
                self.add_content(f"\n**INR Formatter:** {'✅ Implemented' if has_inr else '❌ Not found'}")
        
        # Score frontend
        score = 0
        if templates_dir.exists() and len(templates) > 0: score += 5
        if static_dir.exists(): score += 5
        self.scores['frontend'] = score
    
    def analyze_backend(self):
        """Analyze backend and API"""
        self.add_section("Backend & API Analysis", 2)
        
        app_file = self.project_root / 'app.py'
        
        if not app_file.exists():
            self.add_content("⚠️ No app.py found")
            return
        
        try:
            with open(app_file, 'r') as f:
                content = f.read()
            
            # Extract routes
            routes = []
            for line in content.split('\n'):
                if '@app.route' in line:
                    routes.append(line.strip())
            
            self.add_content(f"**Flask Routes:** {len(routes)}")
            for route in routes:
                self.add_content(f"- {route}")
            
            # Check features
            features = {
                'Async Processing': 'run_async' in content,
                'Error Handling': 'try:' in content and 'except' in content,
                'Logging': 'log_event' in content,
                'Caching': 'lru_cache' in content or '_cache' in content,
                'Dataset Manager': 'DatasetManager' in content,
                'Auto Trainer': 'AutoTrainer' in content
            }
            
            self.add_content(f"\n**Backend Features:**")
            for feature, present in features.items():
                self.add_content(f"- {feature}: {'✅' if present else '❌'}")
            
        except Exception as e:
            self.add_content(f"Error analyzing backend: {str(e)}")
    
    def analyze_git(self):
        """Analyze git history"""
        self.add_section("Git History", 2)
        
        try:
            # Get total commits
            result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            total_commits = result.stdout.strip()
            self.add_content(f"**Total Commits:** {total_commits}")
            
            # Get branch name
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            branch = result.stdout.strip()
            self.add_content(f"**Current Branch:** {branch}")
            
            # Get remote origin
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            origin = result.stdout.strip()
            self.add_content(f"**Remote Origin:** {origin}")
            
            # Get last 10 commits
            result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            commits = result.stdout.strip().split('\n')
            
            self.add_content(f"\n**Recent Commits:**")
            for commit in commits:
                self.add_content(f"- {commit}")
            
            self.scores['versioning'] = 10
            
        except Exception as e:
            self.add_content(f"Git analysis unavailable: {str(e)}")
            self.scores['versioning'] = 0
    
    def calculate_completion(self):
        """Calculate overall completion score"""
        self.add_section("Project Completion Score", 2)
        
        # Define scoring weights
        weights = {
            'data': 20,
            'ml_pipeline': 20,
            'experiments': 10,
            'drift': 10,
            'testing': 10,
            'frontend': 10,
            'documentation': 10,
            'versioning': 10
        }
        
        # Calculate documentation score
        doc_files = list(self.project_root.glob('*.md'))
        self.scores['documentation'] = min(10, len(doc_files))
        
        # Calculate total
        total_score = 0
        max_score = sum(weights.values())
        
        self.add_content("**Component Scores:**")
        for component, weight in weights.items():
            score = self.scores.get(component, 0)
            percentage = (score / weight) * 100 if weight > 0 else 0
            self.add_content(f"- {component.replace('_', ' ').title()}: {score}/{weight} ({percentage:.0f}%)")
            total_score += score
        
        completion_pct = (total_score / max_score) * 100
        self.add_content(f"\n**Overall Completion: {completion_pct:.1f}%**")
        
        # Classification
        if completion_pct >= 90:
            classification = "🏆 Production-Ready"
        elif completion_pct >= 70:
            classification = "🚀 Advanced Development"
        elif completion_pct >= 50:
            classification = "⚙️ Active Development"
        else:
            classification = "🔨 Early Stage"
        
        self.add_content(f"**System Classification:** {classification}")
        
        return completion_pct
    
    def generate_strengths_weaknesses(self):
        """Generate strengths and weaknesses"""
        self.add_section("Strengths", 2)
        
        strengths = []
        
        if self.scores.get('ml_pipeline', 0) >= 15:
            strengths.append("✅ **Robust ML Pipeline** - Well-structured clustering with proper evaluation metrics")
        
        if self.scores.get('data', 0) >= 15:
            strengths.append("✅ **Comprehensive Data** - Multiple datasets with proper OHLCV schema")
        
        if self.stats.get('total_features', 0) > 15:
            strengths.append("✅ **Rich Feature Engineering** - 15+ technical indicators for analysis")
        
        if self.scores.get('frontend', 0) >= 8:
            strengths.append("✅ **Professional Frontend** - Premium dark theme with modern UI/UX")
        
        if self.scores.get('versioning', 0) >= 8:
            strengths.append("✅ **Version Control** - Active git repository with commit history")
        
        if self.scores.get('experiments', 0) >= 5:
            strengths.append("✅ **Experiment Tracking** - Systematic logging of model experiments")
        
        for strength in strengths:
            self.add_content(strength)
        
        self.add_section("Weaknesses & Missing Components", 2)
        
        weaknesses = []
        
        if self.scores.get('testing', 0) < 8:
            weaknesses.append("⚠️ **Limited Test Coverage** - Need more comprehensive unit and integration tests")
        
        if self.scores.get('drift', 0) < 8:
            weaknesses.append("⚠️ **Drift Monitoring** - Limited or missing drift detection system")
        
        if not (self.project_root / 'Dockerfile').exists():
            weaknesses.append("❌ **No Containerization** - Missing Docker setup for deployment")
        
        if not (self.project_root / '.github').exists():
            weaknesses.append("❌ **No CI/CD** - Missing automated testing and deployment pipeline")
        
        if not (self.project_root / 'requirements-dev.txt').exists():
            weaknesses.append("⚠️ **Development Dependencies** - No separate dev requirements file")
        
        if not (self.project_root / 'docs').exists():
            weaknesses.append("⚠️ **API Documentation** - Missing dedicated API documentation")
        
        for weakness in weaknesses:
            self.add_content(weakness)
    
    def generate_recommendations(self):
        """Generate improvement recommendations"""
        self.add_section("Recommendations", 2)
        
        self.add_content("### Immediate Priorities")
        self.add_content("1. **Increase Test Coverage** - Add unit tests for all core modules")
        self.add_content("2. **Implement CI/CD** - Set up GitHub Actions for automated testing")
        self.add_content("3. **Add Containerization** - Create Dockerfile for easy deployment")
        self.add_content("4. **Enhance Drift Monitoring** - Implement real-time drift detection")
        
        self.add_content("\n### Next-Level Improvements")
        self.add_content("1. **Cloud Deployment** - Deploy to AWS/GCP/Azure")
        self.add_content("2. **API Documentation** - Add Swagger/OpenAPI specs")
        self.add_content("3. **Performance Monitoring** - Implement APM (Application Performance Monitoring)")
        self.add_content("4. **Model Registry** - Use MLflow or similar for model versioning")
        self.add_content("5. **A/B Testing Framework** - Compare model versions in production")
        self.add_content("6. **Real-time Predictions** - Add streaming data support")
        self.add_content("7. **Multi-model Support** - Implement ensemble methods")
        self.add_content("8. **Advanced Visualizations** - Add interactive Plotly dashboards")
    
    def generate_dossier(self):
        """Generate complete project dossier"""
        print("🔍 Starting comprehensive project analysis...")
        
        # Header
        self.add_section("AI Financial Time-Series Analysis System", 1)
        self.add_section("Full Project Technical Dossier", 1)
        self.add_content(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.add_content(f"**Analyst:** ML Systems Architect & Technical Auditor")
        
        # Executive Summary
        self.add_section("Executive Summary", 1)
        
        # Run all analyses
        print("📊 Scanning repository...")
        python_files = self.scan_repository()
        
        print("📈 Analyzing data...")
        self.analyze_data()
        
        print("🔧 Analyzing features...")
        self.analyze_features()
        
        print("🤖 Analyzing ML pipeline...")
        self.analyze_ml_pipeline()
        
        print("📝 Analyzing experiments...")
        self.analyze_experiments()
        
        print("🔄 Analyzing drift monitoring...")
        self.analyze_drift()
        
        print("🧪 Analyzing tests...")
        self.analyze_tests()
        
        print("🎨 Analyzing frontend...")
        self.analyze_frontend()
        
        print("⚙️ Analyzing backend...")
        self.analyze_backend()
        
        print("📚 Analyzing git history...")
        self.analyze_git()
        
        print("📊 Calculating completion score...")
        completion = self.calculate_completion()
        
        print("💪 Generating strengths & weaknesses...")
        self.generate_strengths_weaknesses()
        
        print("💡 Generating recommendations...")
        self.generate_recommendations()
        
        # Write to file
        output_file = self.project_root / 'FULL_PROJECT_DOSSIER.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(self.report))
        
        print(f"\n✅ Dossier generated: {output_file}")
        print(f"📊 Project Completion: {completion:.1f}%")
        print(f"📄 Total Lines Analyzed: {self.stats.get('total_lines_of_code', 0):,}")
        
        return output_file

if __name__ == "__main__":
    generator = ProjectDossierGenerator()
    output_file = generator.generate_dossier()
    print(f"\n🎉 Analysis complete! Check {output_file}")
