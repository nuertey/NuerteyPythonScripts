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
            "if": {"row_index": index},
                "backgroundColor": "#93FFDD",
                'color': 'black',
                'fontWeight': 'bold',
                'textAlign': 'left'
        },
                {
            'if': {'column_id': 'Goal'},
                'fontWeight': 'bold',
                'backgroundColor':'#E0F9FF',
                'textAlign': 'center'}],

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
