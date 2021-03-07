#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
import plotly.express as px
from sodapy import Socrata

pd.set_option('display.max_rows', 200)
pd.set_option('display.min_rows', 200)

#df = px.data.tips()
#print(df)
#fig = px.bar(df, x="total_bill", y="sex", color='day', orientation='h',
#             hover_data=["tip", "size"],
#             height=400,
#             title='Restaurant bills')
#fig.show()

# https://data.cityofchicago.org/api/views/igwz-8jzy/
# https://dev.socrata.com/foundry/data.cityofchicago.org/igwz-8jzy

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
chicago_socrata_domain = "data.cityofchicago.org"
rideshare_trips_dataset_identifier = "m6dm-c72p"
community_areas_dataset_identifier = "igwz-8jzy"
socrata_token = None

client = Socrata(chicago_socrata_domain, socrata_token)

# By default, the Socrata connection will timeout after 10 seconds.
# You are able to increase the timeout limit for the Socrata client 
# by updating the 'timeout' instance variable like so:
#
# change the timeout variable to an arbitrarily large number of seconds
client.timeout = 19200

print(
    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
        **client.__dict__
    )
)

try:
    # Returned as JSON from API and converted to Python list of 
    # dictionaries by sodapy.
    results = client.get(rideshare_trips_dataset_identifier, limit=100000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_dict(results)
    print(results_df.shape)
    print()

    #results_df.set_index('trip_id', inplace=True)
    #print(results_df.transpose())
    #print()
    results_df['rounded_miles'] = results_df['trip_miles'].astype(float).apply(lambda x: round(x, 0))

    results = client.get(community_areas_dataset_identifier)
    areas_df = pd.DataFrame.from_dict(results)
    print(areas_df.shape)
    print()
    areas_df = areas_df.infer_objects()
    print(areas_df.dtypes)
    print()
    areas_df['area_num_1'] = areas_df['area_num_1'].astype(int)
    print(areas_df.dtypes)
    print()

    results_df['pickup_community_area_name'] = results_df['pickup_community_area'].map(areas_df.set_index('area_num_1')['community'])

    #print(results_df['pickup_community_area_name'])
    #print()
    #print(results_df.pickup_community_area_name.unique())
    #print()

    ordered_community_areas = areas_df.sort_values(by=['area_num_1'], ascending=True)
    print(ordered_community_areas[['area_num_1', 'community']])
    print()

    figure1 = px.bar(results_df, 
                     y="pickup_community_area", 
                     color='rounded_miles', 
                     #orientation='h',
                     hover_data=["trip_total", "tip", "pickup_community_area_name"],
                     title='Nuertey Odzeyem Analysis Of City Of Chicago RideShare Trip Mileage Frequency')
    figure1.data[-1].showlegend = True

    figure1.update_layout(
        autosize=True,
        yaxis=dict(
            title_text="Pickup Community Area",
            ticktext=ordered_community_areas['community'],
            tickvals=ordered_community_areas['area_num_1'],
            tickmode="array",
            titlefont=dict(size=30),
        )
    )

    figure1.update_yaxes(automargin=True)
    figure1.show()

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
