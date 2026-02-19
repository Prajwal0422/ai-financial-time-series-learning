"""
Statistical Validation
Performs statistical tests on data for validation
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from pathlib import Path


class StatisticalValidator:
    """
    Performs statistical validation tests on financial data.
    """
    
    def __init__(self):
        pass
    
    def test_stationarity(self, df, output_path='models/real_data/stationarity_report.csv'):
        """
        Perform Augmented Dickey-Fuller test on returns for each ticker.
        
        Args:
            df (pd.DataFrame): Dataframe with Log_Return column
            output_path (str): Path to save report
            
        Returns:
            pd.DataFrame: Stationarity test results
        """
        print(f"\n{'='*80}")
        print("STATISTICAL VALIDATION - STATIONARITY TESTS")
        print(f"{'='*80}")
        
        print(f"\nPerforming Augmented Dickey-Fuller tests on returns...")
        print(f"Null Hypothesis: Series has a unit root (non-stationary)")
        print(f"Alternative: Series is stationary")
        print(f"\n{'Ticker':>8} | {'ADF Stat':>10} | {'p-value':>10} | {'Stationary':>12}")
        print("─" * 50)
        
        results = []
        
        for ticker in df['Ticker'].unique():
            ticker_df = df[df['Ticker'] == ticker]
            
            # Get returns (drop NaN)
            returns = ticker_df['Log_Return'].dropna()
            
            if len(returns) < 10:
                print(f"{ticker:>8} | {'N/A':>10} | {'N/A':>10} | {'Too few':>12}")
                continue
            
            try:
                # Perform ADF test
                adf_result = adfuller(returns, autolag='AIC')
                
                adf_stat = adf_result[0]
                p_value = adf_result[1]
                is_stationary = p_value < 0.05
                
                results.append({
                    'Ticker': ticker,
                    'ADF_Statistic': adf_stat,
                    'p_value': p_value,
                    'Is_Stationary': is_stationary,
                    'Critical_Value_1%': adf_result[4]['1%'],
                    'Critical_Value_5%': adf_result[4]['5%'],
                    'Critical_Value_10%': adf_result[4]['10%']
                })
                
                status = "✓ Yes" if is_stationary else "✗ No"
                print(f"{ticker:>8} | {adf_stat:10.4f} | {p_value:10.4f} | {status:>12}")
                
            except Exception as e:
                print(f"{ticker:>8} | {'Error':>10} | {'Error':>10} | {'Error':>12}")
                continue
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        
        if not results_df.empty:
            # Save report
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            results_df.to_csv(output_file, index=False)
            
            # Summary
            stationary_count = results_df['Is_Stationary'].sum()
            total_count = len(results_df)
            
            print("─" * 50)
            print(f"\nSummary:")
            print(f"  Stationary series: {stationary_count}/{total_count}")
            print(f"  Non-stationary series: {total_count - stationary_count}/{total_count}")
            print(f"\n✓ Report saved to: {output_file}")
        
        print(f"{'='*80}\n")
        
        return results_df
    
    def test_normality(self, df, feature='Log_Return'):
        """
        Test normality of a feature using Shapiro-Wilk test.
        
        Args:
            df (pd.DataFrame): Dataframe with feature
            feature (str): Feature to test
            
        Returns:
            dict: Test results
        """
        from scipy import stats
        
        print(f"\n{'='*80}")
        print(f"NORMALITY TEST - {feature}")
        print(f"{'='*80}")
        
        data = df[feature].dropna()
        
        if len(data) > 5000:
            # Shapiro-Wilk test has limitations for large samples
            # Use a sample
            data = data.sample(5000, random_state=42)
            print(f"\nUsing sample of 5000 observations (original: {len(df[feature].dropna())})")
        
        stat, p_value = stats.shapiro(data)
        
        print(f"\nShapiro-Wilk Test:")
        print(f"  Statistic: {stat:.6f}")
        print(f"  p-value: {p_value:.6f}")
        print(f"  Normal: {'Yes' if p_value > 0.05 else 'No'} (α=0.05)")
        
        print(f"{'='*80}\n")
        
        return {
            'feature': feature,
            'statistic': stat,
            'p_value': p_value,
            'is_normal': p_value > 0.05
        }
    
    def get_feature_distributions(self, df, features):
        """
        Get distribution statistics for features.
        
        Args:
            df (pd.DataFrame): Dataframe with features
            features (list): List of features
            
        Returns:
            pd.DataFrame: Distribution statistics
        """
        stats_list = []
        
        for feature in features:
            if feature not in df.columns:
                continue
            
            data = df[feature].dropna()
            
            stats_list.append({
                'Feature': feature,
                'Mean': data.mean(),
                'Std': data.std(),
                'Min': data.min(),
                'Q25': data.quantile(0.25),
                'Median': data.median(),
                'Q75': data.quantile(0.75),
                'Max': data.max(),
                'Skewness': data.skew(),
                'Kurtosis': data.kurtosis()
            })
        
        return pd.DataFrame(stats_list)
