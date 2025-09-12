from flask import render_template, jsonify, request
from app import app
from crypto_service import CryptoService
from ai_predictor import AIPredictor
from pattern_analyzer import PatternAnalyzer
import logging

# Initialize services
crypto_service = CryptoService()
ai_predictor = AIPredictor()
pattern_analyzer = PatternAnalyzer()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/predictions')
def predictions():
    """AI predictions page"""
    return render_template('predictions.html')

@app.route('/patterns')
def patterns():
    """Pattern analysis page"""
    return render_template('patterns.html')

@app.route('/defi')
def defi():
    """DeFi monitoring page"""
    return render_template('defi.html')

@app.route('/api/market-data')
def get_market_data():
    """API endpoint for real-time market data"""
    try:
        data = crypto_service.get_market_overview()
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching market data: {e}")
        return jsonify({'error': 'Failed to fetch market data'}), 500

@app.route('/api/coin-price/<coin_id>')
def get_coin_price(coin_id):
    """API endpoint for specific coin price data"""
    try:
        days = int(request.args.get('days', 7))
        data = crypto_service.get_coin_history(coin_id, days)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching coin price data: {e}")
        return jsonify({'error': 'Failed to fetch coin price data'}), 500

@app.route('/api/predictions/<coin_id>')
def get_predictions(coin_id):
    """API endpoint for AI price predictions"""
    try:
        historical_data = crypto_service.get_coin_history(coin_id, 30)
        predictions = ai_predictor.predict_price(historical_data)
        return jsonify(predictions)
    except Exception as e:
        logging.error(f"Error generating predictions: {e}")
        return jsonify({'error': 'Failed to generate predictions'}), 500

@app.route('/api/patterns/<coin_id>')
def get_patterns(coin_id):
    """API endpoint for pattern analysis"""
    try:
        historical_data = crypto_service.get_coin_history(coin_id, 30)
        patterns = pattern_analyzer.analyze_patterns(historical_data)
        return jsonify(patterns)
    except Exception as e:
        logging.error(f"Error analyzing patterns: {e}")
        return jsonify({'error': 'Failed to analyze patterns'}), 500

@app.route('/api/defi-protocols')
def get_defi_protocols():
    """API endpoint for DeFi protocol data"""
    try:
        data = crypto_service.get_defi_protocols()
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching DeFi data: {e}")
        return jsonify({'error': 'Failed to fetch DeFi protocol data'}), 500

@app.route('/api/trending')
def get_trending():
    """API endpoint for trending cryptocurrencies"""
    try:
        data = crypto_service.get_trending_coins()
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error fetching trending data: {e}")
        return jsonify({'error': 'Failed to fetch trending data'}), 500
