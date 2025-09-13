#!/usr/bin/env python3
"""
Startup script for the Blockchain Analytics Dashboard with WebSocket support
"""
import uvicorn
from app import app

if __name__ == '__main__':
    # Use uvicorn server for FastAPI
    uvicorn.run(
        "app:app",
        host='0.0.0.0', 
        port=5000, 
        reload=True,
        log_level="debug"
    )