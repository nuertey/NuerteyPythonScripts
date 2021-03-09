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
from numpy import inf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import gzip # There is no need to pip install this module as it is 
            # contained within the standard library.

import plotly.graph_objects as go # low-level interface to figures, 
                                  # traces and layout

import plotly.express as px # Plotly Express is the easy-to-use, high-level
                            # interface to Plotly, which operates on "tidy"
                            # data and produces easy-to-style figures.
from scipy import stats

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import variance_inflation_factor

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# For logarithm divide-by-zero warnings
np.seterr(divide = 'ignore') 
#np.seterr(divide = 'warn') 

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
#print(airbnb_dataset_df)
#print()

print('Dataset dimensions of cleaned up Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_dataset_df.shape)
print()

# To ensure that we will have no issues plotting/visualizing the data,
# infer their proper data types:
airbnb_data = airbnb_dataset_df.infer_objects()

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

# Further cleanups:
airbnb_data_dropped['price'] = airbnb_data_dropped['price'].replace('[\$,]', '', regex=True).astype(float)

print('Data type of each column of cleaned up Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_data_dropped.dtypes)
print()

# For debug:
#print(airbnb_data_dropped)
#print()

print('Dataset dimensions of cleaned up (and DROPPED) Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_data_dropped.shape)
print()

print('Generated descriptive and summary statistics for Airbnb Dataframe for Amsterdam after cleanup:')
print(airbnb_data_dropped.describe())
print()

print('Printed concise summary of the DataFrame:')
print(airbnb_data_dropped.info())
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
#print(host_neighbourhood_unique)
print(len(host_neighbourhood_unique))
print()
#print(latitude_unique)
print(len(latitude_unique))
print()
#print(longitude_unique)
print(len(longitude_unique))
print()

#figure0_2 = go.Figure()
#
#figure0_2.add_trace(go.Scattermapbox(
#        lat=latitude_unique,
#        lon=longitude_unique,
#        mode='markers',
#        marker=go.scattermapbox.Marker(
#            size=17,
#            color='rgb(255, 0, 0)',
#            opacity=0.7
#        ),
#        text=host_neighbourhood_unique,
#        hoverinfo='text'
#    ))
#
#figure0_2.add_trace(go.Scattermapbox(
#        lat=latitude_unique,
#        lon=longitude_unique,
#        mode='markers',
#        marker=go.scattermapbox.Marker(
#            size=8,
#            color='rgb(242, 177, 172)',
#            opacity=0.7
#        ),
#        hoverinfo='none'
#    ))
#
#figure0_2.update_layout(
#    title='Amsterdam, Noord-Holland, The Netherlands - AirBnB Host Listings',
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
#        zoom=12,
#        style='satellite-streets'
#    ),
#)
#
#figure0_2.show()

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
#print('Unique Amsterdam neighbourhoods (CLEANSED):')
#print(airbnb_data_dropped.neighbourhood_cleansed.unique())
#print()

neighbourhood_stats = airbnb_data_dropped.groupby(["host_neighbourhood"]).calculated_host_listings_count.sum().reset_index()
sorted_neighbourhood_stats = neighbourhood_stats.sort_values(by=['calculated_host_listings_count'], ascending=True)

print(sorted_neighbourhood_stats)
print()

#figure1_2 = px.histogram(neighbourhood_stats, x="host_neighbourhood", y="calculated_host_listings_count")
#figure1_2.show()

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

airbnb_data_dropped['review_scores_rating'] = airbnb_data_dropped['review_scores_rating'].fillna(0)
wide_data_format['review_scores_rating'] = airbnb_data_dropped['review_scores_rating']
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
     'host_identity_verified']])
print()

print('Preparing for prediction 2:')
# bathrooms is all NaNs so ignore:
print(airbnb_data_dropped[['property_type', 'room_type', 'accommodates',
     'bathrooms_text', 'bedrooms', 'beds', 'amenities', 'price']])
print()

# As we are about to begin, ensure to replace all NaNs in other interested
# category variables with equivalent '0'-like values.
airbnb_data_dropped['bathrooms_text'] = airbnb_data_dropped['bathrooms_text'].fillna("0 baths")
airbnb_data_dropped['bedrooms'] = airbnb_data_dropped['bedrooms'].fillna(0)
airbnb_data_dropped['beds'] = airbnb_data_dropped['beds'].fillna(0)

# Boxplots of 'price' distributions grouped by the values of a third 
# variable can be created using the option by. Here are some examples.

# A box plot (or box-and-whisker plot) shows the distribution of quantitative
# data in a way that facilitates comparisons between variables or across
# levels of a categorical variable. The box shows the quartiles of the 
# dataset while the whiskers extend to show the rest of the distribution,
# except for points that are determined to be “outliers” using a method
# that is a function of the inter-quartile range.

