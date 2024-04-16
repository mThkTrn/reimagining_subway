import os

import flask
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def hello_world():
        return "Hello World"

    @app.route("/about")
    def about():
        return flask.render_template('about.html')

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)