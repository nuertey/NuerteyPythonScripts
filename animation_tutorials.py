#***********************************************************************
# @file
#
# Animation Tutorials.
#
# @note 
#
# @warning  None
#
#  Created: September 13, 2021
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

from datetime import datetime
from dateutil.relativedelta import relativedelta
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

