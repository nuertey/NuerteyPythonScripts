import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np

external_stylesheets = ['/home/rena/Workspace/Heating-Plant-Analysis/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)

df = pd.read_csv('/home/rena/Workspace/Heating-Plant-Analysis/boilerData.csv', index_col='Date', parse_dates=True)
df = df.fillna(method = 'ffill').fillna(method = 'bfill')

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Outdoor Temp', 'value': 'OAT'},
            {'label': 'Hot Water Supply Temp', 'value': 'HWST'},
            {'label': 'Hot Water Return Temp', 'value': 'HWRT'}
        ],
        value=['OAT','HWST','HWRT'],
        multi=True
    ),
    dcc.Graph(
        id='hws',
        figure={
            'data': [
                {'x': df.index, 'y': df.HWST, 'type': 'line', 'name': 'hwst'},
                {'x': df.index, 'y': df.HWRT, 'type': 'line', 'name': 'hwrt'},
                {'x': df.index, 'y': df.OAT, 'type': 'line', 'name': 'oat'},
            ],
            'layout': {
                'title': 'Heating System Data Visualization'
            }
        }
    )
])

# I was hoping in the drop down the person could select between the 
# points HWST, HWRT, OAT whether they want to see all 3 on a plot or 
# just one/two.. – HenryHub Jun 12 '19 at 20:56

# What you need to know is that the callback takes Input from some Dash 
# element (here the value of the dropdown) and returns to Output for some 
# property of another Dash element (here the figure from the graph; 
# notice we only change the data property).

# One other question I have is it possible with dash to bring a calculated
# parameter up to the front end? I think I could this with Flask & Jinja... 
# For example in dash maybe between an HTML div, would it be possible to 
# show something like correlation between two points? IE, correlation = 
# df['HWST'].corr(df['OAT']) – HenryHub Jun 13 '19 at 13:29
#
# I'm not entirely sure what you mean "correlation between two points" 
# (you mean arrays?) and "bring [...] to the front end" but if you want 
# to have details about specific points appear on hover, there is a 
# parameter (I think description) for that in plotly/dash graphs. If you 
# want something to appear in another element (say the correlation you 
# calculated with a few comments) you can create another html.P element 
# (or other) in your app.layout and then modify the callback to have 2 
# outputs: [Output('hws', 'figure'), Output('myP', 'children')], 
# [Input(...)] – Kostas Mouratidis Jun 14 '19 at 4:59

@app.callback(
    dash.dependencies.Output('hws', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(columns):
    return {"data": [{'x': df.index, 'y': df[col], 'type':'line', 'name': col}
                     for col in columns]}

if __name__ == '__main__':
    app.run_server(debug=True)
