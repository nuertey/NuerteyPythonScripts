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
                   np.arange(-2, 2, .25))
                  
z = x*np.exp((-x)**2 - y**2)
v, u = np.gradient(z, .2, .2)

# Create quiver figure
figure_2 = ff.create_quiver(x, y, u, v,
                            scale=.25,
                            arrow_scale=.4,
                            name='quiver',
                            line_width=1
                           )

# Add points to figure
figure_2.add_trace(go.Scatter(x=[-.7, .75], 
                              y=[0, 0],
                              mode='markers',
                              marker_size=12,
                              name='points'))

figure_2.show()


