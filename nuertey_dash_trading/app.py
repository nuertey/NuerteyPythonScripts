#***********************************************************************
# @file
#
# Nuertey's first full-blown Dash web application that presents an automatic
# Trading Application dashboard to the user. It effectively allows the user
# to visualize Nuertey's VWAP Stock Trading Algorithm in action. A secondary
# purpose of this script is to illustrate some teaching ideas to Wayo and 
# other dear students.
#
# @note [1] Chose a country from the drop down list for the current news
#           headlines in that country to be displayed to the user. Clicking 
#           on each news item headline will open a tab for that news item 
#           from the news agency of concern. 
#
#       [2] Incoming stock trades as captured in the PostgreSQL database
#           are displayed to the user.
#
#       [3] Incoming stock quotes as captured in the PostgreSQL database
#           are displayed to the user.
#
#       [4] Outgoing customer stock orders generated by the VWAP algorithm
#           and captured in the PostgreSQL database are displayed to the
#           user.
#
#       [5] Within the quotes table, good Buys, that is, "Ask prices less
#           than or equal to the current VWAP" will change color to red.
#
#       [6] Within the quotes table, good Sells, that is, "Bid prices 
#           greater than or equal to the current VWAP" will change color
#           to green.
#
#       [7] Note that per \'Customer\' requirements, only one order side
#           (BUY or SELL) can be traded at a time.
#
#       [8] The rolling VWAP as calculated and captured in the PostgreSQL 
#           database will be plotted and continuously updated for the user.
#               
# @warning  None
#
#  Created: Amidst the rental and job stresses/uncertainties of July 1st, 
#           2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import os
import sys
import json
import base64
import random
import datetime
import requests
import psycopg2
import pandas as pd
from http import HTTPStatus
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from news_config import COUNTRY_CODES

pd.set_option('display.max_rows', 200)
pd.set_option('display.min_rows', 200)

