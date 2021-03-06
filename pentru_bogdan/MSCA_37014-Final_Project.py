#***********************************************************************
# @file
#
# Python script for Airbnb Consultancy. Its primary goal is to aid Airbnb
# in better understanding their dataset relating to the price of their 
# listings on Amsterdam, North Holland, The Netherlands. For reference,
# this dataset was obtained via the location: 
#
#          http://insideairbnb.com/get-the-data.html
#                              ├── listings.csv.gz
#
# @note None
#
# @warning  None
#
#  Created: March 3, 2021
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

# make sure to install these packages before running:
# pip install numpy
# pip install pandas
# pip install plotly

import math
import numpy as np
import pandas as pd

import gzip # There is no need to pip install this module as it is 
            # contained within the standard library.

import plotly.graph_objects as go # low-level interface to figures, 
                                  # traces and layout

import plotly.express as px # Plotly Express is the easy-to-use, high-level
                            # interface to Plotly, which operates on "tidy"
                            # data and produces easy-to-style figures.

pd.set_option('display.max_rows', 50)
pd.set_option('display.min_rows', 50)

def percentage2float(percent_value):
    try:
        input_value = float(percent_value)

        if math.isnan(input_value):
            result_value = float(0)
        else:
            result_value = input_value/100
    except Exception as e:
        result_value = float(percent_value.strip('%'))/100

    return result_value

file_name = './listings.csv.gz'

the_compressed_file = gzip.open(file_name, 'rb')
airbnb_dataset_raw = the_compressed_file.read()

# For debugging, though the raw data is not yet processed and the output 
# would be unhelpful as yet:
#print(airbnb_dataset_raw)
#print()

# Compression : {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default ‘infer’ 
# for on-the-fly decompression of on-disk data. If ‘infer’ and 
# filepath_or_buffer is path-like, then detect compression from the 
# following extensions: ‘.gz’, ‘.bz2’, ‘.zip’, or ‘.xz’ (otherwise no 
# decompression).
#
# Reference: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
airbnb_dataset_df = pd.read_csv(file_name)
print(airbnb_dataset_df)
print()

