from app import app

# For gunicorn compatibility, ensure the app is available as 'app'
# Gunicorn will look for the app object in this module
