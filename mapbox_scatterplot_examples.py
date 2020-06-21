#***********************************************************************
# @file
#
# Small python script illustrating how to generate scatter plots on 
# Mapbox maps in Python. 
#
# @note 
#
# @warning  None
#
#  Created: Twilight of April 22, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import plotly.graph_objects as go # low-level interface to figures, 
                                  # traces and layout
import plotly.express as px # Plotly Express is the easy-to-use, high-level
                            # interface to Plotly, which operates on "tidy"
                            # data and produces easy-to-style figures.
import pandas as pd


# To plot on Mapbox maps with Plotly, a Mapbox account and a public 
# Mapbox Access Token is needed. Let's just use mine:
token = open(".mapbox_token").read() 

# ==========
# Example 1:
# ==========
# O'Hare International Airport, Chicago, IL
#
# to (by bus)
#
# LaGuardia Airport, Queens, NY
#
# to (by plane)
# 
# Douala International Airport, Cameroon
figure = go.Figure(go.Scattermapbox(
    mode = "markers+text+lines",
    lon = [-87.904724, -73.87396590000003, 9.7183], lat = [41.978611, 40.7769271, 4.0035],
    marker = {'size': 20, 'symbol': ["bus", "airport", "airport"]},
    text = ["Bus", "Airport", "Airport"],textposition = "bottom right"))

figure.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "satellite-streets", 'zoom': 0.7},
    showlegend = False)

figure.show()
figure = go.Figure(go.Scattermapbox(
    mode = "markers+text+lines",
    lon = [-87.963135, -0.171879, -0.013991], lat = [42.166283, 5.607005, 6.104996],
    marker = {'size': 20, 'symbol': ["walk", "airport", "home"]},
    text = ["Apartment", "Airport", "Home Is Home"],textposition = "bottom right"))

figure.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "satellite-streets", 'zoom': 0.7},
    showlegend = False)

figure.show()

# ==========
# Example 2:
# ==========
figure = go.Figure(go.Scattermapbox(
    mode = "markers+text+lines",
    lon = [-75, -80, -50], lat = [45, 20, -20],
    marker = {'size': 20, 'symbol': ["bus", "harbor", "airport"]},
    text = ["Bus", "Harbor", "airport"],textposition = "bottom right"))

figure.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "outdoors", 'zoom': 0.7},
    showlegend = False)

figure.show()

# ==========
# Example 3:
# ==========
px.set_mapbox_access_token(token)
data = px.data.carshare()
print(data)
print()

# Index of series is column name.
dataTypeSeries = data.dtypes 
print('Data type of each column of Dataframe :')
print(dataTypeSeries)
figure = px.scatter_mapbox(data, lat="centroid_lat", lon="centroid_lon",
    color="peak_hour", size="car_hours",
    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, 
    zoom=10)
figure.show()

# ==========
# Example 4:
# ==========
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv')
site_lat = df.lat
site_lon = df.lon
locations_name = df.text

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=locations_name,
        hoverinfo='text'
    ))

fig.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='rgb(242, 177, 172)',
            opacity=0.7
        ),
        hoverinfo='none'
    ))

fig.update_layout(
    title='Nuclear Waste Sites on Campus',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=token,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=3,
        style='satellite-streets'
    ),
)

fig.show()