try:
    app = dash.Dash(
        __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    )
    server = app.server

    colors = {
        'background': '#111111',
        'text': '#7FDBFF',
        'red_text': '#F8051B',
        'yellow_text': '#FCF804',
        'green_yellow_text': '#B1FA08',
        'green_text': '#0CFA08',
        'blue_text': '#041EFC',
        'red_yellow_text': '#FC5E04',
        'cyber_yellow': '#FBD400',
        'lemon_glacier': '#FDFD04',
        'fuchsia': '#FF00FF',
        'picton_blue': '#3DBDFF', 
        'electric_blue': '#64EEFA',
        'pale_aquamarine': '#A4FFEC',
        'pumpkin': '#FD6E10', 
        'royal_orange': '#F79039',
        'rajah': '#F7B155',
        'feldspar': '#FFD5B2', 
        'deep_peach': '#F6C7A0',
    }

    def get_random_color_not_background():
        color_pick = random.choice(list(colors.values()))
        if color_pick == colors['background']:
            color_pick = colors['cyber_yellow']
        return color_pick

    connect_str = "dbname='stock_trading' user='nuertey' host='localhost' " + \
                  "password='krobo2003'"

    connection = psycopg2.connect(connect_str)

    trades = pd.read_sql('select * from trades', connection)
    quotes = pd.read_sql('select * from quotes', connection)
    orders = pd.read_sql('select * from orders', connection)

    country_codes = pd.DataFrame(COUNTRY_CODES)
    codes_dictionary = country_codes.to_dict('list')
    country_code = 'ng' # Default country code = Nigeria for testing and to prick Wayo and Emile's interest.
    culprit_country_name = country_codes.loc[country_codes['value'] == country_code,'label']
    culprit_country_name = next(iter(culprit_country_name), 'no match')

    token = open(".newsapi_token").read().rstrip('\n')

    # API Call to update news
    def update_news(the_code=country_code, the_name=culprit_country_name):
        culprit_country_name = the_name
        news_api_url = f"https://newsapi.org/v2/top-headlines?country={the_code}&apiKey={token}"
        reply = requests.get(news_api_url)
        the_composed_news = html.Div([html.P('Placeholder Text'),])
        if reply.ok:
            text_data = reply.text
            json_dict = json.loads(text_data)
            if json_dict["totalResults"] > 0:
                df = pd.DataFrame.from_dict(json_dict["articles"])
                df = pd.DataFrame(df[["title", "url"]])
                max_rows = 40
                the_composed_news = html.Table(
                    className="table-news",
                    children=[
                        html.Tr(
                            children=[
                                html.Td(
                                    children=[
                                        html.A(
                                            className="td-link",
                                            children=df.iloc[i]["title"],
                                            href=df.iloc[i]["url"],
                                            target="_blank",
                                            style={'textAlign': 'left', 
                                                   'color': get_random_color_not_background()},
                                        )
                                    ]
                                )
                            ]
                        )
                        for i in range(min(len(df), max_rows))
                    ],
                )
            else:
                composed_news = "Sorry. No online news articles were discovered for \"{0}\". Check meatspace.".format(culprit_country_name)
                the_composed_news = html.Div(children=composed_news, style={
                    'textAlign': 'center',
                    'color': colors['red_text']
                })
        else:
            composed_news = f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}'
            reply_json = json.loads(reply.text)
            composed_news = composed_news + "<br>" + json.dumps(reply_json, indent=2)
            the_composed_news = html.Div(children=composed_news, style={
                'textAlign': 'center',
                'color': colors['red_text']
            })

        return html.Div(
            children=[
                html.P(className="p-news", children="News Headlines",
                    style={'textAlign': 'left', 'color': colors['green_text']}
                ),
                html.P(
                    className="p-news float-right",
                    children="Last update : "
                    + datetime.datetime.now().strftime("%H:%M:%S"),
                    style={'textAlign': 'left', 'color': colors['green_text']}
                ),
                the_composed_news,
            ]
        )

    # Create the VWAP trace contrasted with the stock trades price:
    figure1 = go.Figure()
    figure1.add_trace(go.Scatter(x=trades.index, y=trades['price'],
                        mode='lines+markers',
                        name='Stock Exchange Trades Price'))
    figure1.add_trace(go.Scatter(x=trades.index, y=trades['volume_weighted_average_price'],
                        mode='lines+markers',
                        name='Volume-Weighted Average Price (VWAP)'))
    figure1.update_layout(
        title="Stock Exchange Trades Price Versus Volume-Weighted Average Price (VWAP)",
        xaxis_title="Timestamp",
        yaxis_title="Price"
    )

    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        # dcc.Interval is a component that will fire a callback periodically. 
        # Use dcc.Interval to update your app in realtime without needing 
        # to refresh the page or click on any buttons.

        # Interval component for live clock updates:
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),

        # Interval component for graph, database tables and price comparison updates:
        dcc.Interval(id="i_tris", interval=1 * 5000, n_intervals=0),

        html.H1(
            children='Nuertey Odzeyem\'s VWAP Stock Trading Dash Web Application',
            style={
                'textAlign': 'center',
                'color': colors['cyber_yellow']
            }
        ),
        # Div for dropdown list:
        dcc.Dropdown(
            id='demo-dropdown',
            options=[{'label': i, 'value': i} for i in country_codes['label']],
            value=culprit_country_name
        ),
        # Div for dropdown list output container:
        html.Div(id='dd-output-container', style={'color': colors['green_text']}),
        # Left Panel Div
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.Img(
                            className="author-image", src=app.get_asset_url("nuertey_image_dressy2.png")
                        ),
                        html.H2(className="title-header", children="FOREX TRADER"),
                        html.P(children=[html.Strong('Author: Nuertey Odzeyem')]),
                        html.P(children=[html.Strong('Created: July 1st, 2020')]),
                        html.P(children=[html.Strong('Goal: To illustrate ideas to Wayo, Emile, Mbui, Scott, etc.')]),
                    ],
                    style={
                        'textAlign': 'left',
                        'color': colors['red_yellow_text']
                    }
                ),
                # Div for realtime clock:
                html.Div(
                    className="div-currency-toggles",
                    children=[
                        html.P(
                            id="live_clock",
                            className="three-col",
                            children=datetime.datetime.now().strftime("%H:%M:%S"),
                        ),
                    ],
                    style={'textAlign': 'left', 'color': colors['green_text']}
                ),
                # Div for News Headlines:
                html.Div(
                    className="div-news",
                    children=[html.Div(id="news", children=update_news())],
                ),
            ],
        ),
        # Summary Divide Panel Div
        html.Div(                    
            children=[
                html.H4(
                    children='Description/Overview:',
                    style={
                        'textAlign': 'left',
                        'color': colors['red_text']
                    }
                ),
                html.P('Nuertey\'s first full-blown Dash web application that presents an automatic Trading Application dashboard to the user. It effectively allows the user to visualize Nuertey\'s VWAP Stock Trading Algorithm in action. A secondary purpose of this script is to illustrate some teaching ideas to Wayo, Emile, Mbui, Scott and other dear students.'),
                html.H4(
                    children='Notes:',
                    style={
                        'textAlign': 'left',
                        'color': colors['blue_text']
                    }
                ),
                html.P('[1] Chose a country from the drop down list for the current news headlines in that country to be displayed to the user. Clicking on each news item headline will open a tab for that news item from the news agency of concern.'),
                html.P('[2] Incoming stock trades as captured in the PostgreSQL database are displayed to the user.'),
                html.P('[3] Incoming stock quotes as captured in the PostgreSQL database are displayed to the user.'),
                html.P('[4] Outgoing customer stock orders generated by the VWAP algorithm and captured in the PostgreSQL database are displayed to the user.'),
                html.P('[5] Within the quotes and customer stock orders tables, good Buys, that is, \"Ask prices less than or equal to the current VWAP\" will change color to red.'),
                html.P('[6] Within the quotes and customer stock orders tables, good Sells, that is, \"Bid prices greater than or equal to the current VWAP\" will change color to green.'),
                html.P('[7] The rolling VWAP as calculated and captured in the PostgreSQL database will be plotted and continuously updated for the user.'),
            ], 
            style={'textAlign': 'left', 'color': colors['text']}
        ),
        # Right Panel Div
        html.Div(
            className="nine columns div-right-panel",
            children=[
                html.H4(
                    children='Incoming Stock Exchange Trades + Calculated VWAP',
                    style={
                        'textAlign': 'center',
                        'color': colors['red_text']
                    }
                ),
                # Dash DataTable is an interactive table component designed for 
                # viewing, editing, and exploring large datasets. DataTable is 
                # rendered with standard, semantic HTML <table/> markup, which 
                # makes it accessible, responsive, and easy to style. This component 
                # was written from scratch in React.js specifically for the Dash
                # community. Its API was designed to be ergonomic and its behavior
                # is completely customizable through its properties. 7 months in 
                # the making, this is the most complex Dash component that Plotly
                # has written, all from the ground-up using React and TypeScript. 
                # DataTable was designed with a featureset that allows for Dash
                # users to create complex, spreadsheet driven applications with 
                # no compromises:
                dash_table.DataTable(
                    id='stock-trades',
                    columns=[{"name": i, "id": i} for i in trades.columns],
                    data=trades.to_dict('records'),
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'fontWeight': 'bold',
                        'color': colors['fuchsia']
                    },
                    style_cell={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_data_conditional=[{
                        "if": {
                            'column_id': 'volume_weighted_average_price'
                        },
                        "color": colors['cyber_yellow']
                    }]
                ),
                html.H4(
                    children='Incoming Stock Exchange Quotes',
                    style={
                        'textAlign': 'center',
                        'color': colors['fuchsia']
                    }
                ),
                html.H5(
                    children='* Green = Great Quoted Price! Nuertey\'s Automatic VWAP Stock Trading Algorithm Will Decide To Sell.',
                    style={
                        'textAlign': 'left',
                        'color': colors['green_text']
                    }
                ),
                html.H5(
                    children='* Red = Great Quoted Price! Nuertey\'s Automatic VWAP Stock Trading Algorithm Will Decide To Buy.',
                    style={
                        'textAlign': 'left',
                        'color': colors['red_text']
                    }
                ),
                html.H5(
                    children='* Note that per \'Customer\' requirements, only one order side (BUY or SELL) is traded at a time.',
                    style={
                        'textAlign': 'left',
                        'color': colors['cyber_yellow']
                    }
                ),
                dash_table.DataTable(
                    id='stock-quotes',
                    columns=[{"name": i, "id": i} for i in quotes.columns],
                    data=quotes.to_dict('records'),
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'fontWeight': 'bold',
                        'color': colors['blue_text']
                    },
                    style_cell={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_data_conditional = [{
                        'if': {
                            'column_id': 'ask_price',
                            "row_index": x
                        },
                        'color': colors['red_text']
                    } for x in quotes[quotes['timestamped'].isin(orders.loc[orders[orders['side'] == "B"].index, 'timestamped'])].index 
                    ] + [{
                        'if': {
                            'column_id': 'bid_price',
                            "row_index": x
                        },
                        'color': colors['green_text']
                    } for x in quotes[quotes['timestamped'].isin(orders.loc[orders[orders['side'] == "S"].index, 'timestamped'])].index 
                    ]
                ),
                html.H4(
                    children='Outgoing Customer Stock Orders',
                    style={
                        'textAlign': 'center',
                        'color': colors['pumpkin']
                    }
                ),
                dash_table.DataTable(
                    id='stock-orders',
                    columns=[{"name": i, "id": i} for i in orders.columns],
                    data=orders.to_dict('records'),
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'fontWeight': 'bold',
                        'color': colors['picton_blue']
                    },
                    style_cell={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_data_conditional=[{
                        "if": {
                            'column_id': 'price',
                            'filter_query': '{side} eq "B"'
                        },
                        "color": colors['red_text']
                    }] + [{
                        "if": {
                            'column_id': 'price',
                            'filter_query': '{side} eq "S"'
                        },
                        "color": colors['green_text']
                    }]
                ),
                html.H4(
                    children='Visualization Graphs',
                    style={
                        'textAlign': 'center',
                        'color': colors['electric_blue']
                    }
                ),
                # Div for VWAP trace and trades price graphs:
                dcc.Graph(id='graph-1', 
                    figure=figure1
                )
            ],
        ),
    ])

    # Callback to update country of choice for news headlines:
    @app.callback([Output('dd-output-container', 'children'), Output("news", "children")], [Input('demo-dropdown', 'value')])
    def update_output(value):
        culprit_country_name = value
        country_code = country_codes.loc[country_codes['label'] == culprit_country_name,'value']
        country_code = next(iter(country_code), 'no match')
        return 'You have selected "{}" for top news headlines.'.format(culprit_country_name), update_news(country_code, culprit_country_name)

    # Callback to update live clock:
    @app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
    def update_time(n):
        return datetime.datetime.now().strftime("%H:%M:%S")

    # Callback to update trades table, orders table and generated graph:
    @app.callback([Output('stock-trades', 'data'), Output('stock-orders', 'data'), Output('graph-1', 'figure')], [Input("i_tris", "n_intervals")])
    def update_trades_and_graph(n):
        trades = pd.read_sql('select * from trades', connection)
        orders = pd.read_sql('select * from orders', connection)

        # Create the VWAP trace contrasted with the stock trades price:
        figure1 = go.Figure()
        figure1.add_trace(go.Scatter(x=trades.index, y=trades['price'],
                            mode='lines+markers',
                            name='Stock Exchange Trades Price'))
        figure1.add_trace(go.Scatter(x=trades.index, y=trades['volume_weighted_average_price'],
                            mode='lines+markers',
                            name='Volume-Weighted Average Price (VWAP)'))
        figure1.update_layout(
            title="Stock Exchange Trades Price Versus Volume-Weighted Average Price (VWAP)",
            xaxis_title="Timestamp",
            yaxis_title="Price"
        )

        return trades.to_dict('records'), orders.to_dict('records'), figure1

    # Callback to update quotes table:
    @app.callback(Output('stock-quotes', 'data'), [Input("i_tris", "n_intervals")])
    def update_quotes(n):
        quotes = pd.read_sql('select * from quotes', connection)

        return quotes.to_dict('records')

except Exception as e:
    print("Error! General Exception caught:")
    print(e)

if __name__ == "__main__":
    app.run_server(debug=True)
