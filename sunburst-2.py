#***********************************************************************
# @file
#
# Advancing on plotly sunburst plots by assaying some. Other plots have
# since been added to this script/module as well.
#
# @note 
#   Sunburst plots visualize hierarchical data spanning outwards radially
#   from root to leaves. Similar to Icicle charts and Treemaps, the 
#   hierarchy is defined by labels (names for px.icicle) and parent's 
#   attributes. The root starts from the center and children are added 
#   to the outer rings.
#
# @warning  None
#
#  Created: September 9, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import plotly # Plotly.js is an open source charting library written in javascript.
              # One of the coolest things about these charts is that all of them are interactive, as you can see in the example below. You can Zoom in and out, resize and move the axis, and much more.
import plotly.graph_objects as go
import plotly.express as px
from nose.tools import assert_equal

def version_to_int_list(version):
    return [int(s) for s in version.split('.')]

print('plotly.__version__:')
print(plotly.__version__)
print()

print('version_to_int_list(plotly.__version__):')
print(version_to_int_list(plotly.__version__))
print()

print('version_to_int_list(\'3.8.0\'):')
print(version_to_int_list('3.8.0'))
print()

# The comparison uses lexicographical ordering: first the first two items
# are compared, and if they differ this determines the outcome of the 
# comparison; if they are equal, the next two items are compared, and 
# so on, until either sequence is exhausted. Hence the pair of items at
# each index are compared in turn.
#
# A corollary of this is, two lists will only compare as equal if and only
# if they possess the same length and all pairs of items compare as equal.
#
# Note that the comparison of pairs will stop when either an unequal pair
# of items is found or--if the lists are of different lengths--the end of 
# the shorter list is reached.
assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may
# depend on the context. This is sometimes called chained assignment and
# should be avoided. See Returning a View versus Copy. [dataframe_loop_example.py]
pd.options.mode.chained_assignment = None

# ======================================================================
# We'll also be using 3 datasets available from kaggle to include further
# data for analysis and plotting.
# 
#  World happiness report dataset - Dataset also holds information about
#  GDP per capita, social support, life expectancy, generosity, and 
#  corruption.
#
#  Starbucks store location data - It has information about each Starbucks
#  store locations as well as their address, city, country, phone number,
#  latitude and longitude data.
#
#  Indian census data - It has information about the population of Indian
#  districts in 2001 and 2011.
# ======================================================================
starbucks_locations = pd.read_csv("Starbucks/directory.csv")

print('starbucks_locations:')
print(starbucks_locations)
print()

print('starbucks_locations.info():')
print(starbucks_locations.info())
print()

#world_countries_data = pd.read_csv("WorldHappinessReport/2019.csv")
world_countries_data = pd.read_csv("Countries_Of_The_World/countries of the world.csv")

# Create a new World column with value World for center (ultimate parent)
# of sunburst plot.
world_countries_data["World"] = "World" 

print('world_countries_data:')
print(world_countries_data)
print()

print('world_countries_data.info():')
print(world_countries_data.info())
print()

indian_district_population = pd.read_csv("IndianCensus/district wise population for year 2001 and 2011.csv")

# Create a new country column with value India for center (ultimate parent)
# of sunburst plot.
indian_district_population["Country"] = "India" 

print('indian_district_population:')
print(indian_district_population)
print()

print('indian_district_population.info():')
print(indian_district_population.info())
print()

# ======================================================================
# There are two ways to generate a sunburst chart using plotly. It provides
# two APIs for generating sunburst charts.
# 
#     plotly.express - It provides method named sunburst() to create 
#     sunburst charts.
#     plotly.graph_objects - It provides method named Sunburst() to create
#     charts.
# ======================================================================

# Plotly Express¶
# 
# The plotly has a module named express which provides easy to use method named sunburst() which can be used to create sunburst charts. It accepts dataframe containing data, columns to use for hierarchical, and column to use for actual values of the distribution. We can provide a list of columns with hierarchical relations as list to the pathattribute of the method. The values to use to decide sizes of distribution circles can be provided as a column name to thevaluesattribute. We can also providetitle,width, and height attribute of the figure. The sunburst() method returns figure object which can be used to show a chart by calling show() method on it.

