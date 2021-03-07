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

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

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
     'number_of_reviews', 'review_scores_rating', 'calculated_host_listings_count']])
print()

# ====================================================================
# Center a satellite map on Amsterdam, Noord-Holland, The Netherlands
# per its requisite latitude and longitude:
# ====================================================================
# To plot on Mapbox maps with Plotly, a Mapbox account and a public 
# Mapbox Access Token is needed. Let's just use mine:
token = open(".mapbox_token").read() 

#figure0_1 = go.Figure(go.Scattermapbox(
#    mode = "markers+text+lines",
#    lon = [4.9041], lat = [52.3676],
#    marker = {'size': 20, 'symbol': ["car"]},
#    text = ["Transportation"],textposition = "bottom right"))
#
#figure0_1.update_layout(
#    title='Amsterdam, Noord-Holland, The Netherlands',
#    autosize=True,
#    hovermode='closest',
#    showlegend=False,
#    mapbox=dict(
#        accesstoken=token,
#        bearing=0,
#        center=dict(
#            lat=52.3676,
#            lon=4.9041
#        ),
#        pitch=0,
#        zoom=10,
#        style='satellite-streets'
#    ),
#)
#
#figure0_1.show()

# Ensure we have the same row dimensions for these before plotting:
#host_neighbourhood_unique = airbnb_data_dropped.host_neighbourhood.unique()
#latitude_unique = airbnb_data_dropped.latitude.unique()
#longitude_unique = airbnb_data_dropped.longitude.unique()

# The above seems to give incorrect dimensions, probably because of 
# lingering decimal points and misspelt neighbourhoods so use the below
# approach instead for correct results. 
host_neighbourhood_unique = airbnb_data_dropped.host_neighbourhood
latitude_unique = airbnb_data_dropped.latitude
longitude_unique = airbnb_data_dropped.longitude

print('Unique Neighbourhood, Latitude and Longitude of Amsterdam neighbourhoods:')
print(host_neighbourhood_unique)
print(len(host_neighbourhood_unique))
print()
print(latitude_unique)
print(len(latitude_unique))
print()
print(longitude_unique)
print(len(longitude_unique))
print()

figure0_2 = go.Figure()

figure0_2.add_trace(go.Scattermapbox(
        lat=latitude_unique,
        lon=longitude_unique,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=host_neighbourhood_unique,
        hoverinfo='text'
    ))

figure0_2.add_trace(go.Scattermapbox(
        lat=latitude_unique,
        lon=longitude_unique,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
        hoverinfo='none'
    ))

figure0_2.update_layout(
    title='Amsterdam, Noord-Holland, The Netherlands - AirBnB Host Listings',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=token,
        bearing=0,
        center=dict(
            lat=52.3676,
            lon=4.9041
        ),
        pitch=0,
        zoom=12,
        style='satellite-streets'
    ),
)

figure0_2.show()

# ============================================
# Some column data visualizations, line graph:
# ============================================
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

# ======================================================================
# Histograms follow here:
#
# Aggregate 'calculated_host_listings_count' column data for each unique
# neighbourhood. That sounds like an interesting dataset to visualize.
# i.e. which neighbourhoods have the most listings etc.
# ======================================================================
print('Unique Amsterdam neighbourhoods:')
print(airbnb_data_dropped.host_neighbourhood.unique())
print()

# This CLEANSED dataset seems very weird so don't use it.
print('Unique Amsterdam neighbourhoods (CLEANSED):')
print(airbnb_data_dropped.neighbourhood_cleansed.unique())
print()

neighbourhood_stats = airbnb_data_dropped.groupby(["host_neighbourhood"]).calculated_host_listings_count.sum().reset_index()
sorted_neighbourhood_stats = neighbourhood_stats.sort_values(by=['calculated_host_listings_count'], ascending=True)

print(sorted_neighbourhood_stats)
print()

#figure1_2 = px.histogram(neighbourhood_stats, x="host_neighbourhood", y="calculated_host_listings_count")
#figure1_2.show()
#
#figure1_3 = px.histogram(sorted_neighbourhood_stats, x="host_neighbourhood", y="calculated_host_listings_count")
#figure1_3.show()

