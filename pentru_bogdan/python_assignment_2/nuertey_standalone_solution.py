#***********************************************************************
# @file
#
# Assignment_2: Unsupervised Data Mining
#
# @note None
#
# @warning  None
#
#  Created: July 20, 2021
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

# Ensure to install these following packages before running 'standalone':
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import sklearn  # pip install sklearn
import pickle   # pip install pickle-mixin

from sklearn.preprocessing import StandardScaler
from sklearn.utils import check_random_state
from sklearn.decomposition import PCA

from nose.tools import assert_equal, assert_is_instance, assert_is_not # pip install nose
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
from pandas.util.testing import assert_frame_equal

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# ======================================================================
# Problem_1: Dimension Reduction
#
# With Problem_1, we aim to have a better understanding of dimension 
# reduction with PCA. We will use Delta Airline data. 
# ======================================================================

# Delta and other major airlines have data on all of their aircrafts on
# their website.
df = pd.read_csv('delta.csv', index_col='Aircraft')

print(df.head())
print()

# First, let's look at the attributes related to the aircraft physical 
# characteristics:
#
# Cruising Speed (mph) Range (miles) Engines Wingspan (ft) Tail Height 
# (ft) Length (ft) These six variables are about in the middle of the 
# data frame (and it's part of your task to figure out where they are 
# located).

# Bogdan: Here is where they are located:
#
# Index: 44 entries, Airbus A319 to MD-DC9-50
# Data columns (total 33 columns):
#  #   Column                    Non-Null Count  Dtype  
# ---  ------                    --------------  -----  
#  0   Seat Width (Club)         44 non-null     float64
#  ...
#  16  Cruising Speed (mph)      44 non-null     int64  
#  17  Range (miles)             44 non-null     int64  
#  18  Engines                   44 non-null     int64  
#  19  Wingspan (ft)             44 non-null     float64
#  20  Tail Height (ft)          44 non-null     float64
#  21  Length (ft)               44 non-null     float64
#  ... 
#  31  Eco Comfort               44 non-null     int64  
#  32  Economy                   44 non-null     int64  

print('df.info():')
print(df.info())
print()

# Bogdan: Form a new DataFrame for subsequent easier processing:
aircraft_physical_characteristics_df = df[['Cruising Speed (mph)', 
                                           'Range (miles)',
                                           'Engines',
                                           'Wingspan (ft)', 
                                           'Tail Height (ft)', 
                                           'Length (ft)']]

# Bogdan: Visual verification of new DataFrame:
print(aircraft_physical_characteristics_df)
print()

# Write a function named plot_pairgrid() that takes a pandas.DataFrame 
# and uses seaborn.PairGrid to visualize the attributes related to the 
# six physical characteristics listed above. The plots on the diagonal 
# should be histograms of corresponding attributes, and the off-diagonal
# should be scatter plots.
def plot_pairgrid(df):
    '''
    Uses seaborn.PairGrid to visualize the attributes related to the six physical characteristics.
    Diagonal plots are histograms. The off-diagonal plots are scatter plots.
    
    Parameters
    ----------
    df: A pandas.DataFrame. Comes from importing delta.csv.
    
    Returns
    -------
    A seaborn.axisgrid.PairGrid instance.
    '''
    
    # YOUR CODE HERE
    plt.style.use('seaborn') # pretty matplotlib plots
    ax = sns.PairGrid(df)
    
    # Bogdan: Ensure to plot a different function on the diagonal to 
    # show the univariate distribution of the variable in each column:
    ax.map_diag(plt.hist)
    ax.map_offdiag(plt.scatter);
    plt.show()
    
    return ax

# Bogdan: Call your function on your new DataFrame:
pg = plot_pairgrid(aircraft_physical_characteristics_df)
