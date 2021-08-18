# empet
# May '20
# 
# Hi @Natasha,
# 
# Plotly associates a text to a position of coordinates (x, y). An edge is not defined by a unique point to assign it a text.
# In order to display the edge weights you can define one more scatter trace, of mode='text', and its x, y lists are the middle point coordinates of the edges.
# For your example the marker colorscale and colorbar in the node_trace definition should be removed, because marker color is not defined as a numerical list (it is empty).
# 
# This is the code that displays the edge weights. I defined synthetical weights because your etext is an empty list.

#!/usr/bin/env python

import numpy as np
import networkx as nx
import plotly.graph_objects as go
from collections import OrderedDict


def get_edge_trace(G):
    edge_x = []
    edge_y = []

    etext = [f'weight{w}' for w in list(nx.get_edge_attributes(G, 'diameter').values())]#THIS list is empty for your data
    xtext=[]
    ytext=[]
    for edge in G.edges():

        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        xtext.append((x0+x1)/2)
        ytext.append((y0+y1)/2)
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        mode='lines'
    )
    eweights_trace = go.Scatter(x=xtext,y= ytext, mode='text',
                              marker_size=0.5,
                              text=[0.45, 0.7, 0.34],
                              textposition='top center',
                              hovertemplate='weight: %{text}<extra></extra>')
    return edge_trace, eweights_trace


def get_node_trace(G):
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker_size=12,
        #hoverinfo='text', #THIS LINE HAS NO SENSE BECAUSE text WAS NOT DEFINED
        marker_color='RoyalBlue',
        )

    return node_trace


if __name__ == '__main__':

    tail = [1, 2, 3]
    head = [2, 3, 4]

    xpos = [0, 1, 2, 3]
    ypos = [0, 0, 0, 0]
    w = [1, 2, 3]
    xpos_ypos = [(x, y) for x, y in zip(xpos, ypos)]

    ed_ls = [(x, y) for x, y in zip(tail, head)]
    G = nx.Graph()
    G.add_edges_from(ed_ls)


    pos = OrderedDict(zip(G.nodes, xpos_ypos))
    edge_w = OrderedDict(zip(G.edges, w))
    nx.set_node_attributes(G, pos, 'pos')
    nx.set_edge_attributes(G, edge_w, 'weight')

    # convert to plotly graph
    edge_trace, eweights_trace = get_edge_trace(G)
    node_trace = get_node_trace(G)

    fig = go.Figure(data=[edge_trace, node_trace,eweights_trace ],
                    layout=go.Layout(
                        title='<br>Network graph made with Python',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis_visible=False,
                        yaxis_visible=False)
                    )
    fig.show()
