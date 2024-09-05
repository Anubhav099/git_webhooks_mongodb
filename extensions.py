from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']  # Replace with your DB name
collection = db['your_collection']  # Replace with your collection name

# Define the document to insert
document = {
    "request_id": "abcd1234",  # Use Git commit hash or PR ID
    "author": "github_user",  # Name of the Github user
    "action": "PUSH",  # Enum value: "PUSH", "PULL_REQUEST", "MERGE"
    "from_branch": "feature-branch",  # LHS branch
    "to_branch": "main",  # RHS branch
    "timestamp": datetime.utcnow()  # Timestamp in UTC
}

# Insert the document
inserted_id = collection.insert_one(document).inserted_id
print(f"Inserted document with ID: {inserted_id}")
