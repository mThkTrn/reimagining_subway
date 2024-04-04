import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.ny.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.ny.gov,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("wujg-7c2s", limit = 10_000_000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#filter only rows that are from February 9th, 2023
# results_df = results_df[results_df.transit_timestamp.str.startswith("")]

results_df.to_csv("subway_data.csv", index=False, sep = "\t")