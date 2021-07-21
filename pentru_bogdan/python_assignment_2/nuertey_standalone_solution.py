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
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('TkAgg')
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

    print('pca.components_:')    
    print(pca.components_)
    print()

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

# Bogdan: Call your function on the original DataFrame with the requisite
# input arguments :
pca_naive = fit_pca(df, n_components=df.shape[1])
    
assert_is_instance(pca_naive, PCA)
assert_almost_equal(pca_naive.explained_variance_ratio_.sum(), 1.0, 3)
assert_equal(pca_naive.n_components_, df.shape[1])
assert_equal(pca_naive.whiten, False)

def plot_naive_variance(pca):
    '''
    Plots the variance explained by each of the principal components.
    Attributes are not scaled, hence a naive approach.
    
    Parameters
    ----------
    pca: An sklearn.decomposition.pca.PCA instance.
    
    Returns
    -------
    A matplotlib.Axes instance.
    '''
    
    # YOUR CODE HERE
    figure2, ax = plt.subplots()
    ax.plot(list(range(pca.n_components_)), pca.explained_variance_ratio_)
    
    ax.set(xlabel='Dimension #', 
           ylabel='Explained Variance Ratio',
           title='Fraction of Explained Variance')
    
    plt.show() 

    return ax
    
naive_var = plot_naive_variance(pca_naive)

assert_is_instance(naive_var, mpl.axes.Axes)
assert_equal(len(naive_var.lines), 1)

assert_is_not(len(naive_var.title.get_text()), 0,
    msg="Your plot doesn't have a title.")
assert_is_not(naive_var.xaxis.get_label_text(), '',
    msg="Change the x-axis label to something more descriptive.")
assert_is_not(naive_var.yaxis.get_label_text(), '',
    msg="Change the y-axis label to something more descriptive.")

xdata, ydata = naive_var.lines[0].get_xydata().T
assert_array_equal(xdata, list(range(df.shape[1])))
assert_array_almost_equal(ydata, pca_naive.explained_variance_ratio_)

abs_val = np.abs(pca_naive.components_[0])
max_pos = abs_val.argmax()
max_val = abs_val.max()

print('"{0}" accounts for {1:0.3f} % of the variance.'.format(df.columns[max_pos], max_val))
print()
    
# Please write a function named standardize() where StandardScaler 
# function of sklearn will be used to scale each feature so that they 
# have zero mean and unit variance.
def standardize(df):
    '''
    Uses sklearn.preprocessing.StandardScaler to make each features look like
    a Gaussian with zero mean and unit variance.
    
    Parameters
    ----------
    df: A pandas.DataFrame
    
    Returns
    -------
    A numpy array.
    '''
    
    # YOUR CODE HERE
    scaler = StandardScaler()
    
    # Bogdan: Debug prints (commented out for now) and detailed method/steps
    # (also commented out for now) to encourage learning follows..., and
    # then subsequently, that is followed by a 1-line shortcut method of
    # performing the standardizations:
    
    #print('sklearn Scaler type:')    
    #scaler = scaler.fit(df)
    #print(scaler)
    #print()

    #print('Computed mean from input DataFrame to be used for later scaling:')
    #print(scaler.mean_)
    #print()
    
    #print('Computed variance from input DataFrame to be used for later scaling:')
    #print(scaler.var_)
    #print()

    # Perform standardization by centering and scaling:
    #scaled = scaler.transform(df)
    #print('Standardized and scaled DataFrame:')
    #print(scaled)
    #print()

    # Bogdan: As an alternative to all the above steps, you can simply do 
    # it in 1 line as a shortcut like so:
    scaled = StandardScaler().fit_transform(df)
    
    return scaled
    
scaled = standardize(df)

rng = np.random.RandomState(0)
n_samples, n_features = 4, 5

df_t1 = pd.DataFrame(
    rng.randn(n_samples, n_features),
    index=[i for i in 'abcd'],
    columns=[c for c  in 'abcde']
    )
df_t1.loc[:, 'a'] = 0.0  # make first feature zero

scaled_t1 = standardize(df_t1)

assert_is_not(df_t1, scaled_t1)
assert_is_instance(scaled_t1, np.ndarray)
assert_array_almost_equal(
    scaled_t1.mean(axis=0),
    n_features * [0.0] # scaled data should have mean zero
    ) 
assert_array_almost_equal(
    scaled_t1.std(axis=0),
    [0., 1., 1., 1., 1.] # unit variance except for 1st feature
    )
    
# we keep only 10 components
n_components = 10
pca = fit_pca(scaled, n_components=n_components)

# Let's take another look to the explained variance of the first 10 
# principal components from the scaled data.
def plot_scaled_variance(pca):
    '''
    Plots the variance explained by each of the principal components.
    Features are scaled with sklearn.StandardScaler.
    
    Parameters
    ----------
    pca: An sklearn.decomposition.pca.PCA instance.
    
    Returns
    -------
    A matplotlib.Axes instance.
    '''
    
    # YOUR CODE HERE
    figure3, ax = plt.subplots()
    ax.plot(list(range(pca.n_components_)), pca.explained_variance_ratio_)
    
    ax.set(xlabel='Dimension #', 
           ylabel='Explained Variance Ratio',
           title='Fraction of Explained Variance')
    
    plt.show() 
    
    return ax
    
ax = plot_scaled_variance(pca)

assert_is_instance(ax, mpl.axes.Axes)
assert_equal(len(ax.lines), 1)

assert_is_not(len(ax.title.get_text()), 0, msg="Your plot doesn't have a title.")
assert_is_not(ax.xaxis.get_label_text(), '', msg="Change the x-axis label to something more descriptive.")
assert_is_not(ax.yaxis.get_label_text(), '', msg="Change the y-axis label to something more descriptive.")

xdata, ydata = ax.lines[0].get_xydata().T
assert_array_equal(xdata, list(range(n_components)))
assert_array_almost_equal(ydata, pca.explained_variance_ratio_)

# Write a function named reduce() that takes a PCA model (that is already
# trained on array) and a Numpy array, and applies dimensional reduction
# on the array.
def reduce(pca, array):
    '''
    Applies the `pca` model on array.
    
    Parameters
    ----------
    pca: An sklearn.decomposition.PCA instance.
    
    Returns
    -------
    A Numpy array
    '''
    
    # YOUR CODE HERE
    reduced = pca.fit_transform(array)

    return reduced
    
reduced = reduce(pca, scaled)

assert_is_instance(reduced, np.ndarray)
assert_array_almost_equal(reduced, pca.fit_transform(scaled))

# Save the reduced data to the same directory of your notebook  as 'delta_reeuced.npy' that we will use later on
np.save('delta_reduced.npy', reduced)


