import os
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_db():
    global _client
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    if _client is None:
        from pymongo import MongoClient
        _client = MongoClient(uri)
    db_name = os.getenv("MONGO_DB", "ost_open")
    return _client[db_name]
