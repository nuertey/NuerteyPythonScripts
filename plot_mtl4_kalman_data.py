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

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

kalman_filter_data_df = pd.read_csv('kalman_filter_output.csv', 
                                    #sep='\t',  
                                    lineterminator='\n')

print('kalman_filter_data_df:')
print(kalman_filter_data_df)
print()

print('kalman_filter_data_df.info():')
print(kalman_filter_data_df.info())
print()

hist_data = [kalman_filter_data_df.z]
group_labels = ['distplot'] # name of the dataset
the_colors_list = list(range(0, len(kalman_filter_data_df.index)))

figure_1 = ff.create_distplot(hist_data, 
                              group_labels
                             )
figure_1.show()
