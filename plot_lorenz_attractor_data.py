#***********************************************************************
# @file
#
# Plotting Lorenz Attractor Data With Plotly
#
# @note None
#
# @warning  None
#
#  Created: August 25, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

lorenz_attractor_data_df = pd.read_csv('lorenz_output.csv', 
                                       sep='\t',  
                                       lineterminator='\n', 
                                       names=["time", "x", "y", "z"])

print('lorenz_attractor_data_df.shape:')
print(lorenz_attractor_data_df.shape)
print()

print('lorenz_attractor_data_df.head():')
print(lorenz_attractor_data_df.head())
print()

print('lorenz_attractor_data_df.info():')
print(lorenz_attractor_data_df.info())
print()

figure_1 = go.Figure(data=go.Scatter3d(
    x=lorenz_attractor_data_df['x'], y=lorenz_attractor_data_df['y'], z=lorenz_attractor_data_df['z'],
    marker=dict(
        size=4,
        color=lorenz_attractor_data_df['time'],
        colorscale='Viridis',
    ),
    line=dict(
        color='darkblue',
        width=2
    )
))

figure_1.update_layout(
    width=983,
    height=700,
    autosize=True,
    scene=dict(
        camera=dict(
            up=dict(
                x=0,
                y=0,
                z=1
            ),
            eye=dict(
                x=0,
                y=1.0707,
                z=1,
            )
        ),
        aspectratio = dict( x=1, y=1, z=0.7 ),
        aspectmode = 'manual'
    ),
)

figure_1.show()

# ======================================================================

fpu_data_df = pd.read_csv('fpu_output.csv', 
                                       sep='\t',  
                                       lineterminator='\n', 
                                       names=["t", "i", "q", "p", "energy"])

print('fpu_data_df.shape:')
print(fpu_data_df.shape)
print()

print('fpu_data_df.head():')
print(fpu_data_df.head())
print()

print('fpu_data_df.info():')
print(fpu_data_df.info())
print()

figure_2 = go.Figure(data=go.Scatter3d(
    x=fpu_data_df['q'], y=fpu_data_df['p'], z=fpu_data_df['energy'],
    marker=dict(
        size=4,
        color=fpu_data_df['t'],
        colorscale='Viridis',
    ),
    line=dict(
        color='darkblue',
        width=2
    )
))

figure_2.update_layout(
    width=983,
    height=700,
    autosize=True,
    scene=dict(
        camera=dict(
            up=dict(
                x=0,
                y=0,
                z=1
            ),
            eye=dict(
                x=0,
                y=1.0707,
                z=1,
            )
        ),
        aspectratio = dict( x=1, y=1, z=0.7 ),
        aspectmode = 'manual'
    ),
)

figure_2.show()

# ======================================================================

harmonic_data_df = pd.read_csv('harmonic_output.csv', 
                                       sep='\t',  
                                       lineterminator='\n', 
                                       names=["times", "x_vec_0", "x_vec_1"])

print('harmonic_data_df.shape:')
print(harmonic_data_df.shape)
print()

print('harmonic_data_df.head():')
print(harmonic_data_df.head())
print()

print('harmonic_data_df.info():')
print(harmonic_data_df.info())
print()

my_colors = list(range(0, len(harmonic_data_df.index)))
print('my_colors:')
print(my_colors)
print()

figure_3 = go.Figure(data=go.Scatter3d(
    x=harmonic_data_df['times'], y=harmonic_data_df['x_vec_0'], z=harmonic_data_df['x_vec_1'],
    marker=dict(
        size=4,
        #color='darkorange',
        color=my_colors,
        colorscale='Viridis',
    ),
    line=dict(
        color='darkblue',
        width=2
    )
))

figure_3.update_layout(
    width=983,
    height=700,
    autosize=True,
    scene=dict(
        camera=dict(
            up=dict(
                x=0,
                y=0,
                z=1
            ),
            eye=dict(
                x=0,
                y=1.0707,
                z=1,
            )
        ),
        aspectratio = dict( x=1, y=1, z=0.7 ),
        aspectmode = 'manual'
    ),
)

figure_3.show()
