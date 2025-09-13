# Gunicorn configuration for FastAPI
# Using uvicorn workers to serve ASGI applications

bind = "0.0.0.0:5000"
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
reload = True
preload_app = False
accesslog = "-"
access_log_format = "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""