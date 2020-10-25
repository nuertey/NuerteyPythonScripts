#***********************************************************************
# @file
#
# Python script for querying City of Chicago transportation date via the
# the sodapy API (Python bindings for the Socrata Open Data API).
#
# @note None
#
# @warning  None
#
#  Created: October 25, 2020
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

pd.set_option('display.max_rows', 50)
pd.set_option('display.min_rows', 50)

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:

# https://data.cityofnewyork.us/resource/g2t5-u7v8.json

# The Host Name for the API endpoint (the https:// part will be added automatically)
data_url = 'data.cityofnewyork.us'    

# The data set at the API endpoint (311 data in this case)
data_set = 'g2t5-u7v8'    

# Application token:
app_token = None

# Create the client to point to the API endpoint
client = Socrata(data_url, app_token) 

# By default, the Socrata connection will timeout after 10 seconds.
# You are able to increase the timeout limit for the Socrata client 
# by updating the 'timeout' instance variable like so:
#
# change the timeout variable to 60 seconds
client.timeout = 60

# For debugging, display our session credentials:
print(
    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
        **client.__dict__
    )
)

try:
    # Returned as JSON from API and converted to Python list of 
    # dictionaries by sodapy.
    results = client.get(data_set, limit=50)

    # Convert the list of dictionaries to a Pandas DataFrame
    results_df = pd.DataFrame.from_dict(results)

    print(results_df)
    print()

except Exception as e:
    print(e)

# Close the sodapy session when finished:
client.close()
