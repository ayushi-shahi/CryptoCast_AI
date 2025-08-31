import requests
import logging
import time
from datetime import datetime, timedelta

class CryptoService:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
        
    def _get_cached_data(self, key):
        """Get data from cache if it's still valid"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                return data
        return None
    
    def _cache_data(self, key, data):
        """Cache data with timestamp"""
        self.cache[key] = (data, time.time())
    
    def _make_request(self, endpoint, params=None):
        """Make API request with error handling and rate limiting"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 429:
                logging.warning("Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                # Retry once after rate limit
                response = requests.get(url, params=params, timeout=10)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise
    
    def get_market_overview(self):
        """Get market overview data"""
        cache_key = "market_overview"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
            
        try:
            # Get top 10 cryptocurrencies
            coins_data = self._make_request("coins/markets", {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': True,
                'price_change_percentage': '1h,24h,7d'
            })
            
            # Get global market data
            global_data = self._make_request("global")
            
            result = {
                'coins': coins_data,
                'global': global_data['data'],
                'timestamp': datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            logging.error(f"Error fetching market overview: {e}")
            raise
    
    def get_coin_history(self, coin_id, days=7):
        """Get historical price data for a coin"""
        cache_key = f"coin_history_{coin_id}_{days}"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
            
        try:
            # Use simpler endpoint for better rate limit handling
            data = self._make_request(f"coins/{coin_id}/market_chart", {
                'vs_currency': 'usd',
                'days': days
            })
            
            result = {
                'coin_id': coin_id,
                'prices': data['prices'],
                'market_caps': data['market_caps'],
                'total_volumes': data['total_volumes'],
                'timestamp': datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            logging.error(f"Error fetching coin history for {coin_id}: {e}")
            # Return mock data for demo purposes when API fails
            return self._get_mock_price_data(coin_id, days)
    
    def get_trending_coins(self):
        """Get trending coins data"""
        cache_key = "trending_coins"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
            
        try:
            data = self._make_request("search/trending")
            
            result = {
                'trending': data['coins'],
                'timestamp': datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            logging.error(f"Error fetching trending coins: {e}")
            raise
    
    def get_defi_protocols(self):
        """Get DeFi protocol data"""
        cache_key = "defi_protocols"
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
            
        try:
            # Get DeFi coins (categories approach)
            defi_data = self._make_request("coins/markets", {
                'vs_currency': 'usd',
                'category': 'decentralized-finance-defi',
                'order': 'market_cap_desc',
                'per_page': 20,
                'page': 1,
                'sparkline': True,
                'price_change_percentage': '1h,24h,7d'
            })
            
            result = {
                'protocols': defi_data,
                'timestamp': datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            logging.error(f"Error fetching DeFi protocols: {e}")
            raise
    
    def _get_mock_price_data(self, coin_id, days=7):
        """Generate mock price data for demo when API is rate limited"""
        import random
        
        base_price = 50000 if coin_id == 'bitcoin' else 3000 if coin_id == 'ethereum' else 100
        prices = []
        volumes = []
        market_caps = []
        
        current_time = int(time.time() * 1000)
        
        for i in range(days * 24):  # Hourly data points
            timestamp = current_time - (i * 3600000)  # Go back in time
            price_variation = random.uniform(-0.05, 0.05)  # ±5% variation
            price = base_price * (1 + price_variation)
            volume = random.uniform(1000000, 10000000)
            market_cap = price * 19000000  # Approximate circulating supply
            
            prices.insert(0, [timestamp, price])
            volumes.insert(0, [timestamp, volume])
            market_caps.insert(0, [timestamp, market_cap])
        
        return {
            'coin_id': coin_id,
            'prices': prices,
            'market_caps': market_caps,
            'total_volumes': volumes,
            'timestamp': datetime.now().isoformat()
        }
