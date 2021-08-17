#***********************************************************************
# @file
#
# Assignment 4: Data Mining Principles - Networks (or Graphs)
#
# @note None
#
# @warning  None
#
#  Created: August 16, 2021
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

airlines_graph_data = pd.read_csv('Airlines_graph.csv')

print('airlines_graph_data.shape:')
print(airlines_graph_data.shape)
print()

print('airlines_graph_data.head():')
print(airlines_graph_data.head())
print()

print('airlines_graph_data.info():')
print(airlines_graph_data.info())
print()

print('Complex Networks Python Package Version:')
print(nx.__version__)
print()

# Nuertey comment: Let us bypass the Python FutureWarnings that are 
# clouding the output by simply outputting several spaces before.
print('\n\n')

# converting sched_dep_time to 'std' - Scheduled time of departure
airlines_graph_data['std'] = airlines_graph_data.sched_dep_time.astype(str).str.replace('(\d{2}$)', '') + ':' + airlines_graph_data.sched_dep_time.astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

# converting sched_arr_time to 'sta' - Scheduled time of arrival
airlines_graph_data['sta'] = airlines_graph_data.sched_arr_time.astype(str).str.replace('(\d{2}$)', '') + ':' + airlines_graph_data.sched_arr_time.astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

# converting dep_time to 'atd' - Actual time of departure
airlines_graph_data['atd'] = airlines_graph_data.dep_time.fillna(0).astype(np.int64).astype(str).str.replace('(\d{2}$)', '') + ':' + airlines_graph_data.dep_time.fillna(0).astype(np.int64).astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

airlines_graph_data['ata'] = airlines_graph_data.arr_time.fillna(0).astype(np.int64).astype(str).str.replace('(\d{2}$)', '') + ':' + airlines_graph_data.arr_time.fillna(0).astype(np.int64).astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

airlines_graph_data['date'] = pd.to_datetime(airlines_graph_data[['year', 'month', 'day']])

# finally we drop the columns we don't need
airlines_graph_data = airlines_graph_data.drop(columns = ['year', 'month', 'day'])

edgelist_graph_dataframe = nx.from_pandas_edgelist(airlines_graph_data, source='origin', target='dest', edge_attr=True,)

# Nuertey comment: Let us bypass the Python FutureWarnings that are 
# clouding the output by simply outputting several spaces aft.
print('\n\n')

print('edgelist_graph_dataframe.nodes():')
print(edgelist_graph_dataframe.nodes())
print()

