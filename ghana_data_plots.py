#***********************************************************************
# @file
#
# Ghana data visualizations. 
#
# @note 
#
# @warning  None
#
#  Created: September 11, 2021
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

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may
# depend on the context. This is sometimes called chained assignment and
# should be avoided. See Returning a View versus Copy. [dataframe_loop_example.py]
pd.options.mode.chained_assignment = None

# To read native Excel files (.xls), ensure you install the following 
# a priori:
#
# pip install xlrd

# To read native Open Document Formatted spreadsheet files (.ods), 
# ensure you install the following a priori:
#
#pip install odfpy
ghana_population_data_df = pd.read_excel("ghana_population_data.ods",
                                              engine="odf")

print('ghana_population_data_df.shape:')
print(ghana_population_data_df.shape)
print()

print('ghana_population_data_df:')
print(ghana_population_data_df)
print()

print('ghana_population_data_df.info():')
print(ghana_population_data_df.info())
print()

ghana_figure_1 = px.scatter(ghana_population_data_df, 
                            x="City", 
                            y="Population",
                            title="Ghana Population by City",
                            size="Population", 
                            size_max=60, # size_max (int (default 20)) – Set the maximum mark size when using size
                            color="City",
                            hover_name="City",
                            hover_data={'Population':True,
                                        'Region':True,
                                        'City':False
                                    }
                            )
ghana_figure_1.show()
