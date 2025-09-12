# CryptoCast AI

CryptoCast AI is a real-time cryptocurrency monitoring and prediction platform.  
It provides live updates on crypto prices, rankings, market trends, and visual insights through charts and dashboards.  
The system uses WebSockets for live data streaming and Flask as the backend framework.  

---

## Features

- Real-time crypto price updates  
- Market overview and trending coins  
- Coin-specific subscription and updates  
- Live prediction insights  
- Visual representations of price movements and rankings  
- Flask-SocketIO powered WebSocket connections for instant updates  

---

## Tech Stack

- **Backend:** Python, Flask, Flask-SocketIO  
- **Data Services:** Custom CryptoService for fetching live data  
- **Visualization:** Charts and dashboards  
- **Concurrency:** Background tasks for live streaming updates  

---
---

## Setup Instructions

Follow these steps to set up and run the project:

### 1. Clone the repository

git clone https://github.com/ayushi-shahi/CryptoCast_AI.git

### 2. Create and activate a virtual environment

python -m venv venv
On Windows:
venv\Scripts\activate
On Linux/Mac:
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the application
python app.py

### Requirements
Dependencies are listed in requirements.txt. Main packages include:
Flask
Flask-SocketIO
Requests
Eventlet / Gevent (optional for async mode)
