from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["creative_idea_generator"]
ideas_collection = db["ideas"]

def check_db_store():
    """Check and print all documents in the ideas collection."""
    try:
        documents = list(ideas_collection.find())
        if documents:
            print(f"Found {len(documents)} cached ideas:")
            for doc in documents:
                print(f"Topic: {doc.get('topic')}")
                print(f"Idea: {doc.get('idea')}")
                print("-" * 40)
        else:
            print("No cached ideas found in the database.")
    except Exception as e:
        print(f"Error checking database: {str(e)}")

if __name__ == "__main__":
    check_db_store()