# Starbucks Store Count Distribution World Wide Sunburst Chart
# 
# We'll need to prepare the dataset first in order to show Starbucks store counts distribution per city, and country worldwide. We'll be grouping the original Starbucks dataset according to Country, and City. Then we'll call count() on it which will count entry for each possible combination of Country and City. We also have introduceda new column named World which has all valuesthe same containing string World. We have created this column to createa circle inthe center to seethe total worldwide count.

starbucks_dist = starbucks_locations.groupby(by=["Country", "State/Province", "City"]).count()[["Store Number"]].rename(columns={"Store Number":"Count"})

# Create a new World column with value World for center (ultimate parent)
# of sunburst plot.
starbucks_dist["World"] = "World" 
starbucks_dist = starbucks_dist.reset_index()

print('starbucks_dist:')
print(starbucks_dist)
print()

print('starbucks_dist.info():')
print(starbucks_dist.info())
print()

figure_1 = px.sunburst(starbucks_dist,
                  # Notice how the first parent refers to the new World column?
                  path=["World", "Country", "State/Province", "City"], 
                  values='Count',
                  title="Starbucks Store Count Distribution World Wide [Country, State, City]",
                  width=750, height=750)
#figure_1.show()

figure_2 = px.sunburst(indian_district_population,
                  path=["Country", "State", "District",],
                  values='Population in 2011',
                  width=750, height=750,
                  title="Indian District Population Per State",
                  )
#figure_2.show()

figure_3 = px.sunburst(world_countries_data,
                  path=["World", "Region", "Country"],
                  values='Population',
                  width=750, height=750,
                  title="World Population Per Country Per Region",
                  )
#figure_3.show()

figure_3_1 = px.sunburst(world_countries_data,
                  path=["World", "Region", "Country"],
                  values='Population',
                  width=750, height=750,
                  color='Population',
                  title="World Population Per Country Per Region",
                  )
#figure_3_1.show()

figure_4 = px.sunburst(world_countries_data,
                  path=["World", "Region", "Country"],
                  values='Area (sq. mi.)',
                  width=750, height=750,
                  title="World Area Per Country Per Region",
                  )
#figure_4.show()


# World Population Distribution Per Country Per Region Color-Encoded By GDP Sunburst Chart
# 
# Below we have again plotted sunburst chart explaining population distribution per country per region but we have also color encoded each distribution according to GDP of that country/region. We can compare the population and GDP of the country based on this sunburst chart. We can notice that countries like India and China have less GDP even though having more population whereas countries like the US, Japan, Germany, UK, France, Australia, Hong Kong have less population but more GDP.
figure_3_2 = px.sunburst(world_countries_data,
                  path=["World", "Region", "Country"],
                  values='Population',
                  width=750, height=750,
                  color_continuous_scale="BrBG",
                  color='GDP ($ per capita)',
                  title="World Population Per Country Per Region Color-Encoded By GDP"
                  )
                  
# Northern Africa color coding seems incorrect perhaps due to GDP value being null:

# Substituting NaN values.
# Posted in Countries of the World 3 years ago
# 
# What would be the best approach to substitute NaN values? My take on this is to take the mean values over region in which the country is located. 

# Soumitri • 3 years ago • Options • Report • Reply
#
# My approach is to use he imputer and derive the median, substitute the median for the nan

#figure_3_2.show()


# World Population Per Country Per Region Color-Encoded By Area Sunburst Chart
# 
# Below we have again plotted population distribution per country per region of the world but this time we have color encoded data to the area of countries and region. This helps us compare the relationship between population and area. We can notice that countries like India are more but has less area compared to countries like Russia, the United States, Brazil which has visibly more area with less population.

figure_5 = px.sunburst(world_countries_data,
                  path=["World", "Region", "Country"],
                  values='Population',
                  width=750, height=750,
                  color_continuous_scale="RdYlGn",
                  color='Area (sq. mi.)',
                  title="World Population Per Country Per Region Color-Encoded By Area"
                  )
#figure_5.show()


# Plotly Graph Objects¶
# 
# The second way of creating a sunburst chart using plotly is using the Sunburst() method of the graph_objects module. We need to provide it a list of all possible combination of parent and child combination and their values in order to create a chart using this method.

# World Population Per Country Per Region Sunburst Chart

# In order to create a sunburst chart using graph_objects.Sunburst() method, we have done little preprocessing with data. The Sunburst() method expects that we provided all possible parent-child relationship labels and their values to it. We have region-country relation labels and values ready in the dataset but for getting world-region relationship labels and values we have grouped dataframe according to the region in order to get region-wise population counts. We have then combined labels in order to generate all possible parent-child relationship labels as well as values.

region_wise_pop = world_countries_data.groupby(by="Region").sum()[["Population"]].reset_index()

print('region_wise_pop:')
print(region_wise_pop)
print()

print('region_wise_pop.info():')
print(region_wise_pop.info())
print()

print('region_wise_pop.shape[0]:')
print(region_wise_pop.shape[0])
print()

parents = [""] + ["World"] *region_wise_pop.shape[0] + world_countries_data["Region"].values.tolist()
labels = ["World"] + region_wise_pop["Region"].values.tolist() + world_countries_data["Country"].values.tolist()
values = [world_countries_data["Population"].sum()] + region_wise_pop["Population"].values.tolist() + world_countries_data["Population"].values.tolist()

print('parents:')
print(parents)
print()

print('labels:')
print(labels)
print()

print('values:')
print(values)
print()

figure_6 = go.Figure(go.Sunburst(
    parents=parents,
    labels=labels,
    values=values,
))

figure_6.update_layout(title="World Population Per Country Per Region",
                  width=700, height=700)

#figure_6.show()

# World Population Per Country Per Region Sunburst Chart

# Below we have again created a sunburst chart of population distribution but this time it looks completely like the plotly.express module. We have set the branchvalues parameter to string value "total" which fills the whole circle. By default, the Sunburst() method does not create full circle sunburst charts.

region_wise_pop = world_countries_data.groupby(by="Region").sum()[["Population"]].reset_index()

parents = [""] + ["World"] *region_wise_pop.shape[0] + world_countries_data["Region"].values.tolist()
labels = ["World"] + region_wise_pop["Region"].values.tolist() + world_countries_data["Country"].values.tolist()
values  = [world_countries_data["Population"].sum()] + region_wise_pop["Population"].values.tolist() + world_countries_data["Population"].values.tolist()

figure_7 = go.Figure(go.Sunburst(
    parents=parents,
    labels=labels,
    values=values,
    branchvalues="total",
))

figure_7.update_layout(title="World Population Per Country Per Region",
                  width=700, height=700)

# figure_7.show()

# World Population and Area Distribution Per Country Per Region Sunburst Chart Subplots

# Below we have combined two sunburst charts into a single figure. One sunburst chart is about world population distribution per country per region and another is about area distribution per country per region. We can combine many related sunburst charts this way to show possible relationships. Please go through code to understand little preprocessing in order to create charts.

figure_8 = go.Figure()

parents = [""] + ["World"] *region_wise_pop.shape[0] + world_countries_data["Region"].values.tolist()
labels = ["World"] + region_wise_pop["Region"].values.tolist() + world_countries_data["Country"].values.tolist()
values  = [world_countries_data["Population"].sum()] + region_wise_pop["Population"].values.tolist() + world_countries_data["Population"].values.tolist()

figure_8.add_trace(go.Sunburst(
    parents=parents,
    labels= labels,
    values= values,
    domain=dict(column=0),
    name="Population Distribution"
))

region_wise_area = world_countries_data.groupby(by="Region").sum()[["Area (sq. mi.)"]].reset_index()

parents = [""] + ["World"] *region_wise_area.shape[0] + world_countries_data["Region"].values.tolist()
labels = ["World"] + region_wise_area["Region"].values.tolist() + world_countries_data["Country"].values.tolist()
values  = [world_countries_data["Area (sq. mi.)"].sum()] + region_wise_area["Area (sq. mi.)"].values.tolist() + world_countries_data["Area (sq. mi.)"].values.tolist()

figure_8.add_trace(go.Sunburst(
    parents=parents,
    labels= labels,
    values= values,
    domain=dict(column=1)
))

figure_8.update_layout(
    grid= dict(columns=2, rows=1),
    margin = dict(t=0, l=0, r=0, b=0),
    width=900, height=700
)

figure_8.show()
