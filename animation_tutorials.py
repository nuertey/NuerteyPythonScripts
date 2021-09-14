#***********************************************************************
# @file
#
# Animation Tutorials.
#
# @note 
#
# @warning  None
#
#  Created: September 13, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import bqplot
from bqplot import pyplot as plt
import ipywidgets as widgets
import ipyvolume as ipv

import plotly
import plotly.graph_objects as go
import plotly.express as px

import time

from datetime import datetime
from dateutil.relativedelta import relativedelta
from numpy import array
from matplotlib.pyplot import *
from nose.tools import assert_equal
from sklearn.datasets import load_iris, load_wine
from sklearn.preprocessing import MinMaxScaler
from ipyvolume.widgets import quickvolshow

#setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

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

#print('cufflinks.__version__:')
#print(cf.__version__)
#print()

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
# pd.set_option("display.max_columns", 50)

# ======================================================================
# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may
# depend on the context. This is sometimes called chained assignment and
# should be avoided. See Returning a View versus Copy. [dataframe_loop_example.py]
pd.options.mode.chained_assignment = None


# ======================================================================
# Animated Figures With Plotly Express
# 
# Several Plotly Express functions support the creation of animated figures
# through the animation_frame and animation_group arguments.
# ======================================================================

# Here is an example of an animated scatter plot creating using Plotly 
# Express:
gap_minder_df = px.data.gapminder()

print('gap_minder_df:')
print(gap_minder_df)
print()

print('gap_minder_df.info():')
print(gap_minder_df.info())
print()

# Note that you should always fix the x_range and y_range to ensure that 
# your data remains visible throughout the animation.
min_x = int(round(min(gap_minder_df["gdpPercap"]))) - 11
max_x = int(round(max(gap_minder_df["gdpPercap"]))) + 7

min_y = int(round(min(gap_minder_df["lifeExp"]))) - 4
max_y = int(round(max(gap_minder_df["lifeExp"]))) + 7

print('min_x')
print(min_x)
print()

print('max_x')
print(max_x)
print()

print('min_y')
print(min_y)
print()

print('max_y:')
print(max_y)
print()

figure_1 = px.scatter(gap_minder_df, 
           x="gdpPercap", 
           y="lifeExp", 
           animation_frame="year", 
           animation_group="country",
           size="pop", 
           color="continent", 
           hover_name="country",
           log_x=True, 
           size_max=55, 
           range_x=[min_x, max_x], 
           range_y=[min_y, max_y])
figure_1.show()

# ======================================================================
# We'll now explain simple 2d animations with few examples. All of our 
# examples consist of below mentioned common steps:
#
#    Create bqplot Chart
#    Create ipywidgets Button
#    Create callback function for the button which will update chart data
#    Register callback with button using on_click()
#    Create UI combining button and bqplot figure using ipywidgets layout 
#    options.
# ======================================================================
#plt.figure(1, title='Line Chart')
#np.random.seed(0)
#n = 200
#x = np.linspace(0.0, 10.0, n)
#y = np.cumsum(np.random.randn(n))
#plt.plot(x, y)
#plt.show()
#
## The following example does not work and nothing shown in the notebook
## after this code snippet:
#x, y, z = np.random.random((3, 10000))
#ipv.quickscatter(x, y, z, size=1, marker="sphere")
#ipv.show()
#
## Same result as above for the following code:
#x, y, z, u, v = ipv.examples.klein_bottle(draw=False)
#ipv.figure()
#m = ipv.plot_mesh(x, y, z, wireframe=False)
#ipv.squarelim()
#ipv.show()
#
## Only controls shown but no figures after running the following code:
#ds = ipv.datasets.aquariusA2.fetch()
#ipv.quickvolshow(ds.data, lighting=True)
#
## ======================================================================
## Example 1
##
## Our first example consists of simple animation based on a scatter plot
## in bqplot. We'll be creating a simple scatter plot consisting of 100 
## random points. We have used bqplot's pyplot API to create a scatter 
## chart of 100 random points below.
## ======================================================================
#
### Chart Creation Logic
#colors= ["red", "green", "blue", "orangered", "tomato", "lawngreen", 
#         "lime", "pink", "gray", "black"]
#
#figure_1 = plt.figure(animation_duration=1000, 
#                       title="Random Data Scatter Chart")
#figure_1.layout.width="700px"
#figure_1.layout.height="500px"
#
#x = np.random.rand(100)
#y = np.random.rand(100)
#scatter_1 = plt.scatter(x,y)
#
#plt.xlabel("X")
#plt.ylabel("Y")
#
#plt.xlim(0,1)
#plt.ylim(0,1);
#
## And here, a simple ipywidgets button:
#button_one = widgets.Button(description="Start", icon="play")
#
## Below we have created a callback function which will be called each time
## a button is clicked. In the logic of the callback function, we are 
## looping 10 times, generating 100 new random points, and updating chart
## data with this new 100 points. We then stop for 1 second before 
## proceeding with the next iteration. This loop of 10 iterations with a 
## pause of 1 second between each iteration will give us simple animation.
##
## Note that we are updating scatter data using the hold_sync() context 
## of the scatter chart. The main reason for this is that it'll update 
## data at the same time synchronously.
#
### Callback to Update Chart
#def update_scatter_chart(btn):
#    for i in range(10):
#        x = np.random.rand(100)
#        y = np.random.rand(100)
#        idx = np.random.choice(np.arange(len(colors)))
#        with scat.hold_sync():
#            scatter_1.x = x
#            scatter_1.y = y
#            scatter_1.colors = [colors[idx]]
#        time.sleep(1)
#
#button_one.on_click(update_scatter_chart)
#
## Below we have combined button and scatter chart figure into one UI 
## using ipywidgets VBox() layout which will layout widgets passed to it
## vertically. We can click the button and it'll start the animation by
## calling the callback function.
#
### UI Combining Button & Chart
#widgets.VBox([button_one, figure_1])
#
#plt.show()
#
## ======================================================================
#wine  = load_wine()
#
#print("Dataset Features : ", wine.feature_names)
#print("Dataset Size : ", wine.data.shape)
#
#wine_df = pd.DataFrame(data=wine.data, columns=wine.feature_names)
#wine_df["Category"] = wine.target
#
#wine_df.head()
#
#fig = plt.figure(title="Alcohol vs Malic Acid Relation")
#
#scat = plt.scatter(x=wine_df["alcohol"], y=wine_df["malic_acid"])
#
#plt.xlabel("Alcohol")
#plt.ylabel("Malic Acid")
#
#plt.show()
