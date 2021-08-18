# Reference: https://community.plotly.com/t/displaying-edge-labels-of-networkx-graph-in-plotly/39113/8
#
# empet
# May '20
# 
# @Natasha
# Meanwhile I tried to find out why your Plotly figure was different from that drawn with networkx. I noticed that you labeled the nodes in the Excel file starting with 1, but Plotly code supposed that nodes are labeled from 0. So there was a nonconcordance between node labels and edge end labels. Moreover, I’m wondering why you defined a networkx graph as long as your Excel file contained all information to draw a Plotly network.
# 
# Only when you cannot provide the node positions you have to define first a networkx graph and set a graph layout to place the nodes in the plane, i.e. to assign them a position (expressed by node coordinates).
# 
# Here is a new code that resulted by modifying data from your Excel file to get the right Plotly network and avoiding the use of networkx. Moreover I assigned the node indices as labels:

#!/usr/bin/env python

import numpy as np
import pandas as pd
import plotly.graph_objects as go

def get_plotly_data(E, coords):

   # E is the list of tuples representing the graph edges
    # coords is the list of node coordinates 
    N = len(coords)
    Xnodes = [coords[k][0] for k in range(N)] # x-coordinates of nodes
    Ynodes = [coords[k][1] for k in range(N)] # y-coordnates of nodes

    Xedges = []
    Yedges = []
    Xweights = []
    Yweights = []
    for e in E:
        x0, x1 = coords[e[0]][0], coords[e[1]][0]
        y0, y1 = coords[e[0]][1], coords[e[1]][1]
        Xedges.extend([x0, x1, None])
        Yedges.extend([y0, y1, None])
        Xweights.append((x0+x1)/2)
        Yweights.append((y0+y1)/2)
    return Xnodes, Ynodes, Xedges, Yedges, Xweights, Yweights 

def get_node_trace(x, y, labels, marker_size=10, marker_color='RoyalBlue', 
                   line_color='rgb(50,50,50)', line_width=0.5):
    return go.Scatter(
                x=x,
                y=y,
                mode='markers',
                marker=dict(
                            size=marker_size, 
                            color=marker_color,
                            line=dict(color=line_color, width=line_width)
                             ),
            text=labels,
            hoverinfo='text'
               )

def get_edge_trace(x, y, line_color='#888', line_width=1):
    return go.Scatter(
                x=x,
                y=y,
                mode='lines',
                line_color=line_color,
                line_width=line_width,
                hoverinfo='none'
               )

df = pd.read_excel(open("file.xlsx", 'rb'), sheet_name=0, index=False)

#df.columns

I = np.where(np.isnan(df['node'].values))[0]
print(I)

#Reindex the nodes, tail and head, starting with  0

t = df['t'].values-1
h = df['h'].values-1
node= df['node'].values.astype(int)[:I[0]]-1

coords = [(xc,yc ) for xc, yc in zip(df['x'][:I[0]], df['y'][:I[0]])]
E = list(zip(t, h)) #the graph edges
print(E[:5])

Xn, Yn, Xe, Ye, Xw, Yw = get_plotly_data(E, coords)

node_trace = get_edge_trace(Xe, Ye)
edge_trace = get_node_trace(Xn, Yn, node)
eweights_trace = go.Scatter(x=Xw, y= Yw, 
                            mode='markers',
                            marker_size=0.5,
                            text=df['d'][:I[0]],
                            hovertemplate='weight: %{text}<extra></extra>')

layout=go.Layout(title_text='Your title',
            title_x=0.5,
                 height=800,
            showlegend=False,
            xaxis_visible=False,
            yaxis_visible=False,   
            margin=dict(b=20, l=5, r=5, t=80),     
            hovermode='closest')
fig = go.Figure(data=[edge_trace, node_trace, eweights_trace], layout=layout)
