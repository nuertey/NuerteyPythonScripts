import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

figure2 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

figure2.update_layout(
    title="Sample Plot Title",
    xaxis_title="testing x",
    yaxis_title="testing y"
)

df = px.data.iris() # iris is a pandas DataFrame
figure3 = px.scatter(df, x="sepal_width", y="sepal_length")

figure4 = go.Figure()

figure4.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    name="Name of Trace 1"       # this sets its legend entry
))


figure4.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
    name="Name of Trace 2"
))

figure4.update_layout(
    title="Plot Title",
    xaxis_title="X-Axis Title (Nuertey)",
    yaxis_title="Y-Axis Title (Odzeyem)",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash. Nuertey Odzeyem Arriveth!',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Dash: A web application framework for Python. Nuertey\'s Very First Example...', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title':'Bar Graph of San Francisco Versus Montreal',
                'xaxis':{
                    'title':'X-Axis Title'
                },
                'yaxis':{
                    'title':'Y-Axis Title'
                }
            }
        }
    ),
    dcc.Graph(
        id='example-graph-2',
        figure=figure2
    ),
    dcc.Graph(id='example-graph-3', 
        figure=figure3
    ),
    dcc.Graph(id='example-graph-4', 
        figure=figure4
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
