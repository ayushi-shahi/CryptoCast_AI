#!/usr/bin/env python3
"""
Startup script for the Blockchain Analytics Dashboard with WebSocket support
"""
import os
from app import socketio, app

if __name__ == '__main__':
    # Use SocketIO server instead of regular Flask
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        use_reloader=True,
        log_output=True
    )