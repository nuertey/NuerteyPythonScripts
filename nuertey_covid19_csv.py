#***********************************************************************
# @file
#
# Python script for querying COVID-19 statistics via several publicly
# available APIs and visualizing them.
#
# @note For the future, these visualizations could be enhanced with live
# news articles on the 'COVID-19' topic via newsapi much like follows:
#
#https://newsapi.org/v2/top-headlines?country=us&apiKey=f048819049c24d6d86bd424daa2349f1
#
#http://newsapi.org/v2/everything?q=ghana&from=2020-01-01&sortBy=publishedAt&apiKey=f048819049c24d6d86bd424daa2349f1
#
# NEWS_API_KEY = config("NEWS_API_KEY")
# NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
#
# Notice the use of the python 3.6 introduced f-strings in the statement
# above. F-strings can be further explained by this code snippet:
#
# >>> name = "Adjoa"
# >>> age = 15
# >>> f"Hello, {name}. You are {age}."
# 'Hello, Adjoa. You are 15.'
#
# @warning  None
#
#  Created: April 29, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import pandas as pd
import plotly.express as px
from covid import Covid

pd.set_option('display.max_rows', 100)

#source="worldometers" # Source 1...
source="john_hopkins"  # Source 2...
#cov_19 = Covid() # Default is John Hopkins data.
cov_19 = Covid(source)
country_list = cov_19.list_countries()
data = pd.DataFrame(country_list)

cols = ['country_id', 'country', 'confirmed', 'active', 'deaths', 'recovered', 
        'latitude', 'longitude', 'last_update', 'scaled']
combined_output = pd.DataFrame(columns=cols, index=data.index)

for row, country_name_input in zip(data.index, data['name']):
    country_status = cov_19.get_status_by_country_name(str(country_name_input))
    combined_output.loc[row].country_id  = int(country_status['id'])
    combined_output.loc[row].country     = country_status['country']
    combined_output.loc[row].confirmed   = int(country_status['confirmed'])
    combined_output.loc[row].active      = int(country_status['active'])
    combined_output.loc[row].deaths      = int(country_status['deaths'])
    combined_output.loc[row].recovered   = int(country_status['recovered'])
    combined_output.loc[row].latitude    = country_status['latitude']
    combined_output.loc[row].longitude   = country_status['longitude']
    combined_output.loc[row].last_update = int(country_status['last_update'])

# Employing the exponent operation, scale the data in order
# to render smaller values visible on the scatter mapbox.
combined_output["scaled"] = combined_output["confirmed"] ** 0.77

combined_output.to_csv("combined_output_dataframe.csv", index = False, header=True)

world_data = pd.read_csv("combined_output_dataframe.csv")
#print(world_data)
#print()

# Index of series is column name.
#dataTypeSeries = world_data.dtypes 
#print('Data type of each column of combined_output Dataframe :')
#print(dataTypeSeries)

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

color_scale_2 = [
    "#fce9b8", 
    "#fbe6ad",
    "#fbe3a3",
    "#fbdf99",
    "#fadc8f",
    "#fad985",
    "#f9d67a",
    "#f9d370",
    "#f8d066",
    "#f8cc5c",
    "#f8c952",
    "#f7c647",
    "#f7c33d",
    "#f6c033",
    "#f6bd29",
    "#f5b91f",
    "#f5b614",
    "#f4b30a",
    "#F4B000",
    "#efac00",
    "#eaa900",
    "#e5a500",
    "#e0a200",
    "#dc9e00"
]

# ==========
# Example 1:
#
# Here is a simple map rendered with OpenStreetMaps tiles, without needing a Mapbox Access Token:
# ==========
fig = px.scatter_mapbox(
    world_data, 
    lat="latitude", 
    lon="longitude", 
    color="confirmed",
    size="scaled",
    size_max=50,
    hover_name="country", 
    hover_data=["confirmed", "deaths"],
    color_discrete_sequence=["fuchsia"], 
    zoom=3, 
    height=700
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#print(fig.data[0].hovertemplate)
fig.data[0].update(
    hovertemplate="<b>%{hovertext}</b><br><br>Confirmed=%{marker.color}<br>Deaths=%{customdata[1]}"
)

fig.show()

# ==========
# Example 2:
#
# Here is a map rendered with the "dark" style from the Mapbox service, which requires an Access Token:
# ==========
token = open(".mapbox_token").read() 

world_data = pd.read_csv("combined_output_dataframe.csv")

#    color_continuous_scale=px.colors.cyclical.IceFire,
fig = px.scatter_mapbox(
    world_data, 
    lat="latitude", 
    lon="longitude",
    color="confirmed",
    size="scaled",
    size_max=50, 
    hover_name="country", 
    hover_data=["confirmed", "active", "deaths"],
    color_continuous_scale=color_scale_2,
    zoom=3, 
    height=700
)
#fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()

#    mapbox_style="satellite-streets",
fig.layout.update(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    # This takes away the colorbar on the right hand side of the plot
    #coloraxis_showscale=False,
    mapbox_accesstoken=token,
    mapbox_style="dark",
    mapbox=dict(center=dict(lat=float(7.9465), lon=float(1.0232)), zoom=3,),
)

# https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
#print(fig.data[0].hovertemplate)
fig.data[0].update(
    hovertemplate="<b>%{hovertext}</b><br><br>Confirmed=%{marker.color}<br>Active=%{customdata[1]}<br>Deaths=%{customdata[2]}"
)

fig.show()