# Further, per Wikipedia:
#
# "The spacings between the different parts of the box indicate the degree
# of dispersion (spread) and skewness in the data, and show outliers. 
# In addition to the points themselves, they allow one to visually 
# estimate various L-estimators, notably the interquartile range, 
# midhinge, range, mid-range, and trimean."

## boxplot1.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["accommodates"])
#plt.show()
#
## boxplot2.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["property_type"])
#plt.show()
#
## boxplot3.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["bathrooms_text"])
#plt.show()
#
## boxplot4.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["host_neighbourhood"])
#plt.show()
#
## boxplot5.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["calculated_host_listings_count"])
#plt.show()
#
## boxplot6.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["room_type"])
#plt.show()
#
## boxplot7.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["bedrooms"])
#plt.show()
#
## boxplot8.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["beds"])
#plt.show()
#
## boxplot9_1.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["host_is_superhost"])
#plt.show()
#
## boxplot9_2.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["host_identity_verified"])
#plt.show()
#
## boxplot9_3.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["number_of_reviews"])
#plt.show()
#
## boxplot9_4.png
#sns.boxplot(y=airbnb_data_dropped["price"], x=airbnb_data_dropped["review_scores_rating"])
#plt.show()

# Based upon analysis of the various boxplots, removing outliers: price > 2000
outliers_data_dropped = airbnb_data_dropped[airbnb_data_dropped["price"] < 2000]

logarithm_listing_price = np.log(outliers_data_dropped["price"])
#print("Logarithm of Listing Price:")
#print(logarithm_listing_price)
#print()

# Histograms of listing price and log of listing price for further price
# data visualization and comparison:
#figure5 = go.Figure()
#figure5.add_trace(go.Histogram(x=outliers_data_dropped["price"], 
#                               name='listing price',
#                               marker_color='#0023FF', #Bluebonnet
#                               opacity=0.75))
#figure5.update_layout(
#    title_text='Listing Price Histogram', # title of plot
#    xaxis_title_text='Price', # xaxis label
#    yaxis_title_text='Frequency', # yaxis label
#    bargap=0.2, # gap between bars of adjacent location coordinates
#    bargroupgap=0.1 # gap between bars of the same location coordinates
#)
#figure5.show()
#
#figure6 = go.Figure()
#figure6.add_trace(go.Histogram(x=logarithm_listing_price, 
#                                 name='logarithm of listing price',
#                                 marker_color='#E36414', #Metallic Orange
#                                 opacity=0.75))
#figure6.update_layout(
#    title_text='Logarithm of Listing Price Histogram', # title of plot
#    xaxis_title_text='Logarithm of Price', # xaxis label
#    yaxis_title_text='Frequency', # yaxis label
#    bargap=0.2, # gap between bars of adjacent location coordinates
#    bargroupgap=0.1 # gap between bars of the same location coordinates
#)
#figure6.show()

print('Maximum listing price details:')
max_price_details = outliers_data_dropped[outliers_data_dropped['price']==outliers_data_dropped['price'].max()]
print(max_price_details[['amenities', 'host_since', 'host_neighbourhood',
     'price', 'property_type', 'number_of_reviews', 'review_scores_rating',
     'accommodates']])
print()

print('Minimum listing price details:')
min_price_details = outliers_data_dropped[outliers_data_dropped['price']==outliers_data_dropped['price'].min()]
print(min_price_details[['amenities', 'host_since', 'host_neighbourhood',
     'price', 'property_type', 'number_of_reviews', 'review_scores_rating',
     'accommodates']])
print()

#=================================
# OLS Prediction Preparation here:
#=================================
# - VARIABLES:
#
# host_is_superhost                                object
# host_neighbourhood                               object
# host_identity_verified                           object
# property_type                                    object
# room_type                                        object
# accommodates                                      int64
# bathrooms_text                                   object
# bedrooms                                        float64
# beds                                            float64
# number_of_reviews                                 int64
# review_scores_rating                            float64
# calculated_host_listings_count                    int64

print(outliers_data_dropped.info())
print()

# Sanity check (and simplify if possible) category-type variables:
#print(outliers_data_dropped["property_type"].value_counts())
#print()
#print(outliers_data_dropped["room_type"].value_counts())
#print()
#print(outliers_data_dropped["bathrooms_text"].value_counts())
#print()

ols_model_data_frame = outliers_data_dropped[['accommodates', 'bedrooms', 'beds', 'number_of_reviews', 'review_scores_rating', 'calculated_host_listings_count']].copy()

