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
