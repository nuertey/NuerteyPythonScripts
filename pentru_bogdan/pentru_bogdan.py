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

# The Host Name for the API endpoint (the https:// part will be added automatically)
data_url = "data.cityofnewyork.us"
rideshare_trips_dataset_identifier = "m6dm-c72p"
community_areas_dataset_identifier = "igwz-8jzy"
socrata_token = None

data_url='data.cityofnewyork.us'    

# The data set at the API endpoint (311 data in this case)
data_set='erm2-nwe9'    

app_token='xyz123xyz123xyz123xyz123'
client = Socrata(da

client = Socrata(chicago_socrata_domain, socrata_token)

client2 = Socrata("sandbox.demo.socrata.com", "FakeAppToken", username="fakeuser@somedomain.com", password="ndKS92mS01msjJKs")

client2.get("/resource/nimj-3ivp.json", limit=2)
[{u'geolocation': {u'latitude': u'41.1085', u'needs_recoding': False, u'longitude': u'-117.6135'}, u'version': u'9', u'source': u'nn', u'region': u'Nevada', u'occurred_at': u'2012-09-14T22:38:01', u'number_of_stations': u'15', u'depth': u'7.60', u'magnitude': u'2.7', u'earthquake_id': u'00388610'}, {u'geolocation': {u'latitude': u'34.525', u'needs_recoding': False, u'longitude': u'-118.1527'}, u'version': u'0', u'source': u'ci', u'region': u'Southern California', u'occurred_at': u'2012-09-14T22:14:45', u'number_of_stations': u'35', u'depth': u'10.60', u'magnitude': u'1.5', u'earthquake_id': u'15215753'}]

client2.get("/resource/nimj-3ivp.json", where="depth > 300", order="magnitude DESC", exclude_system_fields=False)
[{u'geolocation': {u'latitude': u'-15.563', u'needs_recoding': False, u'longitude': u'-175.6104'}, u'version': u'9', u':updated_at': 1348778988, u'number_of_stations': u'275', u'region': u'Tonga', u':created_meta': u'21484', u'occurred_at': u'2012-09-13T21:16:43', u':id': 132, u'source': u'us', u'depth': u'328.30', u'magnitude': u'4.8', u':meta': u'{\n}', u':updated_meta': u'21484', u'earthquake_id': u'c000cnb5', u':created_at': 1348778988}, {u'geolocation': {u'latitude': u'-23.5123', u'needs_recoding': False, u'longitude': u'-179.1089'}, u'version': u'3', u':updated_at': 1348778988, u'number_of_stations': u'93', u'region': u'south of the Fiji Islands', u':created_meta': u'21484', u'occurred_at': u'2012-09-14T16:14:58', u':id': 32, u'source': u'us', u'depth': u'387.00', u'magnitude': u'4.6', u':meta': u'{\n}', u':updated_meta': u'21484', u'earthquake_id': u'c000cp1z', u':created_at': 1348778988}, {u'geolocation': {u'latitude': u'21.6711', u'needs_recoding': False, u'longitude': u'142.9236'}, u'version': u'C', u':updated_at': 1348778988, u'number_of_stations': u'136', u'region': u'Mariana Islands region', u':created_meta': u'21484', u'occurred_at': u'2012-09-13T11:19:07', u':id': 193, u'source': u'us', u'depth': u'300.70', u'magnitude': u'4.4', u':meta': u'{\n}', u':updated_meta': u'21484', u'earthquake_id': u'c000cmsq', u':created_at': 1348778988}]

client2.get("/resource/nimj-3ivp/193.json", exclude_system_fields=False)
{u'geolocation': {u'latitude': u'21.6711', u'needs_recoding': False, u'longitude': u'142.9236'}, u'version': u'C', u':updated_at': 1348778988, u'number_of_stations': u'136', u'region': u'Mariana Islands region', u':created_meta': u'21484', u'occurred_at': u'2012-09-13T11:19:07', u':id': 193, u'source': u'us', u'depth': u'300.70', u'magnitude': u'4.4', u':meta': u'{\n}', u':updated_meta': u'21484', u':position': 193, u'earthquake_id': u'c000cmsq', u':created_at': 1348778988}

# By default, the Socrata connection will timeout after 10 seconds.
# You are able to increase the timeout limit for the Socrata client 
# by updating the 'timeout' instance variable like so:
#
# change the timeout variable to an arbitrarily large number of seconds
client.timeout = 19200

# For debugging, display our session credentials:
print(
    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
        **client.__dict__
    )
)

try:
    # Returned as JSON from API and converted to Python list of 
    # dictionaries by sodapy.
    results = client.get(rideshare_trips_dataset_identifier, limit=50)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_dict(results)

    # For debugging, show us how the data looks:
    print(results_df.shape)
    print()

    # Perform some data manipulation:
    results_df['rounded_miles'] = results_df['trip_miles'].astype(float).apply(lambda x: round(x, 0))

    # Display the result of that data manipulation as a plain table:
    print(results_df)
    print()

    # Get another kind of data from the City of Chicago API:
    results = client.get(community_areas_dataset_identifier)
    areas_df = pd.DataFrame.from_dict(results)

    # For debugging, show us how the data looks:
    print(areas_df.shape)
    print()

    # For debugging, tell us the data types of the objects in the dataset:
    areas_df = areas_df.infer_objects()
    print(areas_df.dtypes)
    print()

    # Perform some data manipulation by taking one column of the data and,
    # regardless of its actual type forcibly converting it into integers:
    areas_df['area_num_1'] = areas_df['area_num_1'].astype(int)

    # For debugging, and to ensure that our previous conversion worked,
    # print out the data types of the objects in the dataset (i.e. just that column):
    print(areas_df.dtypes)
    print()

    # Do some more interesting data manipulations:
    results_df['pickup_community_area_name'] = results_df['pickup_community_area'].map(areas_df.set_index('area_num_1')['community'])

    # Show the results to us in just a plain table format:
    print(results_df['pickup_community_area_name'])
    print()
    print(results_df.pickup_community_area_name.unique())
    print()

    # Do even more interesting data manipulations:
    ordered_community_areas = areas_df.sort_values(by=['area_num_1'], ascending=True)

    # Show the results to us in just a plain table format:
    print(ordered_community_areas[['area_num_1', 'community']])
    print()

except Exception as e:
    print(e)

# Close the sodapy session when finished:
client.close()
