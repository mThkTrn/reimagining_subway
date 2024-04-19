import pandas as pd
import json

df = pd.read_csv("data/data.csv")

ddict = {}

for ind in df.index:
    name = df['station_complex'][ind]
    time = df['transit_timestamp'][ind][11:]

    if name not in ddict.keys():
        ddict[name] = {}
    if time not in ddict[name].keys():
        ddict[name][time] = {}
    
    station_keys = ["station_complex_id", "borough", "latitude", "longitude", "georeference"]
    for i in station_keys:
        ddict[name][i] = str(df[i][ind])

    ride_keys = ["transit_mode","payment_method","fare_class_category","ridership","transfers"]

    for i in ride_keys:
        ddict[name][time][i] = str(df[i][ind])

print(ddict)

json.dump(ddict, open("data/data.json", "w"))
