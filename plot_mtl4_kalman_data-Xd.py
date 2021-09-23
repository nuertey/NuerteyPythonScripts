#***********************************************************************
# @file
#
# Plotting MTL4 Kalman Filter Data With Plotly
#
# @note None
#
# @warning  None
#
#  Created: September 16, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 8)

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

kalman_filter_data_df = pd.read_csv('TestCase_2-mtl4.csv', 
                                    sep='\t',  
                                    lineterminator='\n')

print('kalman_filter_data_df:')
print(kalman_filter_data_df)
print()

print('kalman_filter_data_df.info():')
print(kalman_filter_data_df.info())
print()

hist_data = [kalman_filter_data_df.z]
group_labels = ['Observations of Discrete LTI Projectile Motion, Measuring Position Only (z)'] # name of the dataset
#the_colors_list = list(range(0, len(kalman_filter_data_df.index)))

colors = ['rgb(0, 200, 200)']

figure_1 = ff.create_distplot(hist_data, 
                              group_labels,
                              curve_type='normal', # override default 'kde'
                              colors=colors
                             )
figure_1.update_layout(title_text='<b>Distplot - Observations of Discrete LTI Projectile Motion, Measuring Position Only For Kalman 3D</b>')
figure_1.show()

figure_2 = go.Figure()

figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
                              y=kalman_filter_data_df.z,
                              mode='markers',
                              name='Noisy Measurements (z)')
                  )

figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
                              y=kalman_filter_data_df.xhat_x,
                              mode='lines+markers',
                              name='<i>A Posteriori</i> Estimate (xhat_x)')
                  )
figure_2.update_xaxes(title_text='Iteration Step')
figure_2.update_yaxes(title_text='Voltage Value')
figure_2.update_layout(title_text='<b>Kalman Filter 3D: Estimate vs. Iteration Step</b>')
figure_2.show()

figure_3 = go.Figure(data=[go.Scatter3d(
    x=kalman_filter_data_df.xhat_x,
    y=kalman_filter_data_df.xhat_y,
    z=kalman_filter_data_df.xhat_z,
    mode='markers',
    marker=dict(
        size=12,
        color=kalman_filter_data_df.xhat_x, # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])

# tight layout
#figure_3.update_layout(margin=dict(l=0, r=0, b=0, t=0))
figure_3.show()

figure_4 = go.Figure()

figure_4.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector.iloc[1:], 
                              y=kalman_filter_data_df.P.iloc[1:],
                              mode='lines+markers',
                              name='<i>A Posteriori</i> Error Estimate (P)')
                  )
figure_4.update_xaxes(range=[0, len(kalman_filter_data_df.index)])
figure_4.update_xaxes(title_text='Iteration Step')
figure_4.update_yaxes(title_text='Voltage<sup>2</sup>')
figure_4.update_layout(title_text='<b>Kalman Filter 3D - Estimated <i>A Posteriori</i> Error vs. Iteration Step</b>')
figure_4.show()

figure_5 = go.Figure(data = go.Cone(x=kalman_filter_data_df.xhat_x,
                                    y=kalman_filter_data_df.xhat_y,
                                    z=kalman_filter_data_df.xhat_z,
                                    u=kalman_filter_data_df.xhat_x,
                                    v=kalman_filter_data_df.xhat_y,
                                    w=kalman_filter_data_df.xhat_z,
                                    colorscale='Blues',
                                    sizemode="absolute",
                                    sizeref=40               
                                    )
                     )

#figure_5.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=0.8),
#                       camera_eye=dict(x=1.2, y=1.2, z=0.6))
#                      )

figure_5.show()
