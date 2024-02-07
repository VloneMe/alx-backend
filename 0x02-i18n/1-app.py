#!/usr/bin/env python3
'''Task 0: Basic Flask app

This script defines a basic Flask application
with a single route ("/") that renders
an HTML template called "1-index.html". It also
configures Flask-Babel for
internationalization support.
'''

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    '''Config class

    This class defines configuration parameters for
    the Flask application.
    '''

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False

babel = Babel(app)


@app.route('/')
def index() -> str:
    '''Default route

    Returns:
        str: Rendered HTML template.
    '''
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(debug=True)
