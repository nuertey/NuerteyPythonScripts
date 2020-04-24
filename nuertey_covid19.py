#***********************************************************************
# @file
#
# Python script for querying COVID-19 statistics via several publicly
# available APIs and visualizing them.
#
# @note 
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
combined_output = pd.DataFrame(columns=cols, index=data.itertuples(index=True, name='Pandas'))

# Example output:
#
# 149 Sao Tome and Principe
# {'id': '149', 'country': 'Sao Tome and Principe', 'confirmed': 4, 'active': 4, 'deaths': 0, 'recovered': 0, 'latitude': 0.18636, 'longitude': 6.613081, 'last_update': 1587655832000}
for row in data.itertuples(index=True, name='Pandas'):
    country_id = getattr(row, "id")
    country_name = getattr(row, "name")
    #print(country_id, country_name)
    country_status = cov_19.get_status_by_country_name(str(country_name))
    print(country_status)
    print()
    combined_output.loc[row].country_id = country_status[0]
    combined_output.loc[row].country = country_status[1]
    combined_output.loc[row].confirmed = country_status[2]
    combined_output.loc[row].active = country_status[3]
    combined_output.loc[row].deaths = country_status[4]
    combined_output.loc[row].recovered = country_status[5]
    combined_output.loc[row].latitude = country_status[6]
    combined_output.loc[row].longitude = country_status[7]
    combined_output.loc[row].last_update = country_status[8]

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
# print(fig.data[0].hovertemplate)
figure.data[0].update(
    hovertemplate="%{customdata[3]}, %{customdata[2]}<br>Confirmed: %{customdata[0]}<br>Deaths: %{customdata[1]}"
)
