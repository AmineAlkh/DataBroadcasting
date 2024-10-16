from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from socketio.exceptions import ConnectionError, SocketIOError
import numpy as np
from db import store_in_db, fetch_previous_arrays

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
        )  # Empty or alphabetical input is converted to 10000 in template!
        if array_size <=0:
            emit("error", {"message": "Invalid input. Array size must be positive."}, broadcast=True)
        elif array_size < 300000:
            random_array = np.random.randint(0, 99999, array_size).tolist()
            # Stores in MongoDB
            array_id = store_in_db(random_array, array_size)
            # If failed to save, shows error message
            if array_id:
                # Broadcast the new array to clients
                socketio.emit("new_array", {"array": random_array})
            else:
                emit("error", {"message": "Failed to connect to database."}, broadcast=True)
        else:
            emit("error", {"message": "Size of array is too large!"}, broadcast=True)
    except ConnectionError as e:
        emit("error", {"message": "Connection error occurred"}, broadcast=True)
    except SocketIOError as e:
        emit("error", {"message": "Socket.IO error occurred"}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
