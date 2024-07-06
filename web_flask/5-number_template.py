#!/usr/bin/python3

"""starts simple Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    return "HBNB"


@app.route("/c/<text>")
def c_var(text):
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python")
@app.route("/python/<text>")
def python_var(text="is_cool"):
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>")
def number(n):
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>")
def number_template(n):
    return render_template("5-number.html", num=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
