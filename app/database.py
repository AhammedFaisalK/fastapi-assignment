import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

client = MongoClient(MONGO_CONNECTION_STRING)
db = client["mydatabase"]

# Collections
items_collection = db["items"]
clockin_collection = db["clock_in_records"]