print('Dataset dimensions of cleaned up Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_dataset_df.shape)
print()

# To ensure that we will have no issues plotting/visualizing the data,
# infer their proper data types:
airbnb_data = airbnb_dataset_df.infer_objects()

print('Data type of each column of cleaned up Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_data.dtypes)
print()

# Enable for debug. For now we don't care about 'name' as these are just 
# the Airbnb listing descriptions such as:
#
# 0                 Quiet Garden View Room & Super Fast WiFi
# 1             Studio with private bathroom in the centre 1
# 2          Lovely, spacious 1 bed apt in Center(with lift)
# 3        Romantic, stylish B&B houseboat in canal district
#amsterdam_host_name = airbnb_data['name']
#print(amsterdam_host_name)
#print()

# Enable for debug. For now we don't care about 'host_location' since
# we know they will all point to "Amsterdam, Noord-Holland, The Netherlands"  
# for corresponding data columns that are not 'NaN'. 
#amsterdam_host_location = airbnb_data['host_location']
#print(amsterdam_host_location)
#print()

# Drop all rows in the overall dataframe in which 'host_neighbourhood'
# is 'NaN'. Note that if you want to keep the resulting DataFrame of
# valid entries in the same variable, you must set:
#
# airbnb_data.dropna(subset=['host_neighbourhood'], inplace=True)
airbnb_data_dropped = airbnb_data.dropna(subset=['host_neighbourhood']) 

# For debug:
#print(airbnb_data_dropped)
#print()

print('Dataset dimensions of cleaned up (and DROPPED) Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_data_dropped.shape)
print()

amsterdam_host_neighbourhood = airbnb_data_dropped['host_neighbourhood']
print(amsterdam_host_neighbourhood)
print()

# Output some of the 'interesting' columns so we see what kind of data
# to be potentially visualized that we are playing with:
print(airbnb_data_dropped[['host_name', 'host_since', 'host_response_time',
     'host_response_rate', 'host_acceptance_rate', 'host_total_listings_count',
     'number_of_reviews', 'review_scores_rating']])
print()

# ==========
# Center the map on Amsterdam, Noord-Holland, The Netherlands per its 
# requisite latitude and longitude:
#
# Great reference for the gmplot package is here:
#
# https://pypi.org/project/gmplot/
# ==========

# Note that the API reference for gmplot states that:
#
# "While most functionality should be available as-is, some features 
# require a Google Maps API key".
#
# If needed, Google Maps API key can be obtained for free from here:
#
# https://developers.google.com/maps/documentation/javascript/get-api-key
#
#gmap = gmplot.GoogleMapPlotter(52.3676, 4.9041, 14, apikey="")

# Draw the map:
#gmap.draw('./amsterdam_map.html')

# Some column data visualizations, line graph:
#figure1 = go.Figure()
#figure1.add_trace(go.Scatter(x=airbnb_data_dropped['host_since'], 
#                            y=airbnb_data_dropped['number_of_reviews'],
#                            mode='markers',
#                            name='Number of Reviews',
#                            line=dict(color='red', width=1)
#))
#figure1.update_layout(title='Amsterdam, Noord-Holland - Airbnb Host Since Date/Number Of Reviews',
#                     xaxis_title='Airbnb Host Since Date',
#                     yaxis_title='Number Of Reviews')
#figure1.show()

# Some column data visualizations, bar chart:
#figure2 = px.bar(airbnb_data_dropped, x="host_acceptance_rate",y="host_name", 
#                 color='review_scores_rating', orientation='h',
#                 hover_data=["host_name", "host_neighbourhood", 
#                             "host_acceptance_rate", "review_scores_rating"],
#                 title='Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Acceptance Rate')
#
##figure2.update_traces(marker_color='violet')
#figure2.update_layout(title='Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Acceptance Rate',
#                     xaxis_title='Host Acceptance Rate',
#                     yaxis_title='Host Name (Hover Mouse For Host Neighbourhood)')
#
#figure2.show()

# Employ a list for now in the list comprehension for faster processing:
wide_data_rate = [percentage2float(x) for x in airbnb_data_dropped['host_acceptance_rate']]
#print(wide_data_rate)
#print()

cols = ['host_acceptance_rate']

# Now create the dataframe from the complete list as this approach is much much faster:
wide_data_format = pd.DataFrame(wide_data_rate, columns=cols, index=airbnb_data_dropped.index)

# Append more columns of interest directly from the existing dataframe
# after performing any necessary transformations:
wide_data_format['number_of_reviews'] = airbnb_data_dropped['number_of_reviews'].astype(float).apply(lambda x: round(x, 0))

wide_data_format['review_scores_rating'] = airbnb_data_dropped['review_scores_rating'].fillna(0)
wide_data_format['host_name'] = airbnb_data_dropped['host_name']
wide_data_format['host_neighbourhood'] = airbnb_data_dropped['host_neighbourhood']

print(wide_data_format)
print()

print('Data type of each column of wide format data:')
print(wide_data_format.dtypes)
print()

# The above transformations were all necessary because to plot "Bar chart
# with Wide Format Data", all the columns must be of the same type, which
# is not the case with our original data.
figure3 = px.bar(wide_data_format, x=["host_acceptance_rate", "number_of_reviews", "review_scores_rating"], y="host_name", orientation='h', hover_data=["host_name", "host_neighbourhood", "host_acceptance_rate", "review_scores_rating"], title="Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Acceptance Rate")

figure3.show()

figure4 = px.bar(wide_data_format, x="host_name", y=["host_acceptance_rate", "number_of_reviews", "review_scores_rating"], hover_data=["host_name", "host_neighbourhood", "host_acceptance_rate", "review_scores_rating"], title="Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Acceptance Rate")

figure4.update_xaxes(type='category')
figure4.show()
