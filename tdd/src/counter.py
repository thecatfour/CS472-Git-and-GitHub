from flask import Flask
from . import status

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Create a counter"""

    app.logger.info(f"Request to create counter: {name}")

    global COUNTERS

    if name in COUNTERS:
        return {"Message":f"Counter {name} already exists"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0

    return {name: COUNTERS[name]}, status.HTTP_201_CREATED

@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Updates a counter"""

    app.logger.info(f"Request to update counter: {name}")

    global COUNTERS

    if name not in COUNTERS:
        return {"Message":f"Counter {name} does not exist"}, status.HTTP_204_NO_CONTENT
    
    COUNTERS[name] += 1

    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["GET"])
def get_counter(name):
    """Gets the value of a counter"""

    app.logger.info(f"Request to get counter value: {name}")

    global COUNTERS

    if name not in COUNTERS:
        return {"Message":f"Counter {name} was not found"}, status.HTTP_404_NOT_FOUND

    return str(COUNTERS[name]), status.HTTP_200_OK