import pandas as pd
import plotly.express as px

pd.set_option('display.max_rows', 100)

world_data = pd.read_csv("combined_output_dataframe.csv")
print(world_data)
print()

# Index of series is column name.
dataTypeSeries = world_data.dtypes 
print('Data type of each column of combined_output Dataframe :')
print(dataTypeSeries)

# ==========
# Example 1:
#
# Here is a simple map rendered with OpenStreetMaps tiles, without needing a Mapbox Access Token:
# ==========
fig = px.scatter_mapbox(world_data, lat="latitude", lon="longitude", hover_name="country", hover_data=["confirmed", "deaths"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=500)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# ==========
# Example 2:
#
# Here is a map rendered with the "dark" style from the Mapbox service, which requires an Access Token:
# ==========
token = open(".mapbox_token").read() 

world_data = pd.read_csv("combined_output_dataframe.csv")

color_scale = [
    "#fadc8f",
    "#f9d67a",
    "#f8d066",
    "#f8c952",
    "#f7c33d",
    "#f6bd29",
    "#f5b614",
    "#F4B000",
    "#eaa900",
    "#e0a200",
    "#dc9e00",
]

fig = px.scatter_mapbox(
    world_data, 
    lat="latitude", 
    lon="longitude",
    color="confirmed",
    size="scaled",
    size_max=50, 
    hover_name="country", 
    hover_data=["confirmed", "deaths"],
    color_continuous_scale=color_scale,
    zoom=3, 
    height=500
)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
