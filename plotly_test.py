# Offline features (plotly.offline) replaced by Renderers framework & HTML
# export
# 
# Version 4 introduces a new renderers framework that is a generalization 
# of version 3's plotly.offline.init_notebook_mode and plotly.offline.iplot
# functions for displaying figures. This is a non-breaking change: the 
# plotly.offline.iplot function is still available and has been reimplemented
# on top of the renderers framework, so no changes are required when porting 
# to version 4. Going forward, we recommend using the renderers framework 
# directly. See Displaying plotly figures for more information.
# 
# In version 3, the plotly.offline.plot function was used to export figures 
# to HTML files. In version 4, this function has been reimplemented on top 
# of the new to_html and write_html functions from the plotly.io module. 
# These functions have a slightly more consistent API (see docstrings for 
# details), and going forward we recommend using them directly when 
# performing HTML export. When working with a graph object figure, these 
# functions are also available as the .to_html and .write_html figure methods.
# 
# New default theme
# 
# An updated "plotly" theme has been enabled by default in version 4.
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Make figure with subplots
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"},
                                            {"type": "surface"}]])

# Add bar traces to subplot (1, 1)
fig.add_trace(go.Bar(y=[2, 1, 3]), row=1, col=1)
fig.add_trace(go.Bar(y=[3, 2, 1]), row=1, col=1)
fig.add_trace(go.Bar(y=[2.5, 2.5, 3.5]), row=1, col=1)

# Read data from a csv
z_data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv")

# Add surface trace to subplot (1, 2)
fig.add_surface(z=z_data)

# Hide legend
fig.update_layout(
    showlegend=False,
    title_text="Default Theme",
    height=500,
    width=800,
)

fig.show()

# Add trace return value
# 
# In version 3, the add_trace graph object figure method returned a reference
# to the newly created trace. This was also the case for the add_{trace_type}
# methods (e.g. add_scatter, add_bar, etc.). In version 4, these methods 
# return a reference to the calling figure. This change was made to support
# method chaining of figure operations. For example:
(make_subplots(rows=1, cols=2)
 .add_scatter(y=[2, 1, 3], row=1, col=1)
 .add_bar(y=[3, 2, 1], row=1, col=2)
 .update_layout(
     title_text="Figure title",
     showlegend=False,
     width=800,
     height=500,
 )
 .show())

# Code that relied on the add_* methods to return a reference to the newly 
# created trace will need to be updated to access the trace from the returned 
# figure. This can be done by appending .data[-1] to the add trace expression.
# 
# Here is an example of a version 3 code snippet that adds a scatter trace 
# to a figure, assigns the result to a variable named scatter, and then 
# modifies the marker size of the scatter trace.
#fig = go.Figure()
#scatter = fig.add_trace(go.Scatter(y=[2, 3, 1]))
#scatter.marker.size = 20

# In version 4, this would be replaced with the following:
figure1 = go.Figure()
scatter = figure1.add_trace(go.Scatter(y=[2, 3, 1])).data[-1]
scatter.marker.size = 20
figure1.show()

# make_subplots updates
# 
# The make_subplots function has been overhauled to support all trace types 
# and to support the integration of Plotly Express. Here are a few changes 
# to be aware of when porting code that uses make_subplots to version 4.
# New preferred import location
# 
# The preferred import location of the make_subplots function is now 
# plotly.subplots.make_subplots. For compatibility, this function is still 
# available as plotly.tools.make_subplots.
# Grid no longer printed by default
# 
# When the print_grid argument to make_subplots is set to True, a text 
# representation of the subplot grid is printed by the make_subplots function. 
# In version 3, the default value of print_grid was True. In version 4, 
# the default value of print_grid is False.
# 
# New row_heights argument to replace row_width
# 
# The legacy argument for specifying the relative height of subplot rows 
# was called row_width. A new row_heights argument has been introduced for 
# this purpose.
# 
#     Note: Although it is not mentioned in the docstring for 
#     plotly.subplots.make_subplots, the legacy row_width argument, with 
#     the legacy behavior, is still available in version 4.
# 
# In addition to having a more consistent name, values specified to the new 
# row_heights argument properly honor the start_cell argument. With the 
# legacy row_width argument, the list of heights was always interpreted 
# from the bottom row to the top row, even if start_cell=="top-left". With 
# the new row_heights argument, the list of heights is interpreted from 
# top to bottom if start_cell=="top-left" and from bottom to top if 
# start_cell=="bottom-left".
# 
# When porting code from row_width to row_heights, the order of the heights 
# list must be reversed if start_cell=="top-left" or start_cell was unspecified.
# 
# Here is a version 3 compatible example that uses the row_width argument 
# to create a figure with subplots where the top row is twice as tall as 
# the bottom row.
fig = make_subplots(
    rows=2, cols=1,
    row_width=[0.33, 0.67],
    start_cell="top-left")

fig.add_scatter(y=[2, 1, 3], row=1, col=1)
fig.add_bar(y=[2, 3, 1], row=2, col=1)
fig.show()

# And here is the equivalent, version 4 example. Note how the order to 
# the height list is reversed compared to the example above.
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.67, 0.33],
    start_cell="top-left")

fig.add_scatter(y=[2, 1, 3], row=1, col=1)
fig.add_bar(y=[2, 3, 1], row=2, col=1)
fig.show()

# Implementation of shared axes with make_subplots
# 
# The implementation of shared axis support in the make_subplots function 
# has been simplified. Prior to version 4, shared y-axes were implemented 
# by associating a single yaxis object with multiple xaxis objects, and 
# vica versa.
# 
# In version 4, every 2D Cartesian subplot has a dedicated x-axis and and 
# a dedicated y-axis. Axes are now "shared" by being linked together using 
# the matches axis property.
# 
# For legacy code that makes use of the make_subplots and add trace APIs, 
# this change does not require any action on the user's part. However, 
# legacy code that uses make_subplots to create a figure with shared axes, 
# and then manipulates the axes directly, may require updates. The output 
# of the .print_grid method on a figure created using make_subplots can be 
# used to identify which axis objects are associated with each subplot.
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
fig.print_grid()
print(fig)

# This is the format of your plot grid as output by the preceeding print()
# statement:
#[ (1,1) x,y   ]  [ (1,2) x2,y2 ]

#Figure({
#    'data': [],
#    'layout': {'template': '...',
#               'xaxis': {'anchor': 'y', 'domain': [0.0, 0.45]},
#               'xaxis2': {'anchor': 'y2', 'domain': [0.55, 1.0]},
#               'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0]},
#               'yaxis2': {'anchor': 'x2', 'domain': [0.0, 1.0], 'matches': 'y', 'showticklabels': False}}
#})

# Since the plot has no data for now, do not bother displaying it:
#fig.show()

# Trace UIDs
# 
# In version 3, all trace graph objects were copied and assigned a new uid 
# property when being added to a Figure. In version 4, these uid properties 
# are only generated automatically when a trace is added to a FigureWidget. 
# When a trace is added to a standard Figure graph object the input uid, 
# if provided, is accepted as is.
# Timezones
# 
# Prior to version 4, when plotly.py was passed a datetime that included a 
# timezone, the datetime was automatically converted to UTC. In version 4, 
# this conversion is no longer performed, and datetime objects are accepted 
# and displayed in local time.
# Headless image export on Linux with Xvfb.
# 
# In version 4, the static image export logic attempts to automatically 
# detect whether to call the orca image export utility using Xvfb. Xvfb is 
# needed for orca to work in a Linux environment if an X11 display server 
# is not available. By default, Xvfb is used if plotly.py is running on 
# Linux if no X11 display server is detected and Xvfb is available on the 
# system PATH.
# 
# This new behavior can be disabled by setting the use_xvfb orca configuration 
# option to False as follows:
# 
# import plotly.io as pio
# pio.orca.config.use_xvfb = False
# 
# Removals
# 
# fileopt argument removal
# 
# The fileopt argument to chart_studio.plotly.plot has been removed, so 
# in-place modifications to previously published figures are no longer 
# supported.
# 
# Legacy online GraphWidget
# 
# The legacy online-only GraphWidget class has been removed. Please use 
# the plotly.graph_objects.FigureWidget class instead. See the Figure Widget 
# Overview for more information.
# 
# Recommended style updates
# 
# Import from graph_objects instead of graph_objs
# 
# The legacy plotly.graph_objs package has been aliased as plotly.graph_objects 
# because the latter is much easier to communicate verbally. The 
# plotly.graph_objs package is still available for backward compatibility.