# Convert categorical variable into dummy/indicator variables. Note that
# it is recommended leaving "drop_first=False" (the default). If drop_first=True,
# you have no way to know from the dummies dataframe alone what the name
# of the "first" dummy category column/variable was, so that operation
# becomes non-invertible. Also, further note that by default, dummy_na=False.
# This is precisely what we want, and that option would have only caused
# issues if our category variables had had NaN values. But we have already
# ensured that this is not the case by our previous 'cleanings' operations,
# and have confirmed so with the "outliers_data_dropped.info()" call on line 577.
dummies_superhost = pd.get_dummies(outliers_data_dropped["host_is_superhost"],
                                   drop_first=False, dummy_na=False)
dummies_superhost.columns = ['false', 'true'] # Differentiate from dummies_identity_verified
#print(dummies_superhost)
#print()

dummies_neighbourhood = pd.get_dummies(outliers_data_dropped["host_neighbourhood"])
#print(dummies_neighbourhood)
#print()

dummies_identity_verified = pd.get_dummies(outliers_data_dropped["host_identity_verified"])
dummies_identity_verified.columns = ['no', 'yes'] # Differentiate from dummies_superhost
#print(dummies_identity_verified)
#print()

dummies_property_type = pd.get_dummies(outliers_data_dropped["property_type"])
#print(dummies_property_type)
#print()

dummies_room_type = pd.get_dummies(outliers_data_dropped["room_type"])
#print(dummies_room_type)
#print()

dummies_bathrooms_text = pd.get_dummies(outliers_data_dropped["bathrooms_text"])

# Strip spaces in column names and replace with underscore(_) as this is
# bad python practice and it also causes Panda DataFrame slicing to fail.
dummies = [dummies_superhost, dummies_neighbourhood, dummies_identity_verified,
           dummies_property_type, dummies_room_type, dummies_bathrooms_text]

for dummy in dummies:
    new_column_names = dummy.columns.str.strip().str.replace('\s+', '_')
    dummy.columns = new_column_names

#print(dummies_bathrooms_text)
#print()

# More verifications of dimension matches:
#print(len(logarithm_listing_price))
#print()
#
#print(len(dummies_superhost))
#print()
#
#print(len(dummies_neighbourhood))
#print()
#
#print(len(dummies_identity_verified))
#print()
#
#print(len(dummies_property_type))
#print()
#
#print(len(dummies_room_type))
#print()
#
#print(len(dummies_bathrooms_text))
#print()

# For debugging Python esoteric syntax for Pandas DataFrame slicing:
#print(list(dummies_superhost.columns.values))
#print()

# Add new columns of dummy variables to our ols_model_data_frame:
for dummy in dummies:
    ols_model_data_frame[list(dummy.columns.values)] = dummy[list(dummy.columns.values)]

# Our complete variables DataFrame for modeling:
#print(ols_model_data_frame)
#print()

print(ols_model_data_frame.info())
print()

# Calculate our correlation matrix with Numpy then:
our_np_array = ols_model_data_frame.values # We want a numpy array
the_correlation_matrix = np.corrcoef(our_np_array.T)
print("Using Numpy, here is our computed correlation matrix:")
print(the_correlation_matrix)
print()

print(the_correlation_matrix.shape)
print()

# Calculate our correlation matrix with Pandas.DataFrame then:
the_correlation_matrix2 = ols_model_data_frame.corr()
print("For validation, using inherent Pandas DataFrame, here is our computed correlation matrix:")
print(the_correlation_matrix2)
print()
print(the_correlation_matrix2.info())
print()

# Visualize as correlation_matrix_1.png then:
#sns.set_theme()
#cmap = sns.color_palette("flare", as_cmap=True)
#sns.heatmap(the_correlation_matrix2, cmap=cmap, vmin=-0.5, vmax=0.5, center=0);
#plt.show()

# Visualize as correlation_matrix_2.png then:
#mask = np.triu(np.ones_like(the_correlation_matrix2, dtype=bool))
#f, ax = plt.subplots(figsize=(9, 9))
#cmap = sns.diverging_palette(240, 20, as_cmap=True)
## cmap = sns.choose_diverging_palette()
#_ = sns.heatmap(
#    the_correlation_matrix2, mask=mask, cmap=cmap, vmax=.3, center=0, square=True,
#    linewidths=.5, cbar_kws={"shrink": .5}
#    )
#plt.show()

# Ensure the target variable 'log_price' is Normally distributed, and
# its kurtosis and skewness are normal. Just as a comparison try the same
# with the false presumption that unadulterated 'price' it self is the 
# target variable:

