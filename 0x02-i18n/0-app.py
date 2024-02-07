#!/usr/bin/env python3
'''Task 0: Basic Flask app

This script defines a basic Flask application
with a single route ("/") that renders
an HTML template called "0-index.html".
'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index() -> str:
    '''Default route

    Returns:
        str: Rendered HTML template.
    '''
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(debug=True)
