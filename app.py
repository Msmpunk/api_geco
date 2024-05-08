import os
from flask import Flask


app = Flask(__name__)
from routes.routes import *

if __name__ == "__main__":
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 8080  # Custom port

    # Start the Flask application
    app.run(host=host, port=port, debug=True)
