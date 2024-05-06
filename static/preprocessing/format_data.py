import pandas as pd
import json
import re

df = pd.read_csv("data/data.csv")
fare_types = ["Metrocard - Fair Fare", "Metrocard - Full Fare","Metrocard - Other", "Metrocard - Seniors & Disability","Metrocard - Students", "Metrocard - Unlimited 30-Day", "Metrocard - Unlimited 7-Day", "OMNY - Full Fare", "OMNY - Other", "OMNY - Seniors & Disability"]
ddict = {}

boroughs = set(df['borough'].tolist())

ddict["boroughs"] = {}
ddict["stations"] = {}
ddict["other_data"] = {}
ddict["other_data"]["boroughs"] = list(boroughs)
for borough in boroughs:
    ddict["boroughs"][borough] = {}
    ddict["boroughs"][borough]["times"] = {}
    ddict["boroughs"][borough]["all_times"] = {}
    for fare_type in fare_types:
            ddict["boroughs"][borough]["all_times"][fare_type] =  {}
            ddict["boroughs"][borough]["all_times"][fare_type]["ridership"] = 0
            ddict["boroughs"][borough]["all_times"][fare_type]["transfers"] = 0
    ddict["boroughs"][borough]["all_times"]["all_fare_classes"] = {}
    ddict["boroughs"][borough]["all_times"]["all_fare_classes"]["ridership"] = 0
    ddict["boroughs"][borough]["all_times"]["all_fare_classes"]["transfers"] = 0

for ind in df.index:
    name = df['station_complex'][ind]
    time = df['transit_timestamp'][ind][11:]
    fare_class = df['fare_class_category'][ind]
    borough = df["borough"][ind]

    lines = set()
    for i in re.findall(r'\(.*?\)', name):
        i = i[1:-1].split(",")
        for elem in i:
            if len(elem) == 1:
                lines.update(elem)
    
    if name not in ddict["stations"].keys():
        ddict["stations"][name] = {}
        ddict["stations"][name]["lines"] = list(lines)
        ddict["stations"][name]["times"] = {}
        ddict["stations"][name]["all_times"] = {}
        for fare_type in fare_types:
            ddict["stations"][name]["all_times"][fare_type] =  {}
            ddict["stations"][name]["all_times"][fare_type]["ridership"] = 0
            ddict["stations"][name]["all_times"][fare_type]["transfers"] = 0
        ddict["stations"][name]["all_times"]["all_fare_classes"] = {}
        ddict["stations"][name]["all_times"]["all_fare_classes"]["ridership"] = 0
        ddict["stations"][name]["all_times"]["all_fare_classes"]["transfers"] = 0
    if time not in ddict["stations"][name]["times"].keys():
        ddict["stations"][name]["times"][time] = {}
        for fare_type in fare_types:
            ddict["stations"][name]["times"][time][fare_type] = {}
            ddict["stations"][name]["times"][time][fare_type]["ridership"] = 0
            ddict["stations"][name]["times"][time][fare_type]["transfers"] = 0
        ddict["stations"][name]["times"][time]["all_fare_classes"] = {}
        ddict["stations"][name]["times"][time]["all_fare_classes"]["ridership"] = 0
        ddict["stations"][name]["times"][time]["all_fare_classes"]["transfers"] = 0
    if time not in ddict["boroughs"][borough]["times"].keys():
        ddict["boroughs"][borough]["times"][time] = {}
        for fare_type in fare_types:
            ddict["boroughs"][borough]["times"][time][fare_type] = {}
            ddict["boroughs"][borough]["times"][time][fare_type]["ridership"] = 0
            ddict["boroughs"][borough]["times"][time][fare_type]["transfers"] = 0
        ddict["boroughs"][borough]["times"][time]["all_fare_classes"] = {}
        ddict["boroughs"][borough]["times"][time]["all_fare_classes"]["ridership"] = 0
        ddict["boroughs"][borough]["times"][time]["all_fare_classes"]["transfers"] = 0
    
    station_keys = ["station_complex_id", "borough", "latitude", "longitude", "georeference"]
    for i in station_keys:
        ddict["stations"][name][i] = str(df[i][ind])

    ride_stats = ["ridership","transfers"]

    for i in ride_stats:
        ddict["stations"][name]["all_times"][fare_class][i] += float(df[i][ind])
        ddict["stations"][name]["all_times"]["all_fare_classes"][i] += float(df[i][ind])
        ddict["stations"][name]["times"][time][fare_class][i] = float(df[i][ind])
        ddict["stations"][name]["times"][time]["all_fare_classes"][i] += float(df[i][ind])

        ddict["boroughs"][borough]["all_times"][fare_class][i] += float(df[i][ind])
        ddict["boroughs"][borough]["all_times"]["all_fare_classes"][i] += float(df[i][ind])

        if fare_class not in ddict["boroughs"][borough]["times"][time]:
            ddict["boroughs"][borough]["times"][time][fare_class] = {}

        if i not in ddict["boroughs"][borough]["times"][time][fare_class]:
            ddict["boroughs"][borough]["times"][time][fare_class][i] = 0
        
        ddict["boroughs"][borough]["times"][time][fare_class][i] += float(df[i][ind])
        
        ddict["boroughs"][borough]["times"][time]["all_fare_classes"][i] += float(df[i][ind])

#print(ddict)

ddict["other_data"]["num_stations"] = len(ddict["stations"].keys())

total_sum = 0

for borough in ddict["boroughs"]:
    total_sum+=ddict["boroughs"][borough]["all_times"]["all_fare_classes"]["ridership"]
ddict["other_data"]["average_hourly_ridership_borough"] = total_sum/(len(ddict["boroughs"].keys()) * 24)

json.dump(ddict, open("data/data.json", "w"))
