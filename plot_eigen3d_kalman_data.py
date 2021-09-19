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

kalman_filter_data_df = pd.read_csv('TestCase_2.csv', 
                                    sep='\t',  
                                    lineterminator='\n')

print('kalman_filter_data_df:')
print(kalman_filter_data_df)
print()

print('kalman_filter_data_df.info():')
print(kalman_filter_data_df.info())
print()

#hist_data = [kalman_filter_data_df.z]
#group_labels = ['Random Normal Observations (z)'] # name of the dataset
##the_colors_list = list(range(0, len(kalman_filter_data_df.index)))
#
#colors = ['rgb(0, 200, 200)']
#
#figure_1 = ff.create_distplot(hist_data, 
#                              group_labels,
#                              curve_type='normal', # override default 'kde'
#                              colors=colors
#                             )
#figure_1.update_layout(title_text='<b>Distplot with Randutils Normal Distribution</b>')
#figure_1.show()
#
#figure_2 = go.Figure()
#
#figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
#                              y=kalman_filter_data_df.z,
#                              mode='markers',
#                              name='Noisy Measurements (z)')
#                  )
#figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
#                              y=kalman_filter_data_df.x_vector,
#                              mode='lines',
#                              name='Mean of \'Truth Value\' (x)')
#                  )
#figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
#                              y=kalman_filter_data_df.xhat_x,
#                              mode='lines+markers',
#                              name='<i>A Posteriori</i> Estimate (xhat_x)')
#                  )
#figure_2.update_xaxes(title_text='Iteration Step')
#figure_2.update_yaxes(title_text='Voltage Value')
#figure_2.update_layout(title_text='<b>Kalman Filter: Estimate vs. Iteration Step</b>')
#figure_2.show()
#
#figure_3 = go.Figure()
#
#figure_3.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector.iloc[1:], 
#                              y=kalman_filter_data_df.P.iloc[1:],
#                              mode='lines+markers',
#                              name='<i>A Posteriori</i> Error Estimate (P)')
#                  )
#figure_3.update_xaxes(range=[0, len(kalman_filter_data_df.index)])
#figure_3.update_xaxes(title_text='Iteration Step')
#figure_3.update_yaxes(title_text='Voltage<sup>2</sup>')
#figure_3.update_layout(title_text='<b>Estimated <i>A Posteriori</i> Error vs. Iteration Step</b>')
#figure_3.show()
#
