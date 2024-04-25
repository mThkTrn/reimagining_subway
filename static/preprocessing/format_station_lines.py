import pandas as pd
import json

df = pd.read_csv("data/subway_station_lines.csv", index_col = False, delimiter = ";")

outdict = {}

for ind in df.index:
    outdict[df["NAME"][ind]] = df["LINE"][ind]

with open("data/subway_station_lines.json", "w") as f:
    json.dump(outdict, f)