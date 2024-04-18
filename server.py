import os
import json
import flask
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})


    boroughs = set()
    data = json.load(open("data/data.json"))
    for station in data.keys():
        boroughs.add(data[station]["borough"])
    
    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def home():
        return  flask.render_template("index.html", boroughs = boroughs)
    
    @app.route("/index")
    def index():
        return  flask.render_template("index.html", boroughs = boroughs)

    @app.route("/about")
    def about():
        return flask.render_template('about.html', boroughs = boroughs)
    
    @app.route("/borough_data/<borough>")
    def subway_data(borough):
        return flask.render_template('borough_data.html', borough = borough, boroughs = boroughs)
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)