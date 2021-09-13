#***********************************************************************
# @file
#
# Cufflinks plotting library tutorials.
#
# @note 
#   Cufflinks is a library that lets us generate interactive charts based
#   on plotly directly from pandas dataframe by calling iplot() or 
#   figure() method on it.
#
# @warning  None
#
#  Created: September 12, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import cufflinks as cf

import plotly
import plotly.graph_objects as go
import plotly.express as px

from numpy import array
from nose.tools import assert_equal
from sklearn.datasets import load_iris, load_wine
from sklearn.preprocessing import MinMaxScaler

setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

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

print('cufflinks.__version__:')
print(cf.__version__)
print()

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may
# depend on the context. This is sometimes called chained assignment and
# should be avoided. See Returning a View versus Copy. [dataframe_loop_example.py]
pd.options.mode.chained_assignment = None

print("List of Cufflinks Themes: ", cf.getThemes())
print()

cf.set_config_file(theme='pearl', sharing='public', offline=True)

cf.datagen.lines(1, 500).ta_plot(study="sma", periods=[13, 21, 55])

iris = load_iris()

iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Create new column in DataFrame by using list comprehension on data:
iris_df["FlowerType"] = [iris.target_names[t] for t in iris.target]

print('iris_df:')
print(iris_df)
print()

print('iris_df.info():')
print(iris_df.info())
print()

iris_df.iplot(kind="scatter",
              x="sepal length (cm)", 
              y='sepal width (cm)',
              mode='markers',
              xTitle="Sepal Length (CM)", 
              yTitle="Sepal Width (CM)",
              title="Sepal Length vs Sepal Width Relationship"
             )

# Below we have created another scatter plot which is exactly the same 
# as the previous scatter chart with only one difference which is that
# we have colored points according to different flower types. We have
# used the figure() method to create a chart this time which has the same
# parameters as iplot(). We have passed the column name to the categories
# parameter in order to color points on a scatter chart according to their
# flower type. We also have overridden the default theme from pearl to
# white by setting the theme parameter.
iris_df.figure(kind="scatter",
               x="sepal length (cm)", 
               y='sepal width (cm)',
               mode='markers',
               categories="FlowerType",
               theme="white",
               xTitle="Sepal Length (CM)", 
               yTitle="Sepal Width (CM)",
               title="Sepal Length vs Sepal Width Relationship Color-encoded by Flower Type"
              )

# Below we have again created the same chart as the first scatter chart
# but have added the regression line to the data as well by setting bestfit
# parameter to True. We have also changed the point type in a scatter chart.
iris_df.iplot(kind="scatter",
              x="sepal length (cm)", 
              y='sepal width (cm)',
              mode='markers',
              colors="tomato",  
              size=8, 
              symbol="circle-open-dot",
              bestfit=True, 
              bestfit_colors=["dodgerblue"],
              xTitle="Sepal Length (CM)", 
              yTitle="Sepal Width (CM)",
              title="Sepal Length vs Sepal Width Relationship along with Best Fit Line"
             )

# ======================================================================
# Bar Charts
#
# The second chart type that we'll introduce is a bar chart.
# ======================================================================
wine = load_wine()

wine_df = pd.DataFrame(data=wine.data, columns=wine.feature_names)

# Create new column in DataFrame by using list comprehension on data:
wine_df["WineType"] = [wine.target_names[t] for t in wine.target]

print('wine_df:')
print(wine_df)
print()

print('wine_df.info():')
print(wine_df.info())
print()

# We'll first create a dataframe that has average ingredients per wine
# type. We can call groupby() method on the wine dataframe to group 
# records according to WineType and then take the mean of that records 
# to get the average of each ingredient per wine type. 
avg_wine_df = wine_df.groupby(by=["WineType"]).mean()

# We then drop two columns from the dataset because both have very high
# values which can skew our charts:
avg_wine_df = avg_wine_df.drop(columns=["magnesium", "proline"])

print('avg_wine_df:')
print(avg_wine_df)
print()

print('avg_wine_df.info():')
print(avg_wine_df.info())
print()

# Below we have created our first bar chart by setting kind parameter to
# bar. We have passed alcohol as y value in order to plot bar chart of
# average alcohol used per wine type. We have also overridden default
# pearl theme to solar theme:
avg_wine_df.iplot(kind="bar", 
                  y="alcohol",
                  colors=["dodgerblue"],
                  bargap=0.5,
                  dimensions=(500, 500),
                  theme="solar",
                  xTitle="Wine Type", 
                  yTitle="Avg. Alcohol", 
                  title="Average Alcohol Per Wine Type"
                 )

# We have again created same chart as previous step but this time we have
# laid out bars horizontally. All other parameters are same as previous
# step. We can change bars from vertical to horizontal by setting
# orientation parameter to h.
avg_wine_df.iplot(kind="bar", 
                  y="alcohol",
                  yTitle="Wine Type", 
                  xTitle="Avg. Alcohol", 
                  title="Average Alcohol Per Wine Type",
                  colors=["tomato"], 
                  bargap=0.5,
                  sortbars=True,
                  dimensions=(500, 400),
                  theme="polar",
                  orientation="h"
                 )



# Apple OHLC Dataset: It has information about Apple OHLC(Open, High, Low
# & Close) data from Apr 2019 - Mar 2020. The dataset can be easily 
# downloaded from yahoo finance as CSV.
apple_df = pd.read_csv("AAPL.csv", index_col=0, parse_dates=True)

print('apple_df:')
print(apple_df)
print()

print('apple_df.info():')
print(apple_df.info())
print()
