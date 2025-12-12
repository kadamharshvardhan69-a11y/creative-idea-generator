from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["creative_idea_generator"]
ideas_collection = db["ideas"]

def get_cached_idea(topic: str) -> str:
    """Retrieve cached idea for a given topic."""
    result = ideas_collection.find_one({"topic": topic})
    return result["idea"] if result else None

def set_cached_idea(topic: str, idea: str):
    """Store idea in cache for a given topic."""
    ideas_collection.insert_one({"topic": topic, "idea": idea})
