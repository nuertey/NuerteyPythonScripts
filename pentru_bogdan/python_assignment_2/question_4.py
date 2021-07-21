#!/usr/bin/env python

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn

from sklearn import manifold, decomposition
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.utils import check_random_state

from nose.tools import assert_equal, assert_is_instance, assert_true, assert_is_not
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal

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

print('df.info():')
print(df.info())
print()

print(df)
print()

# Dimension of the embedded space must be lower than 4.
n_components = 2 

# The learning rate for t-SNE is usually in the range [10.0, 1000.0]. If
# the learning rate is too high, the data may look like a ‘ball’ with any
# point approximately equidistant from its nearest neighbours. If the 
# learning rate is too low, most points may look compressed in a dense 
# cloud with few outliers. If the cost function gets stuck in a bad local
# minimum increasing the learning rate may help.
learning_rate = 100

n_points = df.shape[0]

# init{‘random’, ‘pca’} 
#
# PCA initialization cannot be used with precomputed distances and is
# usually more globally stable than random initialization.
model = manifold.TSNE(n_components=n_components, init='pca', random_state=check_random_state(0))
df_embedded = model.fit_transform(df)

print(df_embedded.shape)
print()

print(df_embedded)
print()

xs = df_embedded[:, 0]
ys = df_embedded[:, 1]

sns.palplot(sns.color_palette("muted"))

color_labels = set(df.index)
#color_labels = df.index.unique()

print(color_labels)
print()

print(len(color_labels))
print()

# List of colors in the color palettes
rgb_values = sns.color_palette("Set2", len(color_labels))

# Map aircraft to the colors
color_map = dict(zip(color_labels, rgb_values))

# Finally use the mapped values
figure6, ax = plt.subplots(figsize=(10,6))

ax.set_title('Manifold Learning With t-distributed Stochastic Neighbor Embedding')
ax.set_ylabel('df_embedded[:, 0]')
ax.set_xlabel('df_embedded[:, 1]')
#plt.scatter(xs, ys, c=df.index.map(color_map))
plt.scatter(xs, ys, c=xs)

plt.show()

# ----------------------------------------------------------------------
# PCA
#
# Projection onto the first 2 principal components
# ----------------------------------------------------------------------
df_pca = decomposition.PCA(n_components=n_components).fit_transform(df)

print(df_pca.shape)
print()

print(df_pca)
print()

xs_pca = df_pca[:, 0]
ys_pca = df_pca[:, 1]

figure7, ax = plt.subplots(figsize=(10,6))

ax.set_title('Manifold Learning With t-distributed Stochastic Neighbor Embedding')
ax.set_ylabel('df_pca[:, 0]')
ax.set_xlabel('df_pca[:, 1]')

plt.scatter(xs_pca, ys_pca, c=xs)

plt.show()

# ----------------------------------------------------------------------
# Bogdan: I archived the plot above as nuertey_figure_6.png. So at this
# juncture, as your professor put it, "[now]... compare/discuss the results
# with PCA [previous questions' answer]. Please submit your code [above]
# and output [nuertey_figure_6.png and console output resulting from
# "print(df_embedded)"; line 67 above], and write down 3-4 sentences that
# you observed from the results."
# ----------------------------------------------------------------------
