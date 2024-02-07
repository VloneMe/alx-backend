#!/usr/bin/env python3
'''Task 4: Force locale with URL parameter

This script defines a Flask application that
allows the user to force the locale
using a URL parameter named "locale".
If the specified locale is available in
the supported languages, it will be used;
otherwise, the best match locale
will be determined based on the Accept-Language header.
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
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''Default route

    Returns:
        html: Rendered homepage.
    '''
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run()
