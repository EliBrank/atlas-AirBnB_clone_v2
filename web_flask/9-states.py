#!/usr/bin/python3

"""starts Flask web application for airBnB clone"""

from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(exception=None):
    storage.close()


@app.route("/states")
def states():
    states_values = storage.all(State).values()
    return render_template(
        '7-states_list.html', states_values=states_values
    )


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):

    states = storage.all(State)  # This returns a dictionary
    state = states.get(f"State.{id}")

    if state:
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
