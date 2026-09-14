import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_router_info():
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
    db_name = os.environ.get("DB_NAME", "ipa2026_db")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    routers = db["routers"]

    router_data = routers.find()
    return router_data


if __name__=='__main__':
    get_router_info()