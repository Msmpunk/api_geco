import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routes.routes import *

if __name__ == "__main__":
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 8102  # Custom port

    # Start the Flask application
    app.run(host=host, port=port, debug=True)
