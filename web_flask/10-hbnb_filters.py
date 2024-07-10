#!/usr/bin/python3

"""starts Flask web application for airBnB clone"""

from flask import Flask, render_template
from models import storage, State, Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(exception=None):
    storage.close()


@app.route("/hbnb_filters")
def hbnb_filters():
    states_values = list(storage.all(State).values())
    amenity_values = list(storage.all(Amenity).values())
    return render_template(
        "10-hbnb_filters.html",
        states_values=states_values,
        amenity_values=amenity_values
    )


# @app.route('/states/<id>')
# def states_by_id(id):
#
#     states = storage.all(State)
#     state = states.get(f"State.{id}")
#
#     if state:
#         return render_template("9-states.html", state=state)
#     else:
#         return render_template("9-states.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
