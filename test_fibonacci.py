#***********************************************************************
# @file
#
# Testing the plotting of a Fibonacci sequence with Plotly
#
# @note None
#
# @warning  None
#
#  Created: August 24, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import pandas as pd
import plotly.graph_objects as go

import plotly.express as px

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

input_x = list(range(0, 42))
output_y = []

def fibonacci_sequence():
    # In mathematics, the Fibonacci numbers, commonly denoted Fn, form a
    # sequence, called the Fibonacci sequence, such that each number is 
    # the sum of the two preceding ones, starting from 0 and 1. That is:
    #
    # F0 = 0, F1 = 1
    a,b = 0,1
    while True:
        yield a
        # and Fn = Fn-1 + Fn-2, for n > 1:
        a,b = b, a+b

generator = fibonacci_sequence()

for i in input_x:
    output_y.append(next(generator))
    
print('input_x:')
print(input_x)
print()

print('output_y:')
print(output_y)
print()

# Creating a DataFrame for easier manipulation, analysis and processing:
fibonacci_data_df = pd.DataFrame(
    {'input_x': input_x,
     'output_y': output_y
    })

fig = px.scatter(fibonacci_data_df, x="input_x", y="output_y")
fig.show()

# ======================================================================

#this describes the direction. Every iteration turns 90 degrees
vectors = [(1,1), (-1,1), (-1,-1), (1,-1)]
angles = [270, 0, 90, 180]

#box_colors = ["grey"]
#uncomment if you like it colorful
box_colors = ["red", "green", "blue"]

squares = [{"origin":(0,0), "length":1},
           {"origin":(1,1), "length":1, "arc_origin":(0,1)},
           {"origin":(0,2), "length":2, "arc_origin":(0,0)},
           {"origin":(-2,0), "length":3, "arc_origin":(1,0)},
           {"origin":(1,-3), "length":5, "arc_origin":(1,2)},
           {"origin":(6,2), "length":8, "arc_origin":(-2,2)}]

for i, sq in enumerate(squares):
    if True:
        #draw the square
        #doc: http://matplotlib.org/api/artist_api.html#matplotlib.patches.Rectangle
        plt.gca().add_patch(Rectangle(
            sq["origin"], 
            sq["length"]*vectors[i%len(vectors)][0],
            sq["length"]*vectors[i%len(vectors)][1], 
            facecolor=box_colors[i%len(box_colors)]
            ))
    if "arc_origin" in sq:
        #draw the arc
        #doc: http://matplotlib.org/api/artist_api.html#matplotlib.patches.Arc
        plt.gca().add_patch(Arc(
            sq["arc_origin"], #origin for the arc
            sq["length"]*2, #width
            sq["length"]*2, #length
            angle = angles[i%len(angles)], #rotation angle
            theta1 = 0, #start angle
            theta2 = 90, #end angle
            lw = 2
            ))
            
plt.axis([-3.5, 11, -3.5, 11])          
plt.show()
