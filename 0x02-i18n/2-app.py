#!/usr/bin/env python3
'''Task 2: Get locale from request

This script defines a Flask application that
retrieves the locale from the request
headers and sets it using Flask-Babel.
It also defines a route ("/") that renders
an HTML template called "2-index.html".
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    '''Config class

    This class defines configuration parameters for the Flask application.
    '''
    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.

    Returns:
        str: Best match locale from the supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''Default route

    Returns:
        str: Rendered HTML template.
    '''
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
