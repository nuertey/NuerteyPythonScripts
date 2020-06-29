import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__)

df = pd.read_csv('/home/rena/Workspace/Heating-Plant-Analysis/boilerData.csv', index_col='Date', parse_dates=True)
df = df.fillna(method = 'ffill').fillna(method = 'bfill')


app.layout = html.Div([

    html.H1('Heating System Temperature Data Visulation'), 
    html.Center('The purpose of the scatter plot below is to prove if a temperature reset strategy is implemented on the hydronic heating system. At various outside air temperature conditions, the hot water temperature should fluctuate to save energy.'),

    dcc.Graph(
        id='hwst-vs-oat',
        figure={
            'data': [
                go.Scatter(
                    x = df.OAT,
                    y = df.HWST,
                    mode = 'markers',
                    marker = dict(
                        color = '#FFBAD2',
                        line = dict(width = 1)
                    )
                )
            ],
            'layout':{
                'title':'Scatter Plot of OAT versus HWST',
                'xaxis':{
                    'title':'whatever you want x to be'
                },
                'yaxis':{
                    'title':'whatever you want y to be'
                }
            }
        }  
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
