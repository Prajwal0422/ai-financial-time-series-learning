"""
Real-Time API Endpoints
Provides live stock data via REST API
"""

from flask import Blueprint, jsonify, request
from analysis.realtime_data import RealtimeDataFetcher, get_live_market_data
from datetime import datetime
import json

realtime_bp = Blueprint('realtime', __name__, url_prefix='/api/realtime')

# Global fetcher instance (cached)
_fetcher = None
_last_update = None
_cache_duration = 60  # seconds

DEFAULT_TICKERS = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT']


def get_fetcher():
    """Get or create fetcher instance."""
    global _fetcher
    if _fetcher is None:
        _fetcher = RealtimeDataFetcher(DEFAULT_TICKERS, update_interval=60)
    return _fetcher


@realtime_bp.route('/current', methods=['GET'])
def get_current_prices():
    """
    Get current prices for all tracked stocks.
    
    Returns:
        JSON with current price data
    """
    try:
        global _last_update
        
        # Check if cache is still valid
        now = datetime.now()
        if _last_update and (now - _last_update).seconds < _cache_duration:
            fetcher = get_fetcher()
            if fetcher.cache:
                return jsonify({
                    'success': True,
                    'data': fetcher.cache,
                    'cached': True,
                    'timestamp': _last_update.isoformat()
                })
        
        # Fetch fresh data
        fetcher = get_fetcher()
        data = fetcher.fetch_all_current_prices()
        _last_update = datetime.now()
        
        return jsonify({
            'success': True,
            'data': data,
            'cached': False,
            'timestamp': _last_update.isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@realtime_bp.route('/ticker/<ticker>', methods=['GET'])
def get_ticker_data(ticker):
    """
    Get current data for specific ticker.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        JSON with ticker data
    """
    try:
        fetcher = get_fetcher()
        data = fetcher.fetch_current_price(ticker.upper())
        
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No data available for {ticker}'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@realtime_bp.route('/summary', methods=['GET'])
def get_market_summary():
    """
    Get market summary statistics.
    
    Returns:
        JSON with market summary
    """
    try:
        fetcher = get_fetcher()
        
        # Ensure we have data
        if not fetcher.cache:
            fetcher.fetch_all_current_prices()
        
        summary = fetcher.get_market_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@realtime_bp.route('/intraday/<ticker>', methods=['GET'])
def get_intraday_data(ticker):
    """
    Get intraday data for specific ticker.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Query params:
        period (str): Data period (1d, 5d, 1mo)
        interval (str): Data interval (1m, 5m, 15m, 1h)
        
    Returns:
        JSON with intraday data
    """
    try:
        period = request.args.get('period', '1d')
        interval = request.args.get('interval', '5m')
        
        fetcher = get_fetcher()
        df = fetcher.fetch_latest_data(ticker.upper(), period=period, interval=interval)
        
        if df is not None:
            # Convert to JSON-serializable format
            data = df.to_dict(orient='records')
            
            # Convert timestamps to strings
            for record in data:
                if 'Date' in record:
                    record['Date'] = record['Date'].isoformat()
            
            return jsonify({
                'success': True,
                'ticker': ticker.upper(),
                'period': period,
                'interval': interval,
                'data': data,
                'count': len(data)
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No intraday data available for {ticker}'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@realtime_bp.route('/snapshot', methods=['POST'])
def save_snapshot():
    """
    Save current market snapshot to file.
    
    Returns:
        JSON with success status
    """
    try:
        fetcher = get_fetcher()
        fetcher.save_snapshot()
        
        return jsonify({
            'success': True,
            'message': 'Snapshot saved successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@realtime_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON with health status
    """
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_duration': _cache_duration,
        'last_update': _last_update.isoformat() if _last_update else None
    })
