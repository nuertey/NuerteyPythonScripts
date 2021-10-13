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
from numpy import array
from nose.tools import assert_equal
from sklearn.datasets import load_iris, load_wine
from sklearn.preprocessing import MinMaxScaler

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
#figure_1.show()

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
#figure_2.show()

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
#figure_3.show()

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
# Visualizing Modern C++ Type Classification Heirarchyy:
# ======================================================================

print('# ========================================================')
print('# Modern C++ Type Classification Heirarchy:'               )
print('# ========================================================')
print()

object_labels = ["std::is_fundamental",           
                 "std::is_object", 
                 "std::is_compound", 
                 "std::is_void",
                 "std::is_arithmetic", 
                 "std::nullptr_t", 
                 "std::is_scalar",
                 "std::is_array", 
                 "std::is_union", 
                 "std::is_class",
                 "std::is_reference", 
                 "std::is_function", 
                 "std::is_floating_point",
                 "std::is_integral", 
                 "std::is_member_pointer", 
                 "std::is_member_object_pointer", 
                 "std::is_member_function_pointer", 
                 "std::is_pointer", 
                 "std::is_enum",
                 "std::is_lvalue_reference", 
                 "std::is_rvalue_reference", 
                 "float",
                 "double", 
                 "long double",
                 "bool",
                 "char", 
                 "signed char",     
                 "unsigned char",
                 "wchar_t", 
                 "char8_t (C++20)",
                 "char16_t (C++11)",
                 "char32_t (C++11)", 
                 "short",
                 "unsigned short",
                 "int", 
                 "unsigned int",
                 "long",
                 "unsigned long", 
                 "long long (C++11)",
                 "unsigned long long (C++11)"]
                  
object_parents = ["", 
                  "", 
                  "", 
                  "std::is_fundamental", 
                  "std::is_fundamental", 
                  "std::is_fundamental", 
                  "std::is_object", 
                  "std::is_object", 
                  "std::is_object", 
                  "std::is_object", 
                  "std::is_compound", 
                  "std::is_compound", 
                  "std::is_arithmetic", 
                  "std::is_arithmetic", 
                  "std::is_scalar", 
                  "std::is_member_pointer", 
                  "std::is_member_pointer", 
                  "std::is_scalar", 
                  "std::is_scalar", 
                  "std::is_reference", 
                  "std::is_reference", 
                  "std::is_floating_point", 
                  "std::is_floating_point", 
                  "std::is_floating_point",
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral", 
                  "std::is_integral",
                  "std::is_integral"]

# The weights also seem to determine the hierarchy level:
object_weights = [10, 
                  10, 
                  10, 
                   8, 
                   8, 
                   8, 
                   9, 
                   5, 
                   5, 
                   5, 
                   7, 
                   9, 
                   6, 
                   6, 
                   7, 
                   6, 
                   6, 
                   6, 
                   5,
                   4, 
                   4, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2, 
                   2,
                   2]

assert_equal(len(object_labels), len(object_parents))
assert_equal(len(object_labels), len(object_weights))

data = dict(
    ClassObject=object_labels,
    ParentObject=object_parents,
    WeightValue=object_weights)

figure_4_2 = px.sunburst(
    data,
    names='ClassObject',
    parents='ParentObject',
    values='WeightValue',
    #color='WeightValue',
)
figure_4_2.show()

# ======================================================================
# Visualizing Nuertey Odzeyem's Solution to Markem Imajem Design Exercise
# Heirarchy:
# ======================================================================

print('# ========================================================')
print('# Markem Imajem Design Exercise Heirarchy:'                )
print('# ========================================================')
print()

object_labels = ["TemperatureReadoutApplication",           
                 "Utility::",
                 "SessionManager", 
                 "Common::",
                 "asio::executor_work_guard",
                 "asio::io_context", 
                 "std::thread", 
                 "SensorNode_t", 
                 "std::string",
                 "std::unique_ptr<tcp::socket>", 
                 "TcpData_t",
                 "std::array<char, M>", 
                 "m_CurrentTemperatureReading",
                 "SystemClock_t::time_point", 
                 "std::enable_shared_from_this<SessionManager>", 
                 "SensorPack_t", 
                 "std::array<SensorNode_t, N>", 
                 "std::mutex", 
                 "SystemClock_t::time_point", 
                 "tcp::resolver",
                 "tcp::resolver::query", 
                 "tcp::v4()", 
                 "tcp::resolver::iterator",
                 "tcp::resolver::iterator()",
                 "tcp::endpoint",
                 "CustomerDisplay", 
                 "asio::buffer",
                 "std::error_code",
                 "asio::post()", 
                 "SystemClock_t::now()",     
                 "Seconds_t(MINIMUM_DISPLAY_INTERVAL_SECONDS)",
                 "Minutes_t(STALE_READING_DURATION_MINUTES)", 
                 "averageTemperature",
                 "TestArtifactSensorNode",
                 "SensorNodeServer",
                 "asio::io_context", 
                 "tcp::acceptor",
                 "tcp::endpoint",
                 "tcp::v4()",
                 "tcp::socket",
                 "std::error_code", 
                 "TCPSession",
                 "std::enable_shared_from_this<TCPSession>",
                 "tcp::socket", 
                 "gs_theRNG.uniform(-50.00, 50.00)",
                 "asio::write()",
                 "std::to_string(randomTemperatureReading)",
                 "asio::buffer",
                 "gs_theRNG.pick({SENSOR_PERIODIC_MODE, SENSOR_RANDOM_CHANGE})",
                 "gs_theRNG.uniform(SENSOR_RANDOM_CHANGE_MIN_SECONDS, SENSOR_RANDOM_CHANGE_MAX_SECONDS - 1)",
                 "Seconds_t(holdoffTime)",
                 "std::this_thread::sleep_for()",
                 "SensorMode_t",
                 "static thread_local randutils::mt19937_rng gs_theRNG"]
                  
object_parents = ["", 
                  "TemperatureReadoutApplication", 
                  "TemperatureReadoutApplication", 
                  "SessionManager",
                  "Common::", 
                  "Common::", 
                  "Common::", 
                  "SensorPack_t", 
                  "SensorNode_t", 
                  "SensorNode_t", 
                  "SensorNode_t", 
                  "TcpData_t", 
                  "SensorNode_t", 
                  "SensorNode_t", 
                  "SessionManager", 
                  "SessionManager", 
                  "SensorPack_t", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager",
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "SessionManager", 
                  "",
                  "TestArtifactSensorNode", 
                  "TestArtifactSensorNode", 
                  "SensorNodeServer", 
                  "SensorNodeServer", 
                  "SensorNodeServer", 
                  "SensorNodeServer", 
                  "SensorNodeServer", 
                  "SensorNodeServer", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession", 
                  "TCPSession",
                  "TCPSession",
                  "Utility::"]

# The weights also seem to determine the hierarchy level:
object_weights = [10, 
                   9, 
                   8, 
                   7, 
                   5, 
                   5, 
                   5, 
                   5, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   6, 
                   6, 
                   5, 
                   6, 
                   6,
                   5, 
                   5, 
                   5, 
                   5, 
                   5, 
                   5, 
                   6, 
                   5, 
                   5, 
                   5, 
                   4, 
                   4, 
                   4, 
                   6, 
                  10, 
                   8, 
                   8, 
                   6, 
                   6, 
                   6, 
                   6, 
                   6, 
                   6, 
                   7, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4, 
                   4,
                   7]

assert_equal(len(object_labels), len(object_parents))
assert_equal(len(object_labels), len(object_weights))

data = dict(
    ClassObject=object_labels,
    ParentObject=object_parents,
    WeightValue=object_weights)

figure_4_3 = px.sunburst(
    data,
    names='ClassObject',
    parents='ParentObject',
    values='WeightValue',
    #color='WeightValue',
)
figure_4_3.show()

# ======================================================================
# Example 4: Other Plotly Plot Types, Bubble Chart.
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
#figure_5.show()

# ======================================================================
# Example 5: Other Plotly Plot Types, Radar Chart.
# ======================================================================

print('# =================')
print('# Example 5:       ')
print('# =================')
print()

# The radar chart is a technique to display multivariate data on the 
# two-dimensional plot where three or more quantitative variables are 
# represented by axes starting from the same point. The relative position
# and angle of lines are of no importance. Each observation is represented
# by a single point on all axes. All points representing each quantitative
# variable is connected in order to generate a polygon. All quantitative
# variables of data are scaled to the same level for comparison. We can
# look at the single observation of data to look at how each quantitative
# variable representing that samples are laid out on the chart.
 
# The radar chart can be useful in identifying and comparing the behavior
# of observations. We can identify which observations are similar as well
# as outliers. The radar charts can be used at various places like sports
# to compare player performance, employee performance comparison, comparison
# of various programs based on different attributes, etc.

# The radar chart is also commonly referred to as a web chart, spider chart,
# spider web chart, star chart, star plot, cobweb chart, polar chart, etc.

# Radar charts also have limitations which are worth pointing out. If there
# be many observations to be displayed then radar charts become crowded.
# As more polygons are layered on top of each other, distinguishing 
# observations becomes difficult. Each axis of the radar chart has the
# same scale which means that we need to scale data and bring all columns
# to the same scale. The alternative charts to avoid pitfalls of radar
# charts are parallel coordinate charts and bar charts.

# The parallel coordinates chart is almost the same chart as the radar chart
# excepting that it lays out quantitative variables in parallel vertically
# unlike the radar chart which lays them out radially. 

# IRIS Flowers Dataset: It has dimensions measured for 3 different IRIS 
# flower types.
iris = load_iris()

# Scale data so that each column’s data gets into the range [0-1]. Once
# data is such a range for all quantitative variables, it becomes
# straightforward to observe their inter-dependencies.
iris_data = MinMaxScaler().fit_transform(iris.data)
iris_data = np.hstack((iris_data, iris.target.reshape(-1,1)))

# In the process of creating the DataFrame, ensure to create a "FlowerType"
# last column:
iris_df = pd.DataFrame(data=iris_data, columns=iris.feature_names + ["FlowerType"])

print('iris_df.shape:')
print(iris_df.shape)
print()

print('iris_df:')
print(iris_df)
print()

print('iris_df.info():')
print(iris_df.info())
print()

# Group by flower type and then take mean of each column. This will give
# us the average value of each data dimension for each flower type.
avg_iris = iris_df.groupby("FlowerType").mean()

print('avg_iris:')
print(avg_iris)
print()

figure_6 = px.line_polar(
                    r=avg_iris.loc[0].values, # Flower type 0.0
                    theta=avg_iris.columns,   # variables
                    line_close=True,   # connect end variables to create a polygon
                    range_r = [0,1.0], # As all variables have been scaled between 0-1 earlier.
                    title="IRIS - %s"%iris.target_names[0])
#figure_6.show()

# Below we are using same line_polar() function to plot radar chart for
# IRIS Versicolor flower type. We can also later update chart attributes
# by using the update_traces() method. We are filling radar chart polygon
# this time by setting fill attribute value to toself. We can also change
# the direction of quantitative variables layout by setting the direction
# attribute to counterclockwise. We can also set the start angle from 
# where we want to start plotting quantitative variables by setting the
# start_angle attribute. The default for start_angle is 90.
figure_7 = px.line_polar(
                    r=avg_iris.loc[1].values, # Flower type 1.0
                    theta=avg_iris.columns,
                    line_close=True,
                    range_r = [0,1.0],
                    title="IRIS - %s"%iris.target_names[1],
                    direction="counterclockwise", start_angle=45
                    )

figure_7.update_traces(fill='toself')
#figure_7.show()

# ----------------------------------------------------------------------
# Wine Dataset: It has information about various ingredients of wine such 
# as alcohol, malic acid, ash, magnesium, etc. for three different wine
# categories.
wine = load_wine()

# Scale data so that each column’s data gets into the range [0-1]. Once
# data is such a range for all quantitative variables, it becomes
# straightforward to observe their inter-dependencies.
wine_data = MinMaxScaler().fit_transform(wine.data)
wine_data = np.hstack((wine_data, wine.target.reshape(-1,1)))

# In the process of creating the DataFrame, ensure to a "WineCat" last
# column:
wine_df = pd.DataFrame(data=wine_data, columns=wine.feature_names + ["WineCat"])

print('wine_df.shape:')
print(wine_df.shape)
print()

print('wine_df:')
print(wine_df)
print()

print('wine_df.info():')
print(wine_df.info())
print()

# We have grouped the wine dataset by wine categories and have then taken
# the mean of each column. This will give us the average value of each 
# data dimension for each wine category that we'll use to plot radar 
# charts. We can take an individual samples and create a radar chart from
# it as well but here we'll be creating a radar chart of the average of 
# each category so that we'll get an idea about each category as a whole.
avg_wine = wine_df.groupby("WineCat").mean()

print('avg_wine:')
print(avg_wine)
print()

# Below we have plotted the radar chart for Wine of class 0. The wine 
# dataset has 13 variables to compare:
figure_8 = px.line_polar(
                    r=avg_wine.loc[0].values, # Wine category 0.0
                    theta=avg_wine.columns,
                    line_close=True,
                    range_r = [0,1.0],
                    title="WINE - %s"%wine.target_names[0]
                    )

