import os
import logging
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import setup_routes
from crypto_service import CryptoService
import time

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Create the FastAPI app
app = FastAPI(title="Blockchain Analytics Dashboard")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup routes
setup_routes(app)

# Import the crypto service for background updates
crypto_service = CryptoService()

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info('Client connected to WebSocket')

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logging.info('Client disconnected from WebSocket')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove failed connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

# Background task for sending live updates
background_task_running = False

async def background_price_updates():
    """Send price updates to all connected clients every 30 seconds"""
    global background_task_running
    background_task_running = True
    
    while background_task_running and manager.active_connections:
        try:
            # Get latest market data
            market_data = crypto_service.get_market_overview()
            await manager.broadcast(json.dumps({
                'type': 'price_update',
                'data': market_data
            }))
            
            # Get trending coins data
            trending_data = crypto_service.get_trending_coins()
            await manager.broadcast(json.dumps({
                'type': 'trending_update', 
                'data': trending_data
            }))
            
            # Sleep for 30 seconds before next update
            await asyncio.sleep(30)
        except Exception as e:
            logging.error(f"Error in background price updates: {e}")
            await asyncio.sleep(30)
    
    background_task_running = False

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Send initial status message
    await manager.send_personal_message(json.dumps({
        'type': 'status',
        'data': {'msg': 'Connected to live price feed'}
    }), websocket)
    
    # Start background task if not already running
    global background_task_running
    if not background_task_running:
        asyncio.create_task(background_price_updates())
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get('type')
            
            if message_type == 'subscribe_to_coin':
                coin_id = message.get('data', {}).get('coin_id')
                if coin_id:
                    logging.info(f'Client subscribed to {coin_id} updates')
                    await manager.send_personal_message(json.dumps({
                        'type': 'subscription_confirmed',
                        'data': {'coin_id': coin_id}
                    }), websocket)
            
            elif message_type == 'get_live_price':
                try:
                    coin_id = message.get('data', {}).get('coin_id', 'bitcoin')
                    
                    # Get current market data
                    market_data = crypto_service.get_market_overview()
                    
                    # Find the requested coin in the market data
                    coin_data = None
                    for coin in market_data.get('coins', []):
                        if coin['id'] == coin_id:
                            coin_data = coin
                            break
                    
                    if coin_data:
                        await manager.send_personal_message(json.dumps({
                            'type': 'live_price_response',
                            'data': {
                                'coin_id': coin_id,
                                'price': coin_data['current_price'],
                                'change_24h': coin_data['price_change_percentage_24h'],
                                'timestamp': int(time.time() * 1000)
                            }
                        }), websocket)
                    else:
                        await manager.send_personal_message(json.dumps({
                            'type': 'live_price_error',
                            'data': {'error': f'Coin {coin_id} not found'}
                        }), websocket)
                        
                except Exception as e:
                    logging.error(f"Error getting live price: {e}")
                    await manager.send_personal_message(json.dumps({
                        'type': 'live_price_error',
                        'data': {'error': 'Failed to fetch live price data'}
                    }), websocket)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
