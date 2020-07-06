#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import requests
import pandas as pd
import plotly.express as px
from sodapy import Socrata

try:
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofchicago.org", None)
    
    # App Tokens
    # 
    # All requests should include an app token that identifies your 
    # application, and each application should have its own unique app token. 
    # A limited number of requests can be made without an app token, but 
    # they are subject to much lower throttling limits than request that 
    # do include one. With an app token, your application is guaranteed 
    # access to it's own pool of requests.
    App Name: nuertey-chicago-transportation    
    Description: Retrieve and visualize transportation dataset for Chicago. 
    App Token: TGwsE5rFJmdWNfLatKrC4WXj7

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofchicago.org,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # By default, the Socrata connection will timeout after 10 seconds.
    # You are able to increase the timeout limit for the Socrata client 
    # by updating the 'timeout' instance variable like so:
    #
    # change the timeout variable to an arbitrarily large number of seconds
    client.timeout = 100

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("m6dm-c72p", limit=20)

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
except Exception as e:
    print(e)