# I "prepared" the data for the above histograms manually with Pandas
# for better visualization, but we can also have plotly automagically do
# the aggregation for us through the "Aggregation Function" and superimpose
# both on the same plot for us:
#
# https://plotly.com/python/histograms/
#figure1_4 = go.Figure()
#figure1_4.add_trace(go.Histogram(histfunc="count", y=airbnb_data_dropped['calculated_host_listings_count'], x=airbnb_data_dropped['host_neighbourhood'], name="count of listings"))
#figure1_4.add_trace(go.Histogram(histfunc="sum", y=airbnb_data_dropped['calculated_host_listings_count'], x=airbnb_data_dropped['host_neighbourhood'], name="cumulative sum for neighborhood"))
#figure1_4.show()

# At this juncture, and judging from the above histogram visualizations
# and the printed output, sorted_neighbourhood_stats, one can roughly
# estimate that since the host_neighbourhood of Jordaan has the most 
# listings (8143), it will perhaps have lower listing prices than
# host_neighbourhood's such as LB of Hillingdon, Friedrichshain, Fulham,
# Hampstead, Shepherd's Bush, etc., which have only 1. They would perhaps
# command the highest prices. I am basing this on the strict economic 
# interpretation that scarcity increases value, demand and attraction.


# ======================================================================
# Attempt to plot "Bar chart with Wide Format Data" i.e. 3 columns of data
# at once. All the columns must be of the same type, which is not the case
# with our original data. So the transformations to follow are necessary.
#
# https://plotly.com/python/bar-charts/
# ======================================================================

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
# with Wide Format Data" i.e. 3 columns of data at once, all the columns
# must be of the same type, which is not the case with our original data.
#figure3 = px.bar(wide_data_format, x=["host_acceptance_rate", "number_of_reviews", "review_scores_rating"], y="host_name", orientation='h', hover_data=["host_name", "host_neighbourhood", "host_acceptance_rate", "review_scores_rating"], opacity=1, title="Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Acceptance Rate")
#
## Attempt to make the background transparent.
#figure3.update_layout({
#     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
#})
#
#figure3.show()
#
#figure4 = px.bar(wide_data_format, x="host_name", y=["host_acceptance_rate", "number_of_reviews", "review_scores_rating"], opacity=1, title="Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Acceptance Rate")
#
#figure4.update_xaxes(type='category')
#
## Attempt to make the background transparent.
#figure4.update_layout({
#     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
#})
#
#figure4.show()

# ===================================================================
# Some column data visualizations, bar chart with just 1 column data:
# ===================================================================
#figure2 = px.bar(wide_data_format, x="host_name",y="number_of_reviews", 
#                 color='review_scores_rating',
#                 hover_data=["host_name", "host_neighbourhood", 
#                             "host_acceptance_rate", "review_scores_rating"],
#                 title='Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Number of Reviews')
#
##figure2.update_traces(marker_color='violet')
#figure2.update_layout(title='Amsterdam, Noord-Holland - Airbnb Host Name/Neighbourhood Versus Number of Reviews',
#                     xaxis_title='Host Name (Hover Mouse For Host Neighbourhood)',
#                     yaxis_title='Number of Reviews')
#
#figure2.update_xaxes(type='category')
#
## Attempt to make the background transparent.
#figure2.update_layout({
#     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
#})
#
#figure2.show()

# ===================================================================
# Analysis/dataset inspection to select variables for OLS prediction:
# ===================================================================
# Output some of the 'interesting' columns so we see what kind of data
# to be potentially used for prediction that we are playing with:
print('Preparing for prediction 1:')

# neighbourhood all point to "Amsterdam, Noord-Holland, The Netherlands"
# so don't care:
# neighbourhood_group_cleansed is all NaNs so ignore:
# neighbourhood_cleansed seems weird so as a caution don't use it. Prefer
# host_neighbourhood:
print(airbnb_data_dropped[['neighborhood_overview', 'host_about', 'host_is_superhost',
     'host_identity_verified', 'latitude', 'longitude']])
print()

print('Preparing for prediction 2:')
# bathrooms is all NaNs so ignore:
print(airbnb_data_dropped[['property_type', 'room_type', 'accommodates',
     'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price']])
print()

