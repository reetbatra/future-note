import urllib
from pymongo import MongoClient

# mongodb://<username>:<password>@<hostname>/?ssl=true&replicaSet=atlas-chq8je-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0
# mongodb+srv://<username>:<password>@cluster0.6velis9.mongodb.net/


def get_mongo_client():
    client = MongoClient(
        "mongodb+srv://" + urllib.parse.quote("test_user_edra") + ":"
        + urllib.parse.quote("test_user_edra") + "@"
        + "cluster0.6velis9.mongodb.net/"
    )
    print("mongo ")
    return client
