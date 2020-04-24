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
#  Created: April 12, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import plotly.express as px
import pandas as pd
from covid import Covid

pd.set_option('display.max_rows', 100)

#source="worldometers" # Source 1...
source="john_hopkins"  # Source 2...
#cov_19 = Covid() # Default is John Hopkins data.
cov_19 = Covid(source)
#data = cov_19.get_data()
country_list = cov_19.list_countries()
#print(country_list)
#print()

data = pd.DataFrame(country_list)
#print(data)
#print()

cols = ['country_id', 'country', 'confirmed', 'active', 'deaths', 'recovered', 
        'latitude', 'longitude', 'last_update', 'scaled']
combined_output = pd.DataFrame(columns=cols, index=data.index)

# Example output:
#
# 149 Sao Tome and Principe
# {'id': '149', 'country': 'Sao Tome and Principe', 'confirmed': 4, 'active': 4, 'deaths': 0, 'recovered': 0, 'latitude': 0.18636, 'longitude': 6.613081, 'last_update': 1587655832000}
for row in data.index:
    country_id_input = getattr(row, "id")
    country_name_input = getattr(row, "name")
    #print(country_id_input, country_name_input)
    country_status = cov_19.get_status_by_country_name(str(country_name_input))
    #print(country_status)
    #print()
    combined_output.loc[row].country_id = country_status['id']
    combined_output.loc[row].country = country_status['country']
    combined_output.loc[row].confirmed = country_status['confirmed']
    combined_output.loc[row].active = country_status['active']
    combined_output.loc[row].deaths = country_status['deaths']
    combined_output.loc[row].recovered = country_status['recovered']
    combined_output.loc[row].latitude = country_status['latitude']
    combined_output.loc[row].longitude = country_status['longitude']
    combined_output.loc[row].last_update = country_status['last_update']

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

# Employing the exponent operation, scale the data in order
# to render smaller values visible on the scatter mapbox.
combined_output["scaled"] = combined_output["confirmed"] ** 0.77
print(combined_output)
print()

lat, lon, zoom = (combined_output["latitude"], combined_output["longitude"], 5)

figure = px.scatter_mapbox(
    combined_output,
    lat="latitude",
    lon="longitude",
    color="confirmed",
    size="scaled",
    size_max=50,
    hover_name="country",
    hover_data=["confirmed", "deaths", "country"],
    color_continuous_scale=color_scale,
)

figure.layout.update(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    # This takes away the colorbar on the right hand side of the plot
    coloraxis_showscale=False,
    mapbox_style=config.MAPBOX_STYLE,
    mapbox=dict(center=dict(lat=lat, lon=lon), zoom=zoom,),
)

# https://community.plot.ly/t/plotly-express-scatter-mapbox-hide-legend/36306/2
print(fig.data[0].hovertemplate)
figure.data[0].update(
    hovertemplate="Confirmed: %{customdata[2]} <br>Active:%{customdata[3]} <br>Deaths: %{customdata[4]}<br>%{customdata[1]}"
)

figure.show()
