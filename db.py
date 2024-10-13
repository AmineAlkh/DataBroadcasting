from pymongo import MongoClient
from datetime import datetime


# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["random_arrays"]
collection = db["arrays"]


def store_in_db(array: list, size: int):
    """
    Tries to store array and returns document id if succeed,
    else returns False
    """
    try:
        array_id = db.arrays.insert_one(
            {"size": size, "array": array, "timestamp": str(datetime.now())}
        ).inserted_id
        return array_id
    except:
        return False


def fetch_previous_arrays(offset=0, limit=10):
    """
    In order to check if arrays are actually saved returns a list,
    if fail returns False
    """
    try:
        previous_arrays = list(
            collection.find().sort("_id", -1).skip(offset).limit(limit)
        )
        return previous_arrays
    except:
        return False
