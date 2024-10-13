from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
from db import store_in_db, fetch_previous_arrays

from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["random_arrays"]
collection = db["arrays"]

app = Flask(__name__)
app.config["SECRET_KEY"] = "random_secret_key"
app.config["STATIC_FOLDER"] = "static"
socketio = SocketIO(app)


@app.route("/")
def index():
    """
    Template contains:
    1: Generate Array btn
    2: List of Real-Time generated arrays (Does not read from database!)
    """
    return render_template("index.html")


@app.route("/previous_arrays")
def previous_arrays():
    """
    Displays last 10 saved arrays (Not real-time, Just reads from Database!)
    """
    previous_arrays = fetch_previous_arrays()
    return render_template("previous.html", arrays=previous_arrays)


@socketio.on("generate_array")
def handle_generate_array(data):
    """
    Called each time a Generate Array btn is clicked and:
    1- Generates array
    2- Stores size, time and array list
    3- Broadcasts it
    """
    try:
        array_size = int(
            data.get("size")
        )  # Empty input is converted to 10000 in template!
        random_array = np.random.randint(0, 99999, array_size).tolist()
        # Stores in MongoDB
        array_id = store_in_db(random_array, array_size)
        # If failed to save, shows error message
        if array_id:
            # Broadcast the new array to clients
            socketio.emit("new_array", {"array": random_array})
        else:
            emit("error", {"message": "Failed to save data"}, broadcast=True)
    except Exception as e:
        emit("error", {"message": str(e)}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
