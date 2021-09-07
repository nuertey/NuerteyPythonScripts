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

import datetime
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

#print('valid_data_indexes:')
#print(valid_data_indexes)
#print()

# Option 1:
#job_search_records_df = nuertey_job_search_records_df[nuertey_job_search_records_df.index.isin(valid_data_indexes)]

# Option 2:
#
# Alternatively, pass the index to the row indexer/slicer of .loc
# Ensure to specify the culprit columns as well. [indexes, :] for all columns.
# And note that Python slices exclude the ending index.
job_search_records_df = nuertey_job_search_records_df.iloc[valid_data_indexes, :]

# Good teaching comment:
#
# "If your DataFrame is named df then use df.iloc[:, [0, 3, 4]]. Usually if
# you want this type of access pattern, you'll already know these particular
# column names, and you can just use df.loc[:, ['name2', 'name5']] where
# 'name2' and 'name5' are your column string names for the respective columns you want"
# * Note that unlike integer slicing, 'name5' is included in the columns):

#print('job_search_records_df:')
#print(job_search_records_df)
#print()
#
#print('job_search_records_df.info():')
#print(job_search_records_df.info())
#print()

# Slice again to get only the columns that we are interested in:
job_search_records_df = job_search_records_df.iloc[:, [0, 3, 4]]

#print('job_search_records_df:')
#print(job_search_records_df)
#print()
#
#print('job_search_records_df.info():')
#print(job_search_records_df.info())
#print()

# Now rename the columns to something befitting what they actually represent:
#
# Note to ALWAYS prefer to work with COLUMN NAMES that are just one word, no spaces!.
#
# Option 1:

#job_search_records_df.rename(columns={'Work Search Record for NUERTEY ODZEYEM':'DateApplied', 
#                   'Unnamed: 3':'CompanyName', 'Unnamed: 4':'JobTitle'}, inplace=True)
       
# Option 2 for renaming by column indexes in case the column names are unknown:
column_indices = [0, 1, 2]
new_names = ['DateApplied', 'CompanyName', 'JobTitle'] 
old_names = job_search_records_df.columns[column_indices]
job_search_records_df.rename(columns=dict(zip(old_names, new_names)), inplace=True)
           
# Ensure the Date Applied column is actually a datetime object for plotly
job_search_records_df['DateApplied'] = pd.to_datetime(job_search_records_df['DateApplied'])

job_search_records_df['CompanyName'] = job_search_records_df['CompanyName'].astype(str)
job_search_records_df['JobTitle'] = job_search_records_df['JobTitle'].astype(str)

print(job_search_records_df.dtypes)
print()

# So as to graph chronologically:
job_search_records_df = job_search_records_df.sort_values(by='DateApplied', ignore_index=True)

print('job_search_records_df:')
print(job_search_records_df)
print()

# Let's visualize with plotly:
#figure_1 = px.scatter(job_search_records_df, 
#                      y="CompanyName", 
#                      x="DateApplied", 
#                      title="Nuertey Odzeyem's Historical Job Search Data From illinoisjoblink.illinois.gov",
#                      color="CompanyName", 
#                      symbol="CompanyName",
#                      hover_name="CompanyName",        # Display this column in bold as the tooltip title.
#                      hover_data={'DateApplied':True,  # Add this column to hover tooltip with default formatting.
#                                  'CompanyName':False, # Remove this column from hover tooltip.
#                                  'JobTitle':True      # Add this column to hover tooltip with default formatting.
#                                 }
#                      )
#figure_1.update_traces(marker_size=10)
#figure_1.show()

# Further analysis ensues:
monthly_analysis_df = job_search_records_df.copy()
monthly_analysis_df['MonthOfYear'] = monthly_analysis_df['DateApplied'].dt.strftime('%B, %Y')

print('monthly_analysis_df:')
print(monthly_analysis_df)
print()

month_of_year_list = list(range())

baseline_date = datetime.datetime.today()
number_of_days = 100
month_of_year_list = [baseline_date - datetime.timedelta(days=x) for x in range(numdays)]
