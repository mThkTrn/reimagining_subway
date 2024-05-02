import os
import json
import flask
from flask import Flask
import math
import re
def map_coords(orig_p0, orig_p1, map_p0, map_p1, coords):
    # print(f"X: ({coords[0]} - {orig_p0[0]}) * ({map_p1[0]}-{map_p0[0]})/({orig_p1[0]}-{orig_p0[0]}) + {map_p0[0]}")
    # print(f"Y: ({coords[1]} - {orig_p0[1]}) * ({map_p1[1]}-{map_p0[1]})/({orig_p1[1]}-{orig_p0[1]}) + {map_p0[0]}")
    # print([(coords[0] - orig_p0[0]) * (map_p1[0]-map_p0[0])/(orig_p1[0]-orig_p0[0]) + map_p0[0],(coords[1] - orig_p0[1]) * (map_p1[1]-map_p0[1])/(orig_p1[1]-orig_p0[1]) + map_p0[1]])
    return [(coords[1] - orig_p0[1]) * (map_p1[1]-map_p0[1])/(orig_p1[1]-orig_p0[1]) + map_p0[1] + 5, 500-((coords[0] - orig_p0[0]) * (map_p1[0]-map_p0[0])/(orig_p1[0]-orig_p0[0]) + map_p0[0])]


def create_app(config=None):
    app = Flask(__name__, static_url_path='', static_folder="static")
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    nyc_svg_bottom_left = [40.495306, -74.257389]
    nyc_svg_top_right = [40.914913, -73.685304]

    boroughs = set()
    data = json.load(open("data/data.json"))
    linedata = json.load(open("data/subway_station_lines.json"))
    for station in data.keys():
        boroughs.add(data[station]["borough"])

    borough_data = {}
    for borough in boroughs:
        borough_data[borough] = {}
        borough_data[borough]["lines"] = set()
        borough_data[borough]["total"] = 0
        borough_data[borough]["times"] = {}
        for i in range(24):
            borough_data[borough]["times"] = [0]*24
    
    for station in data.keys():
        for i in re.findall(r'\(.*?\)', station):
            i = i[1:-1].split(",")
            for elem in i:
                if len(elem) == 1:
                    borough_data[data[station]["borough"]]["lines"].update(elem)
            print(i, borough_data[data[station]["borough"]]["lines"])
        for time in range(24):
            try:
                borough_data[data[station]["borough"]]["times"][time]+=float(data[station]["times"][f"{time:02}:00:00.000"]["ridership"])
            except KeyError:
                pass
    for borough in borough_data: borough_data[borough]["total"] = sum(borough_data[borough]["times"])
    circles_list = []
    circle_scale = 0.3
    for station in data.keys():
        count = 0
        pos = map_coords(nyc_svg_bottom_left, nyc_svg_top_right, (0,0), (500,500), (float(data[station]["latitude"]), float(data[station]["longitude"])))
        for time in data[station]["times"]:
            if time == "07:00:00.000" or time == "06:00:00.000" or time == "08:00:00.000":
                count += (float(data[station]["times"][time]["ridership"]) - float(data[station]["times"][time]["transfers"]))
        pos.append(math.sqrt(count)*circle_scale)
        circles_list.append(pos)
    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def home():
        return  flask.render_template("index.html", boroughs = boroughs, nyc_svg_bottom_left = nyc_svg_bottom_left, nyc_svg_top_right = nyc_svg_top_right, data = data, circles_list = circles_list)
    
    @app.route("/index")
    def index():
        return  flask.render_template("index.html", boroughs = boroughs, nyc_svg_bottom_left = nyc_svg_bottom_left, nyc_svg_top_right = nyc_svg_top_right, data = data, circles_list = circles_list)

    @app.route("/about")
    def about():
        return flask.render_template('about.html', boroughs = boroughs)
    
    @app.route("/borough_data")
    def subway_data():
        borough = flask.request.args.get('borough')
        return flask.render_template('borough_data.html', borough = borough, boroughs = boroughs, data = data, borough_data = borough_data)
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)