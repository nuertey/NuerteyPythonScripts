# What About Dash? What changes are necessary in the usage of Dash elements
# as a result of migrating plotly to version 4?
#
# Dash: Build beautiful, web-based analytic apps. No Javascript required.
# 
# Dash is an open-source framework for building analytical applications, 
# with no Javascript required, and it is tightly integrated with the Plotly
# graphing library.
# 
# Learn about how to install Dash at https://dash.plot.ly/installation.
# 
# Everywhere in this page that you see fig.show(), you can display the same
# figure in a Dash application by passing it to the figure argument of the
# Graph component from the built-in dash_core_components package like this:
import plotly.graph_objects as go # or plotly.express as px

fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

