import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State

df = pd.read_csv(
        'https://gist.githubusercontent.com/chriddyp/'
        'c78bf172206ce24f77d6363a2d754b59/raw/'
        'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
        'usa-agricultural-exports-2011.csv')

app = dash.Dash()
application = app.server

app.layout = html.Div([
    html.Div(id="table1"),

    html.Div([
        html.Button(id='submit-button',                
                children='Submit'
    )
    ]),    

])

@app.callback(Output('table1','children'),
            [Input('submit-button','n_clicks')],
                [State('submit-button','n_clicks')])

def update_datatable(n_clicks,csv_file):            
    if n_clicks:                            
        dfgb = df.groupby(['state']).sum()
        data = df.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (df.columns)]
        return dt.DataTable(data=data, columns=columns)


if __name__ == '__main__':
    application.run(debug=False, port=8080)
