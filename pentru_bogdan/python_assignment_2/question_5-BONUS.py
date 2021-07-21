#!/usr/bin/env python

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn

from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# ----------------------------------------------------------------------
# Problem 5 (Bonus)
# 
# Apply Hiearchical Clustering to delta.csv and observe how physical 
# features are being clustered in early leaves at the bottom. Please 
# submit your code and dendrogram graph along with 1-2 sentences 
# interpretation.
# ----------------------------------------------------------------------

# Bogdan: Usually in Python, it is good practice (i.e. pythonic) to place
# all the function definitions at the top of the source file. Of course
# since you are working in a Jupyter Notebook, it makes more sense to write
# the functions at whichever location seems logical, so that your Notebook
# can flow in its reading.
def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

# Apply Hiearchical Clustering to delta.csv ...
df = pd.read_csv('delta.csv', index_col='Aircraft')

# setting distance_threshold=0 ensures we compute the full tree.
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

model_labels = model.fit_predict(df)

print("Method 1 Of Getting Labels:")
print(model.labels_)
print()

print("Alternative Method 2 Of Getting Labels:")
model = model.fit(df)
print(model.labels_)
print()

# ...and observe how physical features are being clustered in early leaves
# at the bottom [nuertey_figure_7-Dendrogram-BONUS.png].
plt.title('Hierarchical Clustering Dendrogram')

# plot the top three levels of the dendrogram
#plot_dendrogram(model, truncate_mode='level', p=3)

# plot the all levels of the dendrogram
plot_dendrogram(model)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()

# ----------------------------------------------------------------------
# Bogdan: Discuss results with with 1-2 sentences interpretation here...
# ----------------------------------------------------------------------
