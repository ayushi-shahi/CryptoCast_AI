from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from crypto_service import CryptoService
from ai_predictor import AIPredictor
from pattern_analyzer import PatternAnalyzer
import logging

# Initialize services
crypto_service = CryptoService()
ai_predictor = AIPredictor()
pattern_analyzer = PatternAnalyzer()

def setup_routes(app: FastAPI):
    """Setup all routes for the FastAPI application"""
    
    # Initialize templates
    templates = Jinja2Templates(directory="templates")
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        """Main dashboard page"""
        return templates.TemplateResponse("dashboard.html", {"request": request})

    @app.get("/predictions", response_class=HTMLResponse)
    async def predictions(request: Request):
        """AI predictions page"""
        return templates.TemplateResponse("predictions.html", {"request": request})

    @app.get("/patterns", response_class=HTMLResponse)
    async def patterns(request: Request):
        """Pattern analysis page"""
        return templates.TemplateResponse("patterns.html", {"request": request})

    @app.get("/defi", response_class=HTMLResponse)
    async def defi(request: Request):
        """DeFi monitoring page"""
        return templates.TemplateResponse("defi.html", {"request": request})

    @app.get("/api/market-data")
    async def get_market_data():
        """API endpoint for real-time market data"""
        try:
            data = crypto_service.get_market_overview()
            return data
        except Exception as e:
            logging.error(f"Error fetching market data: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch market data")

    @app.get("/api/coin-price/{coin_id}")
    async def get_coin_price(coin_id: str, days: int = Query(default=7)):
        """API endpoint for specific coin price data"""
        try:
            data = crypto_service.get_coin_history(coin_id, days)
            return data
        except Exception as e:
            logging.error(f"Error fetching coin price data: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch coin price data")

    @app.get("/api/predictions/{coin_id}")
    async def get_predictions(coin_id: str):
        """API endpoint for AI price predictions"""
        try:
            historical_data = crypto_service.get_coin_history(coin_id, 30)
            predictions = ai_predictor.predict_price(historical_data)
            return predictions
        except Exception as e:
            logging.error(f"Error generating predictions: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate predictions")

    @app.get("/api/patterns/{coin_id}")
    async def get_patterns(coin_id: str):
        """API endpoint for pattern analysis"""
        try:
            historical_data = crypto_service.get_coin_history(coin_id, 30)
            patterns = pattern_analyzer.analyze_patterns(historical_data)
            return patterns
        except Exception as e:
            logging.error(f"Error analyzing patterns: {e}")
            raise HTTPException(status_code=500, detail="Failed to analyze patterns")

    @app.get("/api/defi-protocols")
    async def get_defi_protocols():
        """API endpoint for DeFi protocol data"""
        try:
            data = crypto_service.get_defi_protocols()
            return data
        except Exception as e:
            logging.error(f"Error fetching DeFi data: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch DeFi protocol data")

    @app.get("/api/trending")
    async def get_trending():
        """API endpoint for trending cryptocurrencies"""
        try:
            data = crypto_service.get_trending_coins()
            return data
        except Exception as e:
            logging.error(f"Error fetching trending data: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch trending data")
