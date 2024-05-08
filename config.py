import os
from logger.logger import setup_logger

logger = setup_logger()

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI')

# Check if the URI is defined
if not MONGO_URI:
    logger.error("The environment variable MONGO_URI is not defined.")
    raise ValueError("The environment variable MONGO_URI is not defined.")