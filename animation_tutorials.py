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
# Several Plotly Express functions support the creation of animated 
# figures through the animation_frame and animation_group arguments.
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

# animation_frame 
#
# (str or int or Series or array-like) – Either a name of 
# a column in data_frame, or a pandas Series or array_like object. Values 
# from this column or array_like are used to assign marks to animation 
# frames.

# animation_group 
#
# (str or int or Series or array-like) – Either a name of a column in 
# data_frame, or a pandas Series or array_like object. Values from this 
# column or array_like are used to provide object-constancy across 
# animation frames: rows with matching `animation_group`s will be treated
# as if they describe the same object in each frame.
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
# Animated Bar Charts with Plotly Express
# ======================================================================
gap_minder_df = px.data.gapminder()

# Note that you should always fix the y_range to ensure that your data
# remains visible throughout the animation.
min_y = int(round(min(gap_minder_df["pop"])))# - 4
max_y = int(round(max(gap_minder_df["pop"])))# + 7

print('min_y')
print(min_y)
print()

print('max_y:')
print(max_y)
print()

figure_2 = px.bar(gap_minder_df, 
                  x="continent", 
                  y="pop", 
                  color="continent",
                  animation_frame="year", 
                  animation_group="country", 
                  range_y=[0, 4000000000])
figure_2.show()

# ======================================================================
# Moving Point on a Curve
# ======================================================================

# Generate curve data
t = np.linspace(-1, 1, 100)
x = t + t ** 2
y = t - t ** 2
xm = np.min(x) - 1.5
xM = np.max(x) + 1.5
ym = np.min(y) - 1.5
yM = np.max(y) + 1.5
N = 50
s = np.linspace(-1, 1, N)
xx = s + s ** 2
yy = s - s ** 2

# Create figure
figure_3 = go.Figure(
    data=[go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue")),
          go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue"))],
    layout=go.Layout(
        xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
        yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
        title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None])])]),
    frames=[go.Frame(
        data=[go.Scatter(
            x=[xx[k]],
            y=[yy[k]],
            mode="markers",
            marker=dict(color="red", size=10))])

        for k in range(N)]
)

figure_3.show()

# ======================================================================
# Moving Frenet Frame Along a Planar Curve
# ======================================================================

# Generate curve data
t = np.linspace(-1, 1, 100)
x = t + t ** 2
y = t - t ** 2
xm = np.min(x) - 1.5
xM = np.max(x) + 1.5
ym = np.min(y) - 1.5
yM = np.max(y) + 1.5
N = 50
s = np.linspace(-1, 1, N)
xx = s + s ** 2
yy = s - s ** 2
vx = 1 + 2 * s
vy = 1 - 2 * s  # v=(vx, vy) is the velocity
speed = np.sqrt(vx ** 2 + vy ** 2)
ux = vx / speed  # (ux, uy) unit tangent vector, (-uy, ux) unit normal vector
uy = vy / speed

xend = xx + ux  # end coordinates for the unit tangent vector at (xx, yy)
yend = yy + uy

xnoe = xx - uy  # end coordinates for the unit normal vector at (xx,yy)
ynoe = yy + ux

# Create figure
figure_4 = go.Figure(
    data=[go.Scatter(x=x, y=y,
                     name="frame",
                     mode="lines",
                     line=dict(width=2, color="blue")),
          go.Scatter(x=x, y=y,
                     name="curve",
                     mode="lines",
                     line=dict(width=2, color="blue"))
          ],
    layout=go.Layout(width=600, height=600,
                     xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
                     yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
                     title="Moving Frenet Frame Along a Planar Curve",
                     hovermode="closest",
                     updatemenus=[dict(type="buttons",
                                       buttons=[dict(label="Play",
                                                     method="animate",
                                                     args=[None])])]),

    frames=[go.Frame(
        data=[go.Scatter(
            x=[xx[k], xend[k], None, xx[k], xnoe[k]],
            y=[yy[k], yend[k], None, yy[k], ynoe[k]],
            mode="lines",
            line=dict(color="red", width=2))
        ]) for k in range(N)]
)

figure_4.show()

# ======================================================================
# Using a Slider and Buttons
# ======================================================================

# The following example uses the well known Gapminder dataset to exemplify
# animation capabilities. This bubble chart animation shows the change
# in 'GDP per Capita' against the 'Life Expectancy' of several countries
# from the year 1952 to 2007, colored by their respective continent and
# sized by population.
#
# This is also an example of building up the structure of a figure as a
# Python dictionary, and then constructing a graph object figure from
# that dictionary.
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
dataset = pd.read_csv(url)

years = ["1952", "1962", "1967", "1972", "1977", "1982", "1987", "1992",
         "1997", "2002", "2007"]

# make list of continents
continents = []
for continent in dataset["continent"]:
    if continent not in continents:
        continents.append(continent)

# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data
year = 1952
for continent in continents:
    dataset_by_year = dataset[dataset["year"] == year]
    dataset_by_year_and_cont = dataset_by_year[
        dataset_by_year["continent"] == continent]

    data_dict = {
        "x": list(dataset_by_year_and_cont["lifeExp"]),
        "y": list(dataset_by_year_and_cont["gdpPercap"]),
        "mode": "markers",
        "text": list(dataset_by_year_and_cont["country"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 200000,
            "size": list(dataset_by_year_and_cont["pop"])
        },
        "name": continent
    }
    fig_dict["data"].append(data_dict)

# make frames
for year in years:
    frame = {"data": [], "name": str(year)}
    for continent in continents:
        dataset_by_year = dataset[dataset["year"] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont["lifeExp"]),
            "y": list(dataset_by_year_and_cont["gdpPercap"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["country"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_year_and_cont["pop"])
            },
            "name": continent
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]

figure_5 = go.Figure(fig_dict)

figure_5.show()

# ======================================================================
# Important Notes
# 
#  Defining redraw: Setting redraw: false is an optimization for scatter
#  plots so that animate just makes changes without redrawing the whole
#  plot. For other plot types, such as contour plots, every frame must 
#  be a total plot redraw, i.e. redraw: true.
# ======================================================================


# ======================================================================



