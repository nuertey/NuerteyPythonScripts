#***********************************************************************
# @file
#
# Demonstrating how to make quiver plots (2D vectors) and cone plots (3D 
# vector fields) in Python with Plotly. A quiver plot displays velocity
# vectors as arrows whereas a cone plot displays a 3D vector field using
# cones to represent the direction and norm of the vectors. 
#
# @note None
#
# @warning  None
#
#  Created: September 17, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# ======================================================================
# Note that the length of the vector is referred to as the vector norm or 
# the vector's magnitude. The length of a vector is a nonnegative number 
# that describes the extent of the vector in space, and is sometimes 
# referred to as the vector's magnitude or the norm.
# ======================================================================

# ======================================================================
# Quiver Plots in Python with Plotly
#
# How to make a quiver plot in Python. A quiver plot displays velocity 
# vectors as arrows. Quiver plots can be made using a figure factory as 
# detailed below:
# ======================================================================

# Basic Quiver Plot:
x, y = np.meshgrid(np.arange(0, 2, .2), np.arange(0, 2, .2))
u = np.cos(x)*y
v = np.sin(x)*y

figure_1 = ff.create_quiver(x, y, u, v)
figure_1.show()

# Quiver Plot with Points:
x, y = np.meshgrid(np.arange(-2, 2, .2),
                   np.arange(-2, 2, .25)
                  )
                  
z = x*np.exp((-x)**2 - y**2)
v, u = np.gradient(z, .2, .2)

# Create quiver figure:
figure_2 = ff.create_quiver(x, y, u, v,
                            scale=.25,
                            arrow_scale=.4,
                            name='quiver',
                            line_width=1
                           )

# Add points to figure:
figure_2.add_trace(go.Scatter(x=[-.7, .75], 
                              y=[0, 0],
                              mode='markers',
                              marker_size=12,
                              name='points')
                  )

figure_2.show()

# ======================================================================
# 3D Cone Plots in Python
# 
# How to make 3D Cone plots in Python with Plotly. A cone plot is the 3D 
# equivalent of a 2D quiver plot, i.e., it represents a 3D vector field 
# using cones to represent the direction and norm of the vectors. 
# 3-D coordinates are given by x, y and z, and the coordinates of the 
# vector field by u, v and w.
# ======================================================================

# Basic 3D Cone. The middle of the cone seems to be here the:
#
# {x:1, y:1, z:1; norm:1.41}
figure_3 = go.Figure(data=go.Cone(x=[1], 
                                  y=[1], 
                                  z=[1], 
                                  u=[1], 
                                  v=[1], 
                                  w=[0])
                    )

figure_3.update_layout(scene_camera_eye=dict(x=-0.76, y=1.8, z=0.92))

figure_3.show()

# Multiple 3D Cones. The pinpoints of the cones seems to be here these:
#
# {x:1, y:1, z:1; norm:1.00}
# {x:2, y:2, z:2; norm:3.00}
# {x:3, y:3, z:3; norm:2.00}
figure_4 = go.Figure(data=go.Cone(x=[1, 2, 3],
                                  y=[1, 2, 3],
                                  z=[1, 2, 3],
                                  u=[1, 0, 0],
                                  v=[0, 3, 0],
                                  w=[0, 0, 2],
                                  sizemode="absolute",
                                  sizeref=2,
                                  anchor="tip")
                    )

figure_4.update_layout(
      scene=dict(domain_x=[0, 1],
                 camera_eye=dict(x=-1.57, y=1.36, z=0.58)))

figure_4.show()

# 3D Cone Lighting:
figure_5 = go.Figure()
figure_5.add_trace(go.Cone(x=[1,] * 3, name="base"))
figure_5.add_trace(go.Cone(x=[2,] * 3, opacity=0.3, name="opacity:0.3"))
figure_5.add_trace(go.Cone(x=[3,] * 3, lighting_ambient=0.3, name="lighting.ambient:0.3"))
figure_5.add_trace(go.Cone(x=[4,] * 3, lighting_diffuse=0.3, name="lighting.diffuse:0.3"))
figure_5.add_trace(go.Cone(x=[5,] * 3, lighting_specular=2, name="lighting.specular:2"))
figure_5.add_trace(go.Cone(x=[6,] * 3, lighting_roughness=1, name="lighting.roughness:1"))
figure_5.add_trace(go.Cone(x=[7,] * 3, lighting_fresnel=2, name="lighting.fresnel:2"))
figure_5.add_trace(go.Cone(x=[8,] * 3, 
                           lightposition=dict(x=0, y=0, z=1e5),
                           name="lighting.position x:0,y:0,z:1e5"))

figure_5.update_traces(y=[1, 2, 3], 
                  z=[1, 1, 1],
                  u=[1, 2, 3], 
                  v=[1, 1, 2], 
                  w=[4, 4, 1],
                  hoverinfo="u+v+w+name",
                  showscale=False
                 )

figure_5.update_layout(scene=dict(aspectmode="data",
                  camera_eye=dict(x=0.05, y=-2.6, z=2)),
                  margin=dict(t=0, b=0, l=0, r=0)
                 )

figure_5.show()

# 3D Cone Vortex:
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/vortex.csv")

print('df:')
print(df)
print()

print('df.info():')
print(df.info())
print()

figure_6 = go.Figure(data = go.Cone(x=df['x'],
                                    y=df['y'],
                                    z=df['z'],
                                    u=df['u'],
                                    v=df['v'],
                                    w=df['w'],
                                    colorscale='Blues',
                                    sizemode="absolute",
                                    sizeref=40)
                    )

figure_6.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=0.8),
                       camera_eye=dict(x=1.2, y=1.2, z=0.6))
                      )

figure_6.show()
