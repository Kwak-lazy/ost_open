from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

_client = None


def get_db():
    global _client
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    if _client is None:
        _client = MongoClient(uri)
    db_name = os.getenv("MONGO_DB", "ost_open")
    return _client[db_name]
