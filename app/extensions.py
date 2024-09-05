from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["WebHooks"]  # Replace with your database name
collection = db["AutoGit"]  # Replace with your collection name
