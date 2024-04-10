import requests
import pandas as pd

#trying a different approach, not using SODA API but just using simple requests

url = "https://data.ny.gov/resource/wujg-7c2s.json"

#SQL parameters

params = {
    "$where": "transit_timestamp >= '2023-03-01T00:00:00' AND transit_timestamp < '2023-03-02T00:00:00'",
    "$limit": 5_000_000 # set this arbitrarily high
}

response = requests.get(url, params=params)


if response.status_code == 200:
    data = pd.DataFrame(response.json())
    data.to_csv("data/data.csv", index = False)
else:
    print(f"Error: {response.status_code} - {response.text}")

