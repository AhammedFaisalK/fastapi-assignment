from pymongo import MongoClient

# Replace with your MongoDB connection string
MONGO_CONNECTION_STRING = "<mongodb+srv://ahammedfaisal70:<db_password>@cluster0.fhi0n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0>"

client = MongoClient(MONGO_CONNECTION_STRING)
db = client["mydatabase"]

# Collections
items_collection = db["items"]
clockin_collection = db["clock_in_records"]
