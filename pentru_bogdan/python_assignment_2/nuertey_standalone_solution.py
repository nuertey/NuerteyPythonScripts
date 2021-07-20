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
import matplotlib
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

### This is the unittest cell, please just run this cell without any modification once you generated "pg" above

cols = ['Cruising Speed (mph)', 'Range (miles)', 'Engines',
        'Wingspan (ft)', 'Tail Height (ft)', 'Length (ft)']

assert_is_instance(pg.fig, plt.Figure)
assert_equal(set(pg.data.columns), set(cols))

for ax in pg.diag_axes:
    assert_equal(len(ax.patches), 10)

for i, j in zip(*np.triu_indices_from(pg.axes, 1)):
    ax = pg.axes[i, j]
    x_in = df[cols[j]]
    y_in = df[cols[i]]
    x_out, y_out = ax.collections[0].get_offsets().T
    assert_array_equal(x_in, x_out)
    assert_array_equal(y_in, y_out)

for i, j in zip(*np.tril_indices_from(pg.axes, -1)):
    ax = pg.axes[i, j]
    x_in = df[cols[j]]
    y_in = df[cols[i]]
    x_out, y_out = ax.collections[0].get_offsets().T
    assert_array_equal(x_in, x_out)
    assert_array_equal(y_in, y_out)

for i, j in zip(*np.diag_indices_from(pg.axes)):
    ax = pg.axes[i, j]
    assert_equal(len(ax.collections), 0)

# Apply PCA
#
# I assume we dont know anything about dimensionality reduction techniques
# and just naively apply principle components to the data.
#
# Write a function named fit_pca() that takes a pandas.DataFrame and uses
# sklearn.decomposition.PCA to fit a PCA model on all values of df.
def fit_pca(df, n_components):
    '''
    Uses sklearn.decomposition.PCA to fit a PCA model on "df".

    Parameters
    ----------
    df: A pandas.DataFrame. Comes from delta.csv.
    n_components: An int. Number of principal components to keep.

    Returns
    -------
    An sklearn.decomposition.pca.PCA instance.
    '''

    # YOUR CODE HERE
    pca = PCA(n_components)
    pca.fit(df)

    print('pca.explained_variance_ratio_:')    
    print(pca.explained_variance_ratio_)
    print()

    print('pca.singular_values_:')       
    print(pca.singular_values_)
    print()

    return pca

# Bogdan: Visual verification of function input arguments, and for 
# learning purposes:
print('Number Of Rows In Overall DataFrame:')
print(df.shape[0])
print()

print('Number Of Columns In Overall DataFrame:')
print(df.shape[1])
print()

print('Number Of Columns In Overall DataFrame (Alternate Method):')
print(len(df.columns))
print()

pca_naive = fit_pca(df, n_components=df.shape[1])
    
assert_is_instance(pca_naive, PCA)
assert_almost_equal(pca_naive.explained_variance_ratio_.sum(), 1.0, 3)
assert_equal(pca_naive.n_components_, df.shape[1])
assert_equal(pca_naive.whiten, False)
