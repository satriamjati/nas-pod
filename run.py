from waitress import serve
from api import app  # assuming your Flask app is at /api.py

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
