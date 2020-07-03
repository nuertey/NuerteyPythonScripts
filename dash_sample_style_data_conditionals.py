# https://dash.plotly.com/datatable/style

# https://github.com/Zhiji022/Kelowna_cultural_plan_survey_analysis/blob/256fe704ad47a48c075339fba0975dc586d5d5e6/callbacks/second_tab/table_style.py

# https://stackoverflow.com/questions/56259327/dash-datatable-conditional-cell-formatting-isnt-working

# https://community.plotly.com/t/datatable-style-data-conditional-several-conditions/30990

the_buys = (orders['side'] == 'B')
            style={
                'textAlign': 'right',
                'color': colors['cyber_yellow'] * or red
            }

the_sells = (orders['side'] == 'S') and (orders['price'] == quotes['bid_price'])
            style={
                'textAlign': 'right',
                'color': colors['green_text']
            }

        style_data_conditional=[
        {
            "if": {"row_index": (orders['side'] == 'B')},
                'color': colors['cyber_yellow'],
                'fontWeight': 'bold'
        },
        {
            'if': {'column_id': 'Goal'},
                'fontWeight': 'bold',
                'backgroundColor':'#E0F9FF',
                'textAlign': 'center'
        }],

    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],

style_data_conditional=[
    {
        'if': {
            'column_id': i,
            'filter_query': '{' + str(i) + '} > 100'
        },
        'backgroundColor': '#99EE6B'
    } for i in col_list
] + [
    {
        'if' : {
            'column_id' : i,
            'filter_query' : '{' + str(i) + '} < 100'
            },
            'backgroundColor' : '#FF7373'
    } for i in col_list
]

style_data_conditional=[{
    "if": {
        'column_id': 'price',
        'filter_query': '{side} eq "B"'
        #                ^     ^ <-- required braces
    },
    "color": colors['cyber_yellow']
}] + [{
    "if": {
        'column_id': 'price',
        'filter_query': '{side} eq "S"'
        #                ^     ^ <-- required braces
    },
    "color": colors['green_text']
}]

# The error happens because you compare two pandas.Series objects with different indices. A simple solution could be to compare just the values in the series. Try it:
# TBD Nuertey Odzeyem, can use this approach too as an alternative to .isin() but .isin() is preferred.
if df1['choice'].values != df2['choice'].values

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
