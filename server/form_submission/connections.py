import os
import urllib
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PWD = os.getenv("MONGO_PWD")


def mongo_client():
    client = MongoClient(
        "mongodb+srv://"
        + urllib.parse.quote(MONGO_USER)
        + ":"
        + urllib.parse.quote(MONGO_PWD)
        + "@"
        + MONGO_URL
    )
    print("mongo ")
    return client
