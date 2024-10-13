from datetime import datetime
from pymongo import MongoClient
import pymongo.errors


# MongoDB setup
client = MongoClient("mongodb://localhost:27017/?timeoutMS=1000") # Set time out to 1 seconds!
db = client["random_arrays"]
collection = db["arrays"]


def store_in_db(array: list, size: int):
    """
    Tries to store array and returns document id if succeed,
    else returns False
    """
    try:
        db.arrays.insert_one(
            {"size": size, "array": array, "timestamp": str(datetime.now())}
        )
        return {"status": 200}
    except pymongo.errors.ServerSelectionTimeoutError:
        return {"status": "Server selection timed out"}
    except pymongo.errors.PyMongoError:
        return {"status": "Failed to establish a connection to the MongoDB server"}


def fetch_previous_arrays(offset=0, limit=10):
    """
    In order to check if arrays are actually saved returns a list,
    if fail returns False
    """
    try:
        previous_arrays = list(
            collection.find().sort("_id", -1).skip(offset).limit(limit)
        )
        return {"status": 200, "data": previous_arrays}
    except pymongo.errors.ServerSelectionTimeoutError:
        return {"status": "Server selection timed out"}
    except pymongo.errors.PyMongoError:
        return {"status": "Failed to establish a connection to the MongoDB server"}