figure_8.update_traces(fill='toself')
#figure_8.show()

figure_9 = px.line_polar(
                    r=avg_wine.loc[1].values, # Wine category 1.0
                    theta=avg_wine.columns,
                    line_close=True,
                    title="WINE - %s"%wine.target_names[1],
                    range_r = [0,1.0]
                    )

figure_9.update_traces(fill='toself')
#figure_9.show()

# We can see from the above two figures that alcohol is more in wine 
# category 0 compared to wine category 1. The ash is also more in wine
# category 0 compared to wine category 1. We can compare all different 
# quantitative variables this way.

# ======================================================================
# The second method provided by plotly is Scatterpolar available as a part
# of the graph_objects module of plotly. It has almost the same parameter
# requirement as that of line_polar() for creating radar charts. It expects
# that we provide parameter r and theta for generating radar charts. We 
# can specify fill color, line color, fill, etc attributes by passing 
# them directly to this method.

# Below we are using Scatterpolar to generate radar chart for IRIS flower
# type verginica:
figure_10 = go.Figure()
figure_10.add_trace(
                go.Scatterpolar(
                                r=avg_iris.loc[2].values, # Flower type 2.0
                                theta=avg_iris.columns,
                                fill='toself',
                                name="IRIS-%s"%iris.target_names[2],
                                fillcolor="orange", opacity=0.6, line=dict(color="orange")
                                )
                )

figure_10.update_layout(
    polar=dict(
        radialaxis=dict(
          visible=True
        ),
      ),
    showlegend=False,
    title="IRIS-%s"%iris.target_names[2]
)

#figure_10.show()

# Combining polygon for all 3 different iris flower types in a single 
# radar chart. We are not filling color in the radar chart. We also have
# repeated first value 2 times in our logic in order to join ends of
# polygons of a radar chart.
figure_11 = go.Figure()

for i in range(3): # 0, 1, 2
    figure_11.add_trace(
            go.Scatterpolar(
                            r=avg_iris.loc[i].values.tolist() + avg_iris.loc[i].values.tolist()[:1],
                            theta=avg_iris.columns.tolist() + avg_iris.columns.tolist()[:1],
                            name="IRIS-%s"%iris.target_names[i],
                            showlegend=True,
                            )
            )

figure_11.update_layout(
    polar=dict(
        radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
            ),

    title="IRIS Flower Variables According to Flower Categories"
)

#figure_11.show()
# We can easily compare quantitative variables of different flower types
# easily now. We can see that iris setosa has on an average more sepal
# width compared to the other two. Iris versicolor is smaller in size
# compared to iris virginica. Iris virginica has the biggest petal length,
# petal width, and sepal length compared to the other two.

# Below we are again plotting three different iris flowers with their
# polygon filled in this time:
figure_12 = go.Figure()

colors = ["tomato", "dodgerblue", "yellow"]
for i in range(3):
    figure_12.add_trace(
                go.Scatterpolar(
                                r=avg_iris.loc[i].values.tolist() + avg_iris.loc[i].values.tolist()[:1],
                                theta=avg_iris.columns.tolist() + avg_iris.columns.tolist()[:1],
                                fill='toself',
                                name="IRIS-%s"%iris.target_names[i],
                                fillcolor=colors[i], line=dict(color=colors[i]),
                                showlegend=True, opacity=0.6
                                )
                )

figure_12.update_layout(
    polar=dict(
        radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
            ),
    title="IRIS Flower Variables According to Flower Categories"
)

#figure_12.show()

# Below we are plotting three different wine types on a single radar 
# chart. We can easily compare different quantitative variables across
# different wine types now.
figure_13 = go.Figure()

for i in range(3):
    figure_13.add_trace(
                go.Scatterpolar(
                                r=avg_wine.loc[i].values,
                                theta=avg_wine.columns,
                                fill='toself',
                                name="WINE-%s"%wine.target_names[i],
                                showlegend=True,
                                )
                )

figure_13.update_layout(
    polar=dict(
        radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
            ),
    title="Wine Variables According to Wine Categories"
)

#figure_13.show()
# We can notice from the above chart that wine class 0 has the highest
# amount of alcohol. Wine class 0 also has more proline, magnesium,
# phenols, flavonoids, proanthocyanins, and od280/od315 compared to the
# other two wine types. Wine class 2 has more malic acid, the alkalinity
# of ash, non-flavonoid phenols, and color intensity compared to the
# other two wine types.
