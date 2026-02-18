"""
Regime Insights Module
Generates interpretable summaries of what each regime represents
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path


def analyze_regime_characteristics(df, regime_col='Regime'):
    """
    Analyze characteristics of each regime.
    
    Args:
        df (pd.DataFrame): DataFrame with regime labels and features
        regime_col (str): Name of regime column
        
    Returns:
        dict: Regime characteristics
    """
    regimes = sorted(df[regime_col].unique())
    characteristics = {}
    
    # Features to analyze
    key_features = [
        'Log_Return', 'Simple_Return',
        'Volatility_10', 'Volatility_30',
        'Momentum_5', 'Momentum_10',
        'Price_to_MA10', 'Price_to_MA30'
    ]
    
    # Filter to available features
    available_features = [f for f in key_features if f in df.columns]
    
    for regime in regimes:
        regime_data = df[df[regime_col] == regime]
        
        char = {
            'regime_id': int(regime),
            'sample_count': len(regime_data),
            'percentage': float(len(regime_data) / len(df) * 100),
            'features': {}
        }
        
        # Analyze each feature
        for feature in available_features:
            feature_data = regime_data[feature].dropna()
            if len(feature_data) > 0:
                char['features'][feature] = {
                    'mean': float(feature_data.mean()),
                    'median': float(feature_data.median()),
                    'std': float(feature_data.std()),
                    'min': float(feature_data.min()),
                    'max': float(feature_data.max())
                }
        
        characteristics[f'regime_{regime}'] = char
    
    return characteristics


def generate_regime_interpretation(characteristics):
    """
    Generate human-readable interpretation of each regime.
    
    Args:
        characteristics (dict): Regime characteristics from analyze_regime_characteristics
        
    Returns:
        dict: Interpretations for each regime
    """
    interpretations = {}
    
    for regime_key, char in characteristics.items():
        regime_id = char['regime_id']
        features = char['features']
        
        # Extract key metrics
        avg_return = features.get('Log_Return', {}).get('mean', 0)
        avg_volatility = features.get('Volatility_10', {}).get('mean', 0)
        avg_momentum = features.get('Momentum_5', {}).get('mean', 0)
        
        # Classify regime based on characteristics
        interpretation = {
            'regime_id': regime_id,
            'sample_count': char['sample_count'],
            'percentage': char['percentage'],
            'label': '',
            'description': '',
            'characteristics': []
        }
        
        # Determine label based on return and volatility
        if avg_return > 0.001:
            if avg_volatility < 0.015:
                interpretation['label'] = 'Stable Growth'
                interpretation['description'] = 'Positive returns with low volatility - steady upward movement'
            else:
                interpretation['label'] = 'Volatile Growth'
                interpretation['description'] = 'Positive returns with high volatility - strong but unstable gains'
        elif avg_return < -0.001:
            if avg_volatility < 0.015:
                interpretation['label'] = 'Gradual Decline'
                interpretation['description'] = 'Negative returns with low volatility - slow downward trend'
            else:
                interpretation['label'] = 'Market Stress'
                interpretation['description'] = 'Negative returns with high volatility - significant downward pressure'
        else:
            if avg_volatility < 0.015:
                interpretation['label'] = 'Consolidation'
                interpretation['description'] = 'Flat returns with low volatility - sideways movement'
            else:
                interpretation['label'] = 'High Uncertainty'
                interpretation['description'] = 'Flat returns with high volatility - directionless but turbulent'
        
        # Add detailed characteristics
        if avg_return > 0:
            interpretation['characteristics'].append(f"Positive average return ({avg_return*100:.3f}%)")
        else:
            interpretation['characteristics'].append(f"Negative average return ({avg_return*100:.3f}%)")
        
        if avg_volatility > 0.02:
            interpretation['characteristics'].append(f"High volatility ({avg_volatility*100:.2f}%)")
        elif avg_volatility < 0.01:
            interpretation['characteristics'].append(f"Low volatility ({avg_volatility*100:.2f}%)")
        else:
            interpretation['characteristics'].append(f"Moderate volatility ({avg_volatility*100:.2f}%)")
        
        if avg_momentum > 0:
            interpretation['characteristics'].append("Positive momentum")
        elif avg_momentum < 0:
            interpretation['characteristics'].append("Negative momentum")
        
        # Add price position relative to MA
        if 'Price_to_MA10' in features:
            price_to_ma = features['Price_to_MA10']['mean']
            if price_to_ma > 1.02:
                interpretation['characteristics'].append("Price above moving average (bullish)")
            elif price_to_ma < 0.98:
                interpretation['characteristics'].append("Price below moving average (bearish)")
        
        interpretations[regime_key] = interpretation
    
    return interpretations


def create_regime_summary_report(df, regime_col='Regime'):
    """
    Create comprehensive regime summary report.
    
    Args:
        df (pd.DataFrame): DataFrame with regime labels and features
        regime_col (str): Name of regime column
        
    Returns:
        dict: Complete regime analysis report
    """
    print("\nGenerating Regime Insights...")
    print("=" * 60)
    
    # Analyze characteristics
    characteristics = analyze_regime_characteristics(df, regime_col)
    
    # Generate interpretations
    interpretations = generate_regime_interpretation(characteristics)
    
    # Create report
    report = {
        'total_samples': len(df),
        'n_regimes': len(characteristics),
        'characteristics': characteristics,
        'interpretations': interpretations
    }
    
    # Print summary
    print(f"\nIdentified {report['n_regimes']} distinct market regimes:")
    print("-" * 60)
    
    for regime_key in sorted(interpretations.keys()):
        interp = interpretations[regime_key]
        print(f"\nRegime {interp['regime_id']}: {interp['label']}")
        print(f"  Frequency: {interp['sample_count']:,} samples ({interp['percentage']:.1f}%)")
        print(f"  Description: {interp['description']}")
        print(f"  Characteristics:")
        for char in interp['characteristics']:
            print(f"    • {char}")
    
    print("=" * 60)
    
    return report


def save_regime_insights(report, output_path='models/regime_insights.json'):
    """
    Save regime insights report to JSON file.
    
    Args:
        report (dict): Report from create_regime_summary_report
        output_path (str): Path to save JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Regime insights saved to {output_file}")


def get_regime_interpretation(regime_id, insights_path='models/regime_insights.json'):
    """
    Get interpretation for a specific regime.
    
    Args:
        regime_id (int): Regime ID
        insights_path (str): Path to insights JSON file
        
    Returns:
        dict: Regime interpretation
    """
    insights_file = Path(insights_path)
    
    if not insights_file.exists():
        return None
    
    with open(insights_file, 'r') as f:
        report = json.load(f)
    
    regime_key = f'regime_{regime_id}'
    return report['interpretations'].get(regime_key)
