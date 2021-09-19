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

#kalman_filter_data_df = pd.read_csv('kalman_filter_output.csv', 
#                                    sep='\t',  
#                                    lineterminator='\n')

kalman_filter_data_df = pd.read_csv('TestCase_1.csv', 
                                    sep='\t',  
                                    lineterminator='\n')

print('kalman_filter_data_df:')
print(kalman_filter_data_df)
print()

print('kalman_filter_data_df.info():')
print(kalman_filter_data_df.info())
print()

hist_data = [kalman_filter_data_df.z]
group_labels = ['Random Normal Observations (z)'] # name of the dataset
#the_colors_list = list(range(0, len(kalman_filter_data_df.index)))

colors = ['rgb(0, 200, 200)']

figure_1 = ff.create_distplot(hist_data, 
                              group_labels,
                              curve_type='normal', # override default 'kde'
                              colors=colors
                             )
figure_1.update_layout(title_text='<b>Distplot with Randutils Normal Distribution</b>')
figure_1.show()

figure_2 = go.Figure()

figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
                              y=kalman_filter_data_df.z,
                              mode='markers',
                              name='Noisy Measurements (z)')
                  )
figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
                              y=kalman_filter_data_df.x_vector,
                              mode='lines',
                              name='Mean of \'Truth Value\' (x)')
                  )
figure_2.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector, 
                              y=kalman_filter_data_df.xhat_x,
                              mode='lines+markers',
                              name='<i>A Posteriori</i> Estimate (xhat_x)')
                  )
figure_2.update_xaxes(title_text='Iteration Step')
figure_2.update_yaxes(title_text='Voltage Value')
figure_2.update_layout(title_text='<b>Kalman Filter: Estimate vs. Iteration Step</b>')
figure_2.show()

figure_3 = go.Figure()

figure_3.add_trace(go.Scatter(x=kalman_filter_data_df.step_vector.iloc[1:], 
                              y=kalman_filter_data_df.P.iloc[1:],
                              mode='lines+markers',
                              name='<i>A Posteriori</i> Error Estimate (P)')
                  )
figure_3.update_xaxes(range=[0, len(kalman_filter_data_df.index)])
figure_3.update_xaxes(title_text='Iteration Step')
figure_3.update_yaxes(title_text='Voltage<sup>2</sup>')
figure_3.update_layout(title_text='<b>Estimated <i>A Posteriori</i> Error vs. Iteration Step</b>')
figure_3.show()

#-----------------------------------------------------------------------
# Debugging the plots; comparing mathplotlib to plotly
#-----------------------------------------------------------------------
#n_iter = 50
#x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
#
#plt.figure()
#plt.plot(kalman_filter_data_df.z, 'k+', label='noisy measurements (z)')
#plt.plot(kalman_filter_data_df.xhat, 'b-', label='a posteri estimate (xhat)')
#plt.axhline(x, color='g', label='truth value (x)')
#plt.legend()
#plt.title('Estimate vs. iteration step', fontweight='bold')
#plt.xlabel('Iteration')
#plt.ylabel('Voltage')
#
#plt.figure()
#valid_iter = range(1, n_iter) # Pminus not valid at step 0
#plt.plot(valid_iter, kalman_filter_data_df.Pminus[valid_iter], label='a priori error estimate (Pminus)')
#plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
#plt.xlabel('Iteration')
#plt.ylabel('$(Voltage)^2$')
#plt.setp(plt.gca(),'ylim', [0, .01])
#plt.show()

# ======================================================================
# Examples:
# ======================================================================
#import numpy as np
#
## Add histogram data
#x1 = np.random.randn(200)-2
#x2 = np.random.randn(200)
#x3 = np.random.randn(200)+2
#x4 = np.random.randn(200)+4
#
## Group data together
#hist_data = [x1, x2, x3, x4]
#
#group_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
#
## Create distplot with custom bin_size
#fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5, 1])
#fig.show()
