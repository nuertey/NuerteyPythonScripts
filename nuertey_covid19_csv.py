#***********************************************************************
# @file
#
# Python script for querying COVID-19 statistics via John Hopkins API
# and visualizing them.
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
import os
import sys
import argparse
import pandas as pd
import plotly.express as px
from covid import Covid

pd.set_option('display.max_rows', 100)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-h] | [-v] | [-d]",
        description="Visualize COVID-19 statistics data on the World map.",
        allow_abbrev=False,
        add_help=True
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 0.0.2"
    )
    parser.add_argument(
        "-d", "--download", action='store_true',
        help="Download realtime data from John Hopkins data source. Absence of this argument would imply that \"combined_output_dataframe.csv\" would rather be used as the input data source."
    )
    return parser

parser = init_argparse()
args = parser.parse_args()
data_source_file_name = "combined_output_dataframe.csv"

if not args.download:
    if not os.path.isfile(data_source_file_name):
        print("The data source file specified \"{0}\" does not exist".format(data_source_file_name))
        sys.exit()
else:
    source = "john_hopkins"  # Currently, the only source supported by this script.
    cov_19 = Covid(source)
    country_list = cov_19.list_countries()
    data = pd.DataFrame(country_list)
    print(data)
    print()
    
    cols = ['country_id', 'country', 'confirmed', 'active', 'deaths', 'recovered', 
            'latitude', 'longitude', 'last_update', 'scaled']
    combined_output = pd.DataFrame(columns=cols, index=data.index)
    
    for row, country_name_input in zip(data.index, data['name']):
        country_status = cov_19.get_status_by_country_name(str(country_name_input))
        # These ensuing on-the-fly integer casts do not seem to matter to
        # the combined_output dataframe as its members still register as 
        # PyTypeObject, that is, a 'new type'. But keep the code as-is 
        # for now for instructive purposes.
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
    
    # Since the DataFrame is in the default 'object' dtype, and the plotters
    # below rather need the data information in integer and floats, use the
    # technique of writing everything to a CSV file and then reading it again
    # so that it is automagically converted into the numeric types for us.
    # Calm, peaceful sleep, silence and minimized stress leads to good thought.   
    combined_output.to_csv(data_source_file_name, index = False, header=True)

# Read the data back in the proper numeric formats:
world_data = pd.read_csv(data_source_file_name)
#print(world_data)
#print()

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

# The fuchsia color code is #FF00FF. Here it is graded in order of increasing strength:
magenta_gradient = [
    "#ff00ff",
    "#e800e7",
    "#cc00cc",
    "#b000af",
    "#8b008b",
]

# The Hot Gradient Color Scheme palette has 6 colors which are Red (#FE0000),
# Red-Orange (X11) (#FE3F02), University Of Tennessee Orange (#F97C00), 
# Orange Peel (#FB9E00), Cyber Yellow (#FBD400) and Lemon Glacier (#FDFD04).
hot_gradient = [
    "#fdfd04",
    "#fbd400",
    "#fb9e00",
    "#f97c00",
    "#fe3f02",
    "#fe0000",
]

# ==========
# Example 1:
#
# Here is a simple map rendered with OpenStreetMaps tiles, without needing
# a Mapbox Access Token:
# ==========
#     color_discrete_sequence=["fuchsia"], 
figure = px.scatter_mapbox(
    world_data, 
    lat="latitude", 
    lon="longitude", 
    color="confirmed",
    size="scaled",
    size_max=50,
    hover_name="country", 
    hover_data=["confirmed", "deaths"],
    color_continuous_scale=magenta_gradient,
    zoom=3, 
    height=700
)
figure.update_layout(mapbox_style="open-street-map")
figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Replace the displayed latitude and longitude with custom-labelled data:
#print(figure.data[0].hovertemplate)
figure.data[0].update(
    hovertemplate="<b>%{hovertext}</b><br><br>Confirmed=%{marker.color}<br>Deaths=%{customdata[1]}"
)

figure.show()

# ==========
# Example 2:
#
# Here is a map rendered with the "dark" style from the Mapbox service, 
# which requires an Access Token. Obtain your free access token from www.mapbox.com
# and save it in the current directory as the filename below, '.mapbox_token':
# ==========
token = open(".mapbox_token").read()

#    color_continuous_scale=px.colors.cyclical.IceFire,
figure = px.scatter_mapbox(
    world_data, 
    lat="latitude", 
    lon="longitude",
    color="confirmed",
    size="scaled",
    size_max=50, 
    hover_name="country", 
    hover_data=["confirmed", "active", "deaths"],
    color_continuous_scale=hot_gradient,
    zoom=3, 
    height=700
)

#    mapbox_style="satellite-streets",
figure.layout.update(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    # This takes away the colorbar on the right hand side of the plot
    #coloraxis_showscale=False,
    mapbox_accesstoken=token,
    mapbox_style="dark",
    # Center the map on Ghana, literally center of the World:
    mapbox=dict(center=dict(lat=float(7.9465), lon=float(1.0232)), zoom=3,),
)

#print(figure.data[0].hovertemplate)
figure.data[0].update(
    hovertemplate="<b>%{hovertext}</b><br><br>Confirmed=%{marker.color}<br>Active=%{customdata[1]}<br>Deaths=%{customdata[2]}"
)

figure.show()
