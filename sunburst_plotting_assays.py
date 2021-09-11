#***********************************************************************
# @file
#
# Advancing on plotly sunburst plots by assaying some. 
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
# Example 1:
# ======================================================================

print('# =================')
print('# Example 1:       ')
print('# =================')
print()

# With px.sunburst, each row of the DataFrame is represented as a sector
# of the sunburst. Furthermore, the sunburst plot requires weights (values),
# labels, and parent. Here we compose with a dictionary:
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"], # Labels.
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4]) # Weights.

figure_1 = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)

figure_1.show()

# ======================================================================
# Example 2:
# ======================================================================

print('# =================')
print('# Example 2:       ')
print('# =================')
print()

# Sunburst of a rectangular DataFrame with plotly.express
# 
# Hierarchical data are often stored as a rectangular dataframe, with 
# different columns corresponding to different levels of the hierarchy.
# px.sunburst can take a path parameter corresponding to a list of columns.
# Note that id and parent should not be provided if path is given.
df = px.data.tips()

print('df.shape:')
print(df.shape)
print()

print('df = px.data.tips():')
print(df)
print()

print('df.info():')
print(df.info())
print()

# path = parent, children, grandchildren, ...
# values = the column that would determine weights or (pizza) slice widths of segments.
#
# And the implication in this case is that the aggregation and groupby
# operations to determine the 'pizza slices' are internally and automagically
# performed by plotly itself.
figure_2 = px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
figure_2.show()

# ======================================================================
# Example 3:
# ======================================================================

print('# =================')
print('# Example 3:       ')
print('# =================')
print()

# Sunburst of a rectangular DataFrame with continuous color argument in
# px.sunburst
#
# If a color argument is passed, the color of a node is computed as the
# average of the color values of its children, weighted by their values.
df = px.data.gapminder().query("year == 2007")

print('df.shape:')
print(df.shape)
print()

print('df = px.data.gapminder().query(\"year == 2007\"):')
print(df)
print()

print('df.info():')
print(df.info())
print()

figure_3 = px.sunburst(df, 
                       path=['continent', 'country'], 
                       values='pop',
                       color='lifeExp', 
                       hover_data=['iso_alpha'],
                       color_continuous_scale='RdBu',
                       color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop'])
                      )
figure_3.show()

# ======================================================================
# Visualizing Nuertey Odzeyem's SharedInputNotifier OS Abstraction Heirarchy:
# ======================================================================

print('# ========================================================')
print('# Nuertey\'s SharedInputNotifier OS Abstraction Heirarchy:')
print('# ========================================================')
print()

object_labels = ["SharedInputNotifier", "eDevice", "eDeviceHandler", 
                 "ReadableDevice", "WriteableDevice", "eSocket", 
                 "ClientSocket", "ServerSocket", "CANSocket", "eTimer",
                 "GenericSharedMemory", "I2CDevice", "InputGPIODevice",
                 "OutputGPIODevice","InputOutputGPIODevice", "MessageQueue",
                  "SPIDevice", "TermDevice", "USBHotplugDevice", "GPIODeviceHandler",
                  "LostHeartBeatTimerHandler", "EPOLL_NOTIFICATION_MODE",
                  "LEVEL_TRIGGERED", "EDGE_TRIGGERED"]
                  
object_parents = ["", "SharedInputNotifier", "SharedInputNotifier", 
                  "eDevice", "eDevice", "WriteableDevice", "eSocket", 
                  "eSocket", "WriteableDevice", "ReadableDevice", 
                  "WriteableDevice", "WriteableDevice", "ReadableDevice", 
                  "WriteableDevice", "WriteableDevice", "WriteableDevice", 
                  "WriteableDevice", "WriteableDevice", "ReadableDevice",
                  "eDeviceHandler", "eDeviceHandler", "eDevice", 
                  "EPOLL_NOTIFICATION_MODE", "EPOLL_NOTIFICATION_MODE"]

# The weights also seem to determine the hierarchy level:
object_weights = [10, 6, 6, 
                  5, 5, 4, 
                  3, 3, 3, 3, 
                  3, 3, 3, 
                  3, 3, 3, 
                  3, 3, 3,
                  3, 3, 2, 
                  1, 1]

assert_equal(len(object_labels), len(object_parents))
assert_equal(len(object_labels), len(object_weights))

data = dict(
    ClassObject=object_labels,
    ParentObject=object_parents,
    WeightValue=object_weights)

figure_4 = px.sunburst(
    data,
    names='ClassObject',
    parents='ParentObject',
    values='WeightValue',
    #color='WeightValue',
)

figure_4.show()

# ======================================================================
# Example 4: Other Plotly Plot Types
# ======================================================================

print('# =================')
print('# Example 4:       ')
print('# =================')
print()

# Bubble chart with plotly.express
# 
# A bubble chart is a scatter plot in which a third dimension of the data
# is shown through the size of markers. For other types of scatter plot,
# see the scatter plot documentation.
# 
# We first show a bubble chart example using Plotly Express. Plotly Express
# is the easy-to-use, high-level interface to Plotly, which operates on a
# variety of types of data and produces easy-to-style figures. The size of
# markers is set from the dataframe column given as the size parameter.
df = px.data.gapminder()

print('df.shape:')
print(df.shape)
print()

print('df = px.data.gapminder():')
print(df)
print()

print('df.info():')
print(df.info())
print()

figure_5 = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
                      size="pop", color="continent", hover_name="country", 
                      log_x=True, size_max=60)
figure_5.show()
