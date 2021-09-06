#***********************************************************************
# @file
#
# Analyze my historical illinoisjoblink.illinois.gov job search records
# just for fun and to occupy my time in productive pursuits.
#
# @note None
#
# @warning  None
#
#  Created: September 6, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

# To read native Excel files (.xls), ensure you install the following 
# a priori:
#
# pip install xlrd

# To read native Open Document Formatted spreadsheet files (.ods), 
# ensure you install the following a priori:
#
#pip install odfpy
nuertey_job_search_records_df = pd.read_excel("nuertey_job_search_records.ods",
                                              engine="odf")

print('nuertey_job_search_records_df.shape:')
print(nuertey_job_search_records_df.shape)
print()

print('nuertey_job_search_records_df:')
print(nuertey_job_search_records_df)
print()

print('nuertey_job_search_records_df.info():')
print(nuertey_job_search_records_df.info())
print()

# Select only range of indexes with valid data:
valid_data_indexes = list(range(5, 145))

print('valid_data_indexes:')
print(valid_data_indexes)
print()

# Option 1:
#job_search_records_df = nuertey_job_search_records_df[nuertey_job_search_records_df.index.isin(valid_data_indexes)]

# Option 2:
#
# Alternatively, pass the index to the row indexer/slicer of .loc
# Ensure to specify the culprit columns as well. [indexes, :] for all columns.
# And note that Python slices exclude the ending index.
job_search_records_df = nuertey_job_search_records_df.loc[valid_data_indexes, :]

print('job_search_records_df:')
print(job_search_records_df)
print()

print('job_search_records_df.info():')
print(job_search_records_df.info())
print()
