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

# Since the name of the method networkx.algorithms.clique.find_cliques
# can seem confusing, even though it actually does return the maximal
# cliques, let us rename it so that its name itself reflects what it is.
from networkx.algorithms.clique import find_cliques as maximal_cliques

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

# More complicated plotly plot...
pos=nx.fruchterman_reingold_layout(edgelist_graph_dataframe)

print('pos:')
print(pos)
print()

# Create Edges
#
# Add edges as disconnected lines in a single trace and nodes as a scatter trace
edge_x = []
edge_y = []
for edge in edgelist_graph_dataframe.edges():
    x0 = pos[edge[0]][0]
    y0 = pos[edge[0]][1]
    x1 = pos[edge[1]][0]
    y1 = pos[edge[1]][1]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

#print('edge_x:')
#print(edge_x)
#print()

#print('edge_y:')
#print(edge_y)
#print()

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')
    
node_x = []
node_y = []
for node in edgelist_graph_dataframe.nodes():
    x = pos[node][0]
    y = pos[node][1]
    node_x.append(x)
    node_y.append(y)    

#print('node_x:')
#print(node_x)
#print()

#print('node_y:')
#print(node_y)
#print()

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
# Another option would be to size points by the number of connections i.e.
# node_trace.marker.size = node_adjacencies

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

nx.algorithms.degree_centrality(edgelist_graph_dataframe) # Notice the 3 airports from which all of our 100 rows of data originates
# Calculate average edge density of the Graph

# your code is here

# ======================================================================
# Begin your code here:
# ======================================================================

print("Name: %s" % edgelist_graph_dataframe.name)
print("Type: %s" % type(edgelist_graph_dataframe).__name__)
print("Frozen: %s" % nx.is_frozen(edgelist_graph_dataframe))
print()
print("Density: %.17f" % nx.density(edgelist_graph_dataframe))
print()
print("Nodes: %s" % edgelist_graph_dataframe.number_of_nodes())
print("Edges: %s" % edgelist_graph_dataframe.number_of_edges())

# ======================================================================
# End your code here:
# ======================================================================

nx.average_shortest_path_length(edgelist_graph_dataframe) # Average shortest path length for ALL paths in the Graph

nx.average_degree_connectivity(edgelist_graph_dataframe) # For a node of degree k - What is the average of its neighbours' degree?

# Let us find all the paths available
for path in nx.all_simple_paths(edgelist_graph_dataframe, source='JAX', target='DFW'):
    print(path)

# Let us find the dijkstra path from JAX to DFW.
# You can read more in-depth on how dijkstra works from this resource - https://courses.csail.mit.edu/6.006/fall11/lectures/lecture16.pdf
dijpath = nx.dijkstra_path(edgelist_graph_dataframe, source='JAX', target='DFW')

print()
print('Dijkstra path from JAX to DFW:')
print(dijpath)

# Let us try to find the dijkstra path weighted by airtime (approximate case)
shortpath = nx.dijkstra_path(edgelist_graph_dataframe, source='JAX', target='DFW', weight='air_time')

print()
print('Dijkstra path from JAX to DFW approximately weighted by airtime:')
print(shortpath)

# ======================================================================
# Further Answers to Questions Here Mr B:
# ======================================================================

# How many maximal cliques we can spot in this airline network? (20 Points)

the_maximal_cliques_subgraph = maximal_cliques(edgelist_graph_dataframe)

# "To obtain a list of all maximal cliques, use list(find_cliques(G)). 
# However, be aware that in the worst-case, the length of this list can 
# be exponential in the number of nodes in the graph. This function avoids
# storing all cliques in memory by only keeping current candidate node 
# lists in memory during its search.
#
# This implementation is based on the algorithm published by Bron and 
# Kerbosch (1973) [1], as adapted by Tomita, Tanaka and Takahashi (2006)
#  [2] and discussed in Cazals and Karande (2008) [3]. It essentially 
# unrolls the recursion used in the references to avoid issues of recursion
# stack depth (for a recursive implementation, see find_cliques_recursive()).
#
# This algorithm ignores self-loops and parallel edges, since cliques are
# not conventionally defined with such edges."
#
# Reference: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html#networkx.algorithms.clique.find_cliques

the_maximal_cliques_list = list(the_maximal_cliques_subgraph)

print()
print("The Number of Maximal Cliques in this Airline Network is: %d" % len(the_maximal_cliques_list))
print()