# Skewness  A measure of the symmetry of the data about the mean. 
# Normally-distributed errors should be symmetrically distributed about 
# the mean (equal amounts above and below the line).
# 
# Kurtosis  A measure of the shape of the distribution. Compares the 
# amount of data close to the mean with those far away from the mean 
# (in the tails).
# 
# Source: https://www.datarobot.com/blog/ordinary-least-squares-in-python/

# Plot a histogram and kernel density estimate:
#sns.distplot(outliers_data_dropped['price'], kde=True)
#figure10 = plt.figure()
#result = stats.probplot(outliers_data_dropped['price'], plot=plt)
#plt.show()

# Observed printout:
#
# Skewness: 4.169105
# Kurtosis: 35.177666
print("Skewness: %f" % outliers_data_dropped['price'].skew())
print("Kurtosis: %f" % outliers_data_dropped['price'].kurt())
print()

# Seaborn will not like infinity in the dataset so detect them, observe if
# they are actually there, and replace with reasonable values.
#print(logarithm_listing_price[logarithm_listing_price == -inf])
#print()

# This one was not detected so no need to worry about +infinity
#print(logarithm_listing_price[logarithm_listing_price == inf])
#print()

# Replace -infinity with 0.
logarithm_listing_price[logarithm_listing_price == -inf] = 0

#sns.distplot(logarithm_listing_price, kde=True)
#figure11 = plt.figure()
#result = stats.probplot(logarithm_listing_price, plot=plt)
#plt.show()

# Observed printout:
#
# Skewness: -0.385103
# Kurtosis: 5.437960
print("Skewness: %f" % logarithm_listing_price.skew())
print("Kurtosis: %f" % logarithm_listing_price.kurt())
print()

# ======================================================================
# Obviously the better values are the logarithm of the listing price as 
# even a visual inspection of our earlier histograms already indicated.
# So we will rather use that as our target variable in our OLS prediction.
# ======================================================================

# ===============
# OLS Regression:
# ===============

# Specify the constant term. Note that an intercept is not included by 
# default and should be added by the user:
ols_model_data_frame = sm.add_constant(ols_model_data_frame, prepend=False)

# Describe the model:
ols_model = sm.OLS(logarithm_listing_price, ols_model_data_frame)

# Fit the model:
results = ols_model.fit()

# OLS Regression results and summary:
print(results.summary())
print()

# TBD: Outline and interpret what the summary means here.

print(results.params)
print()

# This produces our four regression plots for "number_of_reviews"
#figure12 = plt.figure(figsize=(15,8))
#figure12 = sm.graphics.plot_regress_exog(results, "number_of_reviews", fig=figure12)
#plt.show()

# This produces our four regression plots for "calculated_host_listings_count"
#figure13 = plt.figure(figsize=(15,8))
#figure13 = sm.graphics.plot_regress_exog(results, "calculated_host_listings_count", fig=figure13)
#plt.show()

# This produces our four regression plots for "accommodates"
#figure14 = plt.figure(figsize=(15,8))
#figure14 = sm.graphics.plot_regress_exog(results, "accommodates", fig=figure14)
#plt.show()

# This produces our four regression plots for "bedrooms"
#figure15 = plt.figure(figsize=(15,8))
#figure15 = sm.graphics.plot_regress_exog(results, "bedrooms", fig=figure15)
#plt.show()

# Draw a plot to compare the true relationship to OLS predictions:
#prstd, iv_l, iv_u = wls_prediction_std(results)
#
#fig, ax = plt.subplots(figsize=(8,6))
#ax.plot(logarithm_listing_price, 'o', label="Data")
#ax.plot(results.fittedvalues, 'r--.', label="Predicted")
#ax.plot(iv_u, 'r--')
#ax.plot(iv_l, 'r--')
#legend = ax.legend(loc="best")
#plt.show()

# ==================================================================
# Diagnostics, Goodness-of-Fit and Specification tests on the model:
# ==================================================================

# Full list of attributes:
#print(dir(results))
#print()

# Rainbow test for linearity:
stat_F_test, pvalue_test = sm.stats.linear_rainbow(results)
print("stat_F_test, pvalue_test")
print(stat_F_test, pvalue_test)
print()

# Plot partial regression for 'accommodates':
#sm.graphics.plot_partregress(endog='price', exog_i='accommodates',
#                             exog_others=['bedrooms', 'number_of_reviews', 'calculated_host_listings_count'],
#                             data=outliers_data_dropped, obs_labels=False)
#plt.show()

# Plot partial regression for 'number_of_reviews':
sm.graphics.plot_partregress(endog='price', exog_i='number_of_reviews',
                             exog_others=['bedrooms', 'review_scores_rating', 'calculated_host_listings_count'],
                             data=outliers_data_dropped, obs_labels=False)
plt.show()
