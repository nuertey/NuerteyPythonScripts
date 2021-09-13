#***********************************************************************
# @file
#
# Getting very familiar with plotly by assaying (trying) some plots. 
# Occupying oneself in productive pursuits and all...
#
# @note None
#
# @warning  None
#
#  Created: September 9, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cufflinks as cf

import plotly
import plotly.graph_objects as go
import plotly.express as px

from numpy import array
from matplotlib.pyplot import *
from nose.tools import assert_equal
from sklearn.datasets import load_iris, load_wine
from sklearn.preprocessing import MinMaxScaler

setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

matplotlib.use('TkAgg')

def version_to_int_list(version):
    return [int(s) for s in version.split('.')]

print('plotly.__version__:')
print(plotly.__version__)
print()

print('version_to_int_list(plotly.__version__):')
print(version_to_int_list(plotly.__version__))
print()

print('version_to_int_list(\'3.8.0\'):')
print(version_to_int_list('3.8.0'))
print()

# The comparison uses lexicographical ordering: first the first two items
# are compared, and if they differ this determines the outcome of the 
# comparison; if they are equal, the next two items are compared, and 
# so on, until either sequence is exhausted. Hence the pair of items at
# each index are compared in turn.
#
# A corollary of this is, two lists will only compare as equal if and only
# if they possess the same length and all pairs of items compare as equal.
#
# Note that the comparison of pairs will stop when either an unequal pair
# of items is found or--if the lists are of different lengths--the end of 
# the shorter list is reached.
assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'

print('cufflinks.__version__:')
print(cf.__version__)
print()

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may
# depend on the context. This is sometimes called chained assignment and
# should be avoided. See Returning a View versus Copy. [dataframe_loop_example.py]
pd.options.mode.chained_assignment = None

print("List of Cufflinks Themes: ", cf.getThemes())
print()

cf.set_config_file(theme='pearl', sharing='public', offline=True)

# To read native Excel files (.xls), ensure you install the following 
# a priori:
#
# pip install xlrd

# To read native Open Document Formatted spreadsheet files (.ods), 
# ensure you install the following a priori:
#
#pip install odfpy
dating_profiles_data_df = pd.read_excel("gender_ratio.ods", engine="odf")

# As whistespaces before (and after) column names are messing up the code
# below by it not locating specific columns unless with 'iloc' as used 
# below, strip the whitespaces before continuing:

# Option 1: Use the inplace=True argument to change the DataFrame in situ:
dating_profiles_data_df.rename(columns=lambda x: x.strip(), inplace=True)

# Option 2: Assign it back to your df variable:
#dating_profiles_data_df = dating_profiles_data_df.rename(columns=lambda x: x.strip())

print('dating_profiles_data_df.shape:')
print(dating_profiles_data_df.shape)
print()

print('dating_profiles_data_df:')
print(dating_profiles_data_df)
print()

print('dating_profiles_data_df.info():')
print(dating_profiles_data_df.info())
print()

#col_one_list = df['one'].tolist()
x1 = dating_profiles_data_df.iloc[:,0].to_numpy()
y1 = dating_profiles_data_df.iloc[:,3].to_numpy()

y2 = dating_profiles_data_df.iloc[:,1].to_numpy()

y3 = dating_profiles_data_df.iloc[:,2].to_numpy()

trace1 = go.Scatter(
    x=x1,
    y=y1
)
trace2 = go.Histogram(
    x=x1,
    y=y2
)
trace3 = go.Histogram(
    x=x1,
    y=y3
)

data = [trace1]#, trace2, trace3]

#layout = go.Layout(
#    yaxis=dict(
#        domain=[0, 0.33]
#    ),
#    legend=dict(
#        traceorder="reversed"
#    ),
#    yaxis2=dict(
#        domain=[0.33, 0.66]
#    ),
#    yaxis3=dict(
#        domain=[0.66, 1]
#    )
#)
figure_1 = go.Figure(data=data)#, layout=layout)

figure_1.add_trace(trace2)
figure_1.add_trace(trace3)

# Overlay both histograms
figure_1.update_layout(barmode='overlay')

# Reduce opacity to see both histograms
figure_1.update_traces(opacity=0.75)

figure_1.show()

figure_2 = go.Figure()
figure_2.add_trace(go.Histogram(x=y2))
figure_2.add_trace(go.Histogram(x=y3))

# Overlay both histograms
figure_2.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
figure_2.update_traces(opacity=0.75)
figure_2.show()

# ======================================================================
x0 = np.random.randn(500)
# Add 1 to shift the mean of the Gaussian distribution
x1 = np.random.randn(500) + 1

figure_3 = go.Figure()
figure_3.add_trace(go.Histogram(x=x0))
figure_3.add_trace(go.Histogram(x=x1))

# Overlay both histograms
figure_3.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
figure_3.update_traces(opacity=0.75)
figure_3.show()

# ======================================================================
# Now apply my new Plotly/cufflinks plotting knowledges...
# ======================================================================
df1 = dating_profiles_data_df[['Age', 'Male', 'Female']]

df1.iplot(kind="bar",
          sortbars=True,
          x="Age",
          xTitle="Age",
          yTitle="Population on Dating Sites", 
          title="Proportion of Male versus Female on Dating Sites by Age",
          theme="ggplot"
         )

dating_profiles_data_df.iplot(
          x="Age",
          y=["Male", "Female"],
          width=2.0,
          xTitle="Age",
          yTitle="Population on Dating Sites", 
          title="Proportion of Male versus Female on Dating Sites by Age",
          )

df1.iplot(kind="hist",
              #bins=50, 
              #colors=["red"],
              #x="Age",
              keys=["Male", "Female"],
              #dimensions=(600, 400),
              xTitle="Age",
              yTitle="Population on Dating Sites", 
              title="Proportion of Male versus Female on Dating Sites by Age - Histogram",
              )

# Create a ratio chart of Male and Female stats in the Dating data. 
df1.iplot(kind="ratio", 
               x="Age",
               keys=["Male", "Female",],
               title="Proportion of Male versus Female on Dating Sites by Age - Ratio Chart"
              )
