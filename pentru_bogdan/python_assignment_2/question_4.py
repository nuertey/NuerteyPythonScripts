#!/usr/bin/env python

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn import manifold
from sklearn.manifold import TSNE

from nose.tools import assert_equal, assert_is_instance, assert_true, assert_is_not
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal

# Next line to silence pyflakes. This import is needed.
Axes3D

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# ----------------------------------------------------------------------
# t-distributed Stochastic Neighbor Embedding.
# 
# t-SNE [1] is a tool to visualize high-dimensional data. It converts similarities between data points to joint probabilities and tries to minimize the Kullback-Leibler divergence between the joint probabilities of the low-dimensional embedding and the high-dimensional data. t-SNE has a cost function that is not convex, i.e. with different initializations we can get different results.
# 
# It is highly recommended to use another dimensionality reduction method (e.g. PCA for dense data or TruncatedSVD for sparse data) to reduce the number of dimensions to a reasonable amount (e.g. 50) if the number of features is very high. This will suppress some noise and speed up the computation of pairwise distances between samples.
# 
# Reference: https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
# ----------------------------------------------------------------------

# Problem 4
# 
# Apply t-SNE reduction to delta.csv file and compare/discuss the results with PCA.

df = pd.read_csv('delta.csv', index_col='Aircraft')

n_components = 3
n_points = df.shape[0]

# Create figure
fig = plt.figure(figsize=(15, 8))
fig.suptitle("Manifold Learning with %i points"  % (n_points), fontsize=14)

# Add 3d scatter plot
ax = fig.add_subplot(2, 1, 1, projection='3d')
ax.scatter(df[:, 0], df[:, 1], df[:, 2], c=color, cmap=plt.cm.Spectral)
ax.view_init(4, -72)

t_SNE = TSNE(n_components=n_components, init='pca', random_state=0)
df_embedded = t_SNE.fit_transform(df)

print(df_embedded.shape)
print()

print(df_embedded)
print()

ax = fig.add_subplot(2, 1, 2)
ax.scatter(df_embedded[:, 0], df_embedded[:, 1], df_embedded[:, 1], c=color, cmap=plt.cm.Spectral)
ax.set_title("t-distributed Stochastic Neighbor Embedding")
ax.xaxis.set_major_formatter(NullFormatter())
ax.yaxis.set_major_formatter(NullFormatter())
ax.axis('tight')

plt.show()
