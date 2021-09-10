#***********************************************************************
# @file
#
# Advancing on plotly sunburst plots by assaying some. 
#
# @note 
#   Sunburst plots visualize hierarchical data spanning outwards radially
#   from root to leaves. Similar to Icicle charts and Treemaps, the 
#   hierarchy is defined by labels (names for px.icicle) and parent's 
#   attributes. The root starts from the center and children are added 
#   to the outer rings.
#
# @warning  None
#
#  Created: September 9, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
from nose.tools import assert_equal

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
# so on, until either sequence is exhausted. 
assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may
# depend on the context. This is sometimes called chained assignment and
# should be avoided. See Returning a View versus Copy. [dataframe_loop_example.py]
pd.options.mode.chained_assignment = None

# ======================================================================
# Example 1:
# ======================================================================

# With px.sunburst, each row of the DataFrame is represented as a sector
# of the sunburst. Furthermore, the sunburst plot requires weights (values),
# labels, and parent. Here we compose with a dictionary:
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"], # Labels.
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4]) # Weights.

figure_1 =px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)

figure_1.show()
