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
    
    data = json.load(open("data/data.json"))
    
    adds_counter = 0
    times_sum = 0
    for station in data["stations"]:
        for time in data["stations"][station]["times"]:
            times_sum += (data["stations"][station]["times"][time]["all_fare_classes"]["ridership"] * int(time[:2]))
            adds_counter += data["stations"][station]["times"][time]["all_fare_classes"]["ridership"]
    avg_time = times_sum/adds_counter

    boroughs = data["other_data"]["boroughs"]
    # linedata = json.load(open("data/subway_station_lines.json"))
    # for station in data.keys():
    #     boroughs.add(data[station]["borough"])

    # borough_data = {}
    # for borough in boroughs:
    #     borough_data[borough] = {}
    #     borough_data[borough]["lines"] = set()
    #     borough_data[borough]["total"] = 0
    #     borough_data[borough]["times"] = {}
    #     for i in range(24):
    #         borough_data[borough]["times"] = [0]*24
    
    # for station in data.keys():
    #     for i in re.findall(r'\(.*?\)', station):
    #         i = i[1:-1].split(",")
    #         for elem in i:
    #             if len(elem) == 1:
    #                 borough_data[data[station]["borough"]]["lines"].update(elem)
    #         #print(i, borough_data[data[station]["borough"]]["lines"])
    #     for time in range(24):
    #         try:
    #             borough_data[data[station]["borough"]]["times"][time]+=float(data[station]["times"][f"{time:02}:00:00.000"]["ridership"])
    #         except KeyError:
    #             pass
    # for borough in borough_data: borough_data[borough]["total"] = sum(borough_data[borough]["times"])
    
    # [fairfare, transfer, lines]
    
    fairfare_circles_list = []
    transfer_circles_list = []
    lines_circles_list = []
    scales = [1, 0.2, 3]

    for station in data["stations"].keys():
        counts = [data["stations"][station]["times"]["08:00:00.000"]["Metrocard - Fair Fare"]["ridership"], data["stations"][station]["all_times"]["all_fare_classes"]["transfers"], len(data["stations"][station]["lines"])]
        # print(counts)
        pos = [map_coords(nyc_svg_bottom_left, nyc_svg_top_right, (0,0), (500,500), (float(data["stations"][station]["latitude"]), float(data["stations"][station]["longitude"]))), map_coords(nyc_svg_bottom_left, nyc_svg_top_right, (0,0), (500,500), (float(data["stations"][station]["latitude"]), float(data["stations"][station]["longitude"]))), map_coords(nyc_svg_bottom_left, nyc_svg_top_right, (0,0), (500,500), (float(data["stations"][station]["latitude"]), float(data["stations"][station]["longitude"])))]
        #print(pos[0])
        # print(counts[0]*scales[0]==counts[2]*scales[2])
        pos[0].append(math.sqrt(counts[0])*scales[0])
        pos[1].append(math.sqrt(counts[1])*scales[1])
        pos[2].append(math.sqrt(counts[2])*scales[2])
        # print(f"adding: {math.sqrt(counts[0])*scales[0]}")
        # print(pos[0])
        fairfare_circles_list.append(pos[0])
        transfer_circles_list.append(pos[1])
        lines_circles_list.append(pos[2])

    #print("check: "+ str(fairfare_circles_list == lines_circles_list))
    # print(fairfare_circles_list)
    #print(transfer_circles_list)
    # print(lines_circles_list)
    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def home():
        return  flask.render_template("index.html", boroughs = boroughs, nyc_svg_bottom_left = nyc_svg_bottom_left, nyc_svg_top_right = nyc_svg_top_right, data = data, fairfare_circles_list = fairfare_circles_list, transfer_circles_list = transfer_circles_list, lines_circles_list = lines_circles_list)
    
    # @app.route("/index")
    # def index():
    #     return  flask.render_template("index.html", boroughs = boroughs, nyc_svg_bottom_left = nyc_svg_bottom_left, nyc_svg_top_right = nyc_svg_top_right, data = data, circles_list = circles_list)

    @app.route("/about")
    def about():
        return flask.render_template('about.html', boroughs = boroughs)
    
    @app.route("/borough_data")
    def subway_data():
        borough = flask.request.args.get('borough')

        bor_adds_counter = 0
        bor_times_sum = 0
        for station in data["stations"]:
            if data["stations"][station]["borough"] == borough:
                for time in data["stations"][station]["times"]:
                    bor_times_sum += (data["stations"][station]["times"][time]["all_fare_classes"]["ridership"] * int(time[:2]))
                    bor_adds_counter += data["stations"][station]["times"][time]["all_fare_classes"]["ridership"]
        bor_avg_time = bor_times_sum/bor_adds_counter

        return flask.render_template('borough_data.html', borough = borough, boroughs = boroughs, data = data, transit_bor = (bor_avg_time < avg_time), very_transit_bor = ((avg_time - bor_avg_time) > 1.5), time_vals = [(i, f"{i:02}:00:00.000") for i in range(24)])
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)