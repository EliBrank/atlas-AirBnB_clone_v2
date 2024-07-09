#!/usr/bin/python3

"""starts Flask web application for airBnB clone"""

from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(exception=None):
    storage.close()


@app.route("/cities_by_state")
def states_list():
    states_values = list(storage.all(State).values())
    return render_template("8-cities_by_states.html", states_values=states_values)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
