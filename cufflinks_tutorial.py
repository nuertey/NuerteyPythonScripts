#***********************************************************************
# @file
#
# Cufflinks - Create Plotly charts from Pandas DataFrame with just one
#             line of code. Following are some cufflinks plotting library
#             tutorials.
#
# @note 
#   Cufflinks is a library that lets us generate interactive charts based
#   on plotly directly from pandas dataframe by calling iplot() or the
#   figure() method on the dataframe.
#
# @warning  None
#
#  Created: September 12, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cufflinks as cf

import plotly
import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime
from dateutil.relativedelta import relativedelta
from numpy import array
from matplotlib.pyplot import *
from nose.tools import assert_equal
from sklearn.datasets import load_iris, load_wine
from sklearn.preprocessing import MinMaxScaler

setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

matplotlib.use('TkAgg')

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

# ======================================================================
# Example cufflinks plot:
cf.datagen.lines(1, 500).ta_plot(study="sma", periods=[13, 21, 55])

# ======================================================================
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

# Below we have created side by side bar chart by directly calling iplot()
# on the whole dataframe. We have set sortbars parameter to True in order
# to sort bars from the highest quantity to the lowest. We have also 
# overridden the default chart theme from pearl to ggplot.
avg_wine_df.iplot(kind="bar",
                  sortbars=True,
                  xTitle="Wine Type",
                  yTitle="Average Ingredient Value", 
                  title="Average Ingredients Per Wine Type",
                  theme="ggplot"
                  )

# We can create a stacked bar chart easily by setting barmode parameter
# to stack. Below we have created a stacked bar chart to show the average
# distribution of ingredients per wine type.
avg_wine_df.iplot(kind="bar",
                  barmode="stack",
                  xTitle="Wine Type",
                  yTitle="Average Ingredient Value",  
                  title="Average Ingredients Per Wine Type",
                  opacity=1.0,
                 )

# We can create an individual bar chart for columns of the dataframe by
# setting the subplots parameter to True. It'll create a different bar
# charts for each column of the dataframe. We have set the keys parameter
# to list of columns to use from the dataframe so that bar charts will
# be created for these 4 columns. We can pass a list of columns to use
# from the dataframe as a list to the keys parameter.
avg_wine_df.iplot(kind="bar",
                  subplots=True,
                  sortbars=True,
                  keys = ["ash", "total_phenols", "hue", "malic_acid"],
                  xTitle="Wine Type",
                  yTitle="Average Ingredient Value",
                  title="Average Ingredients Per Wine Type",
                  theme="henanigans"
                  )



# ----------------------------------------------------------------------
# https://stackoverflow.com/questions/33149428/modify-the-legend-of-pandas-bar-plot/33150133

fig, ax1 = plt.subplots()
df = pd.DataFrame({'A':26, 'B':20}, index=['N'])
df.plot(kind='bar', ax=ax1)
#ax1 = df.plot(kind='bar') # "same" as above
ax1.legend(["AAA", "BBB"]);
plt.show()

# Alternate way:
df1 = pd.DataFrame({'A':26, 'B':20}, index=['N'])
ax2 = df1.plot(kind='bar')
ax2.hlines(23, -.5,.5, linestyles='dashed')
ax2.annotate('average',(-0.4,23.5))
ax2.legend(["AAA", "BBB"]);
plt.show()

# ======================================================================
# Line Charts
#
# The third chart type that we'll introduce is a line chart. We can easily
# create a line chart by just calling iplot() method on the dataframe
# and giving which column to use for the x and y-axis. 
# ======================================================================

# Apple OHLC Dataset: It has information about Apple OHLC(Open, High, Low
# & Close) data from September,2020 - September,2021. The dataset was 
# downloaded from yahoo finance as CSV. URL:
#
# https://finance.yahoo.com/quote/AAPL/history?p=AAPL
apple_df = pd.read_csv("AAPL.csv", index_col=0, parse_dates=True)

print('apple_df:')
print(apple_df)
print()

print('apple_df.info():')
print(apple_df.info())
print()

# If we don't give  value for the x-axis then it'll use the index of the
# dataframe as the x-axis. In our case, the index of the dataframe is the
# date for prices. We have plotted below the line chart of Open price over the whole period.
apple_df.iplot(y="Open",
               xTitle="Date", 
               yTitle="Price ($)", 
               title="Open Price From September,2020 - September,2021"
              )

# We can plot more than one line on the chart by passing a list of column
# names from the dataframe as a list to the y parameter and it'll add 
# one line per column to the chart.
apple_df.iplot(y=["Open", "High", "Low", "Close"],
               width=2.0,
               xTitle="Date", 
               yTitle="Price ($)", 
               title="OHLC Price From September,2020 - September,2021"
              )
              
# Below we have created a line chart with two-line where 2nd line has a
# separate y-axis on the right side. We can set the secondary parameter
# by giving the column name to the secondary_y parameter and the axis 
# title for the secondary y-axis to secondary_y_title. This can be very
# useful when the quantities which we want to plot are on a different scale.
apple_df.iplot(y="Open",
               secondary_y="Close", 
               secondary_y_title="Close Price ($)",
               xTitle="Date", 
               yTitle="Open Price ($)", 
               title="Open Price From September,2020 - September,2021"
              )

# Below we have again created a line chart but this time using mode as
# lines+markers which will add both line and points to the chart. We have
# also modified the default gridcolor to black from gray.
apple_df.iplot(y="Open",
               mode="lines+markers", 
               size=4.0,
               colors=["dodgerblue"],
               gridcolor="black",
               xTitle="Date", 
               yTitle="Price ($)", 
               title="Open Price From September,2020 - September,2021"
              )

# Below is another another example with subplots:
apple_df.iplot(y=["Open", "High", "Low", "Close"],
               width=2.0,
               subplots=True,
               xTitle="Date", 
               yTitle="Price ($)", 
               title="OHLC Price From September,2020 - September,2021"
              )

# ======================================================================
# Area Charts
#
# 
# The fourth chart type that we'll introduce is area charts. We can easily
# create an area chart using the same parameters as that of a line chart
# with only one change. We need to set the fill parameter to True in 
# order to create an area chart.
# ======================================================================

# Below we have created an area chart covering the area under the open
# price of Apple stock:
apple_df.iplot(y="Open",
               fill=True,
               xTitle="Date", 
               yTitle="Price ($)", 
               title="Open Price From September,2020 - September,2021",
              )

apple_df.iplot(
               keys=["Open", "High", "Low", "Close"],
               subplots=True,
               fill=True,
               xTitle="Date", 
               yTitle="Price ($)", 
               title="OHLC Price From Open Price From September,2020 - September,2021"
              )

# ======================================================================
# Pie Charts
# 
# The fifth chart type is pie charts. 
# ======================================================================

# We'll be creating a new dataframe from the wine dataframe which has 
# information about the count of samples per each wine category. We can 
# create this dataframe by grouping the original wine dataframe based on
# wine type and then calling the count() method on it to get a count of 
# samples per wine type:
wine_cnt = wine_df.groupby(by=["WineType"]).count()[["alcohol"]].rename(columns={"alcohol":"Count"}).reset_index()

print('wine_cnt:')
print(wine_cnt)
print()

print('wine_cnt.info():')
print(wine_cnt.info())
print()

# We can easily create a pie chart by calling iplot() method on the 
# dataframe passing it kind parameter as pie. We also need to pass which
# column to use for labels and which column to use for values. Below we
# have created a pie chart from the wine type count dataframe created in
# the previous cell. We have also modified how labels should be displayed
# by setting textinfo parameter.
wine_cnt.iplot(kind="pie",
               labels="WineType",
               values="Count",
               textinfo='percent+label', 
               hole=.4,
              )

# Below we have created the same pie chart as the previous step with two
# minor changes. We have removed the internal circle and we have pulled
# out the class_2 wine type patch a little bit out to highlight it. We
# need to pass the pull parameter list of floats which is the same size
# as labels and only one float should be greater than 0.
wine_cnt.reset_index().iplot(kind="pie",
                             labels="WineType",
                             values="Count",
                             textinfo='percent+label',
                             pull=[0, 0, 0.1],
                             )

# ======================================================================
# Histograms
# 
# The sixth chart type that we'll introduce is the histogram. We can easily
# create a histogram by setting the kind parameter to hist. We have passed
# the column name as the keys parameter in order to create a histogram 
# of that column.
# ======================================================================

wine_df.iplot(kind="hist",
              bins=50, 
              colors=["red"],
              keys=["alcohol"],
              #dimensions=(600, 400),
              title="Alcohol Histogram"
             )

# Below we have created another example of the histogram where we are 
# plotting a histogram of three quantities:
wine_df.iplot(kind="hist",
              bins=50, 
              colors=["red", "blue", "green", "black"],
              keys=["total_phenols", "flavanoids", "ash"],
              title="Ash, Total Phenols & Flavanoids Histogram"
             )
             
# ======================================================================
# Box Plots
# 
# The seventh chart type that we'll introduce is the box plots. We can 
# easily create a box plot from the pandas dataframe by setting the kind
# parameter to box in iplot() method. 
# ======================================================================

# We have below created a box plot of four quantities of iris flowers. 
# We have passed column names of four features of the iris flower to the
# keys parameter as a list.
iris_df.iplot(kind="box",
              keys=iris.feature_names, 
              boxpoints="outliers",
              xTitle="Flower Features", 
              title="IRIS Flower Features Box Plot"
             )

# ======================================================================
# Heatmaps
# 
# The eight chart type is heatmaps. 
# ======================================================================

# We'll first create a correlation dataframe for the wine dataset by 
# calling the corr() method on it.
wine_corr_df = wine_df.corr()

print('wine_corr_df:')
print(wine_corr_df)
print()

print('wine_corr_df.info():')
print(wine_corr_df.info())
print()

# Once we have the correlation dataframe ready, we can easily create a
# heatmap by calling iplot() method on it and passing the kind parameter
# value as heatmap. We have also provided colormap as Blues. We can also
# set chart dimensions by passing width and height as tuple to the 
# dimensions parameter.
wine_corr_df.iplot(kind="heatmap",
                   colorscale="Blues",
                   #dimensions=(900,900)
                  )

# Below we have created another heatmap of the iris flowers dataset
# showing a correlation between various features.
iris_df.corr().iplot(kind="heatmap",
                   colorscale="Reds",
                   #dimensions=(500,500)
                   )

# ======================================================================
# CandleStick & OHLC Charts
# 
# The ninth chart type that we'll introduce is the candlestick chart. We 
# can easily create a candlestick chart from the dataframe by calling 
# iplot() method on it and passing candle as value to the kind parameter.
# ======================================================================

# We also need to have Open, High, Low, and Close columns in the 
# dataframe in that order. Below we have created a candlestick chart of
# whole apple OHLC data.
apple_df.iplot(kind="candle", keys=["Open", "High", "Low", "Close"])

# Below we have created another example of a candlestick chart where we
# are plotting candles for only Apr-2021 data.

mask = (apple_df.index >= '2021-04-01') & (apple_df.index <= '2021-04-30')
test_date_df = apple_df.loc[mask]

print('test_date_df:')
print(test_date_df)
print()

print('test_date_df.info():')
print(test_date_df.info())
print()

test_date_df.iplot(kind="candle",
                   keys=["Open", "High", "Low", "Close"],
                  )

# We can create an OHLC chart exactly the same way as a candlestick chart
# with the only difference which is we need to set the kind parameter as
# ohlc.
test_date_df.iplot(kind="ohlc",
                   keys=["Open", "High", "Low", "Close"])

# ======================================================================
# Bubble Chart
# 
# The tenth chart type that we'll plot using cufflinks is a bubble chart.
# The bubble chart can be used to represent three dimensions of data. The 
# two-dimension are used to create a scatter plot and the third dimension 
# is used to decide the sizes of points in the scatter plot.
# ======================================================================

# Below we have created a bubble chart on the iris dataframe's first 50
# samples by setting the kind parameter to bubble. We have used sepal
# length and sepal width as x and y dimension and petal width as size
# dimension:
iris_df[:50].iplot(kind="bubble", 
                   x="sepal length (cm)", 
                   y="sepal width (cm)", 
                   size="petal width (cm)",
                   colors=["tomato"],
                   xTitle="Sepal Length (CM)", 
                   yTitle="Sepal Width (CM)",
                   title="Sepal Length vs Sepal Width Bubble Chart"
                  )

# ======================================================================
# 3D Bubble Chart
# 
# We can also create a 3D bubble chart that can be used to represent 4 
# dimensions of data. The first three dimensions of data will be used to 
# create a 3D scatter chart and 4th dimension will be used to decide the 
# size of the point (bubble) in a scatter plot.
# ======================================================================

# We are creating a 3D bubble chart by setting the kind parameter to 
# bubble3d in iplot() method. We have used sepal length, sepal width and 
# petal width to create a 3D scatter chart and petal length to decide the 
# sizes of points in a 3D scatter chart. We have also color encoded points 
# in scatter plot based on flower types.
iris_df.iplot(kind="bubble3d",
              x="sepal length (cm)", 
              y="sepal width (cm)", 
              z="petal width (cm)",
              size="petal length (cm)",
              colors=["dodgerblue", "lime", "tomato"], 
              categories="FlowerType",
              xTitle="Sepal Length (CM)", 
              yTitle="Sepal Width (CM)", 
              zTitle="Petal Width (CM)",
              title="Sepal Length vs Sepal Width vs Petal Width Bubble 3D Chart"
             )

# ======================================================================
# 3D Scatter Chart
# 
# We can create 3d scatter charts as well as using cufflinks. We need to 
# set kind parameter to scatter3d in iplot() method. 
# ======================================================================

# We are creating 3d scatter chart of sepal length, sepal width, and 
# petal width. We even have color encoded points in 3d scatter chart 
# according to flower type.
iris_df.iplot(kind="scatter3d",
              x="sepal length (cm)", 
              y="sepal width (cm)", 
              z="petal width (cm)",
              size=5,
              colors=["dodgerblue", "lime", "tomato"], 
              categories="FlowerType",
              xTitle="Sepal Length (CM)", 
              yTitle="Sepal Width (CM)", 
              zTitle="Petal Width (CM)",
              title="Sepal Length vs Sepal Width vs Petal Width Scatter Chart"
             )

# ======================================================================
# Spread Chart
# 
# The thirteenth chart type that we'll introduce is spread chart. 
# ======================================================================

# Below we are creating a spread chart of high and low prices by setting
# the kind parameter to spread.
apple_df.iplot(kind="spread", 
               keys=["High", "Low"],
               title="High and Low Price Spread Chart"
              )

# ======================================================================
# Ratio Chart
# 
# The fourteenth and last chart type that we'll introduce is the ratio 
# chart. We can create a ratio chart by setting the kind parameter to ratio.
# ======================================================================

# We are creating a ratio chart of open and close prices of apple 
# OHLC data.
apple_df.iplot(kind="ratio", 
               keys=["Open", "Close",],
               title="Open & Close Price Ratio Chart"
              )

# This concludes our small tutorial explaining how to use cufflinks to
# create plotly charts directly from the pandas dataframe.




