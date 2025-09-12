import os
import logging
from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import time

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize Socket.IO with threading mode for better compatibility
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Import the blueprint from routes.py
from routes import routes   # ✅ import Blueprint
app.register_blueprint(routes)  # ✅ register it with the app

# Import the crypto service for background updates
from crypto_service import CryptoService

# Background thread for sending live updates
background_thread = None
thread_lock = threading.Lock()

def background_price_updates():
    """Send price updates to all connected clients every 30 seconds"""
    crypto_service = CryptoService()
    while True:
        try:
            # Get latest market data
            market_data = crypto_service.get_market_overview()
            socketio.emit("price_update", market_data, namespace="/")

            # Get trending coins data
            trending_data = crypto_service.get_trending_coins()
            socketio.emit("trending_update", trending_data, namespace="/")

            # Sleep for 30 seconds before next update
            time.sleep(30)
        except Exception as e:
            logging.error(f"Error in background price updates: {e}")
            time.sleep(30)

@socketio.on("connect")
def handle_connect():
    """Handle client connection"""
    logging.info("Client connected to WebSocket")
    emit("status", {"msg": "Connected to live price feed"})

    # Start background thread if not already running
    global background_thread
    with thread_lock:
        if background_thread is None:
            background_thread = socketio.start_background_task(background_price_updates)

@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection"""
    logging.info("Client disconnected from WebSocket")

@socketio.on("subscribe_to_coin")
def handle_coin_subscription(data):
    """Handle subscription to specific coin updates"""
    coin_id = data.get("coin_id")
    if coin_id:
        logging.info(f"Client subscribed to {coin_id} updates")
        emit("subscription_confirmed", {"coin_id": coin_id})

@socketio.on("get_live_price")
def handle_live_price_request(data):
    """Handle request for immediate price data"""
    try:
        coin_id = data.get("coin_id", "bitcoin")
        crypto_service = CryptoService()

        # Get current market data
        market_data = crypto_service.get_market_overview()

        # Find the requested coin in the market data
        coin_data = None
        for coin in market_data.get("coins", []):
            if coin["id"] == coin_id:
                coin_data = coin
                break

        if coin_data:
            emit("live_price_response", {
                "coin_id": coin_id,
                "price": coin_data["current_price"],
                "change_24h": coin_data["price_change_percentage_24h"],
                "timestamp": int(time.time() * 1000)
            })
        else:
            emit("live_price_error", {"error": f"Coin {coin_id} not found"})

    except Exception as e:
        logging.error(f"Error getting live price: {e}")
        emit("live_price_error", {"error": "Failed to fetch live price data"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
