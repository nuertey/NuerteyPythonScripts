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
import plotly.graph_objects as go

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

print('edgelist_graph_dataframe.edges():')
print(edgelist_graph_dataframe.edges())
print()

# ======================================================================
# Begin your code here:
# ======================================================================

# Simpler plot...
nx.draw(edgelist_graph_dataframe, with_labels=True)
plt.show()


# More complicated plotly plot that I still need to debug tomorrow...
pos=nx.fruchterman_reingold_layout(edgelist_graph_dataframe)

# Create Edges
#
# Add edges as disconnected lines in a single trace and nodes as a scatter trace

edge_x = []
edge_y = []
for edge in edgelist_graph_dataframe.edges():
    x0, y0 = edgelist_graph_dataframe.nodes[edge[0]]['pos']
    x1, y1 = edgelist_graph_dataframe.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')
    
node_x = []
node_y = []
for node in edgelist_graph_dataframe.nodes():
    x, y = edgelist_graph_dataframe.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)    

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

# Color node points by the number of connections.
#
# Another option would be to size points by the number of connections i.e. node_trace.marker.size = node_adjacencies

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(edgelist_graph_dataframe.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

# Create Network Graph:
figure_2 = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Assignment 4: Data Mining Principles - Airlines Data Network Graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
figure_2.show()



# ======================================================================
# End your code here:
# ======================================================================
