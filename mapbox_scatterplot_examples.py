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
import plotly.express as px # Plotly Express is the easy-to-use, high-level
                            # interface to Plotly, which operates on "tidy"
                            # data and produces easy-to-style figures.

# To plot on Mapbox maps with Plotly, a Mapbox account and a public 
# Mapbox Access Token is needed. Let's just use mine:
px.set_mapbox_access_token(open(".mapbox_token").read())


data = px.data.carshare()
figure = px.scatter_mapbox(data, lat="centroid_lat", lon="centroid_lon",
    color="peak_hour", size="car_hours",
    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, 
    zoom=10)
figure.show()
