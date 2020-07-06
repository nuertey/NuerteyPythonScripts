#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import requests
import pandas as pd
import plotly.express as px
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("data.cityofchicago.org", None)

# App Tokens
# 
# All requests should include an app token that identifies your 
# application, and each application should have its own unique app token. 
# A limited number of requests can be made without an app token, but 
# they are subject to much lower throttling limits than request that 
# do include one. With an app token, your application is guaranteed 
# access to it's own pool of requests.
#
# App Name: nuertey-chicago-transportation    
# Description: Retrieve and visualize transportation dataset for Chicago. 
# App Token: TGwsE5rFJmdWNfLatKrC4WXj7
NUERTEY_CHICAGO_TRANSPORTATION_TOKEN = "TGwsE5rFJmdWNfLatKrC4WXj7" 
SOCRATA_USERNAME = "intelliplay2003@gmail.com"
SOCRATA_PASSWORD = "!Krobo2003"

# Example authenticated client (needed for non-public datasets):
client = Socrata("data.cityofchicago.org",
                NUERTEY_CHICAGO_TRANSPORTATION_TOKEN,
                username=SOCRATA_USERNAME,
                password=SOCRATA_PASSWORD)

# By default, the Socrata connection will timeout after 10 seconds.
# You are able to increase the timeout limit for the Socrata client 
# by updating the 'timeout' instance variable like so:
#
# change the timeout variable to an arbitrarily large number of seconds
client.timeout = 100

print(
    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
        **client.__dict__
    )
)

try:
    # First 2000 results, returned as JSON from API / converted to Python 
    # list of dictionaries by sodapy.
    results = client.get("m6dm-c72p", limit=2)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    print(results_df)
    print()

    #figure1 = px.bar(results_df['trip_miles'], 
    #                 x="Trip Frequency", y="Trip Miles", 
    #                 color='frequency', orientation='h',
    #                 hover_data=["fare", "tip"],
    #                 title='City Of Chicago RideShare Trip Mileage Frequency')
    #figure1.show()

    # SoQL Clauses
    #
    # https://dev.socrata.com/docs/queries/
    #
    # Example(s):
    # https://soda.demo.socrata.com/resource/4tka-6guv.json?$where=magnitude > 3.0

    # get(dataset_identifier, content_type="json", **kwargs)
    # 
    # Retrieve data from the requested resources. Filter and query data by field name, id, or using SoQL keywords.
    # 
    # >>> client.get("nimj-3ivp", limit=2)
    # [{u'geolocation': {u'latitude': u'41.1085', u'needs_recoding': False, u'longitude': u'-117.6135'}, u'version': u'9', u'source': u'nn', u'region': u'Nevada', u'occurred_at': u'2012-09-14T22:38:01', u'number_of_stations': u'15', u'depth': u'7.60', u'magnitude': u'2.7', u'earthquake_id': u'00388610'}, {...}]
    # 
    # >>> client.get("nimj-3ivp", where="depth > 300", order="magnitude DESC", exclude_system_fields=False)
    # [{u'geolocation': {u'latitude': u'-15.563', u'needs_recoding': False, u'longitude': u'-175.6104'}, u'version': u'9', u':updated_at': 1348778988, u'number_of_stations': u'275', u'region': u'Tonga', u':created_meta': u'21484', u'occurred_at': u'2012-09-13T21:16:43', u':id': 132, u'source': u'us', u'depth': u'328.30', u'magnitude': u'4.8', u':meta': u'{\n}', u':updated_meta': u'21484', u'earthquake_id': u'c000cnb5', u':created_at': 1348778988}, {...}]
    # 
    # >>> client.get("nimj-3ivp/193", exclude_system_fields=False)
    # {u'geolocation': {u'latitude': u'21.6711', u'needs_recoding': False, u'longitude': u'142.9236'}, u'version': u'C', u':updated_at': 1348778988, u'number_of_stations': u'136', u'region': u'Mariana Islands region', u':created_meta': u'21484', u'occurred_at': u'2012-09-13T11:19:07', u':id': 193, u'source': u'us', u'depth': u'300.70', u'magnitude': u'4.4', u':meta': u'{\n}', u':updated_meta': u'21484', u':position': 193, u'earthquake_id': u'c000cmsq', u':created_at': 1348778988}
    # 
    # >>> client.get("nimj-3ivp", region="Kansas")
    # [{u'geolocation': {u'latitude': u'38.10', u'needs_recoding': False, u'longitude': u'-100.6135'}, u'version': u'9', u'source': u'nn', u'region': u'Kansas', u'occurred_at': u'2010-09-19T20:52:09', u'number_of_stations': u'15', u'depth': u'300.0', u'magnitude': u'1.9', u'earthquake_id': u'00189621'}, {...}]

except Exception as e:
    print(e)

# Close the sodapy session when finished:
client.close()