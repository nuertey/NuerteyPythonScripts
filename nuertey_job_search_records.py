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

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from nose.tools import assert_equal

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

# ======================================================================
# Test:
temperature_records_df = pd.read_excel("TemperatureReadouts.ods", 
                            engine="odf", 
                            header=None, 
                            names=['TemperatureReadout'])

print('temperature_records_df:')
print(temperature_records_df)
print()

print('temperature_records_df.info():')
print(temperature_records_df.info())
print()

# Let's visualize with plotly:
figure_0 = px.scatter(temperature_records_df, 
                      y="TemperatureReadout", 
                      x=temperature_records_df.index, 
                      title="Temperature Readout DataFrame",
                      )
figure_0.update_traces(marker_size=10)
figure_0.show()

# ======================================================================
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
valid_data_indexes = list(range(5, 196))

#print('valid_data_indexes:')
#print(valid_data_indexes)
#print()

# Option 1:
#job_search_records_df = nuertey_job_search_records_df[nuertey_job_search_records_df.index.isin(valid_data_indexes)]

# Option 2:
#
# Alternatively, pass the index to the row indexer/slicer of .loc
# Ensure to specify the culprit columns as well. [indexes, :] for all columns.
# And note that Python slices with iloc, exclude the ending index.
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

# Slice again to get only the column index positions that we are interested in:
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
figure_1 = px.scatter(job_search_records_df, 
                      y="CompanyName", 
                      x="DateApplied", 
                      title="Nuertey Odzeyem's Historical Job Search Details - Obtained Via illinoisjoblink.illinois.gov",
                      color="CompanyName", 
                      labels={'DateApplied':'Year, Month and Day of Job Application'},
                      symbol="CompanyName",
                      hover_name="CompanyName",        # Display this column in bold as the tooltip title.
                      hover_data={'DateApplied':True,  # Add this column to hover tooltip with default formatting.
                                  'CompanyName':False, # Remove this column from hover tooltip.
                                  'JobTitle':True      # Add this column to hover tooltip with default formatting.
                                 }
                      )
figure_1.update_traces(marker_size=10)
figure_1.show()

# ======================================================================
# Further analysis ensues:
# ======================================================================
monthly_analysis_df = job_search_records_df.copy()
monthly_analysis_df['MonthOfYear'] = monthly_analysis_df['DateApplied'].dt.strftime('%B, %Y')

# Deleting columns without having to reassign the DataFrame:
monthly_analysis_df.drop('CompanyName', axis=1, inplace=True)
monthly_analysis_df.drop('JobTitle', axis=1, inplace=True)

print('monthly_analysis_df:')
print(monthly_analysis_df)
print()

# An example of generating DataFrame indexes with date types can also be
# found in your script, dataframe_tutorial.py line 168.
frequency_analysis_df = monthly_analysis_df.groupby('MonthOfYear').count()
frequency_analysis_df.rename(columns={'DateApplied':'FrequencyCount'}, inplace=True)

print('frequency_analysis_df:')
print(frequency_analysis_df)
print()

MonthOfYear_list = frequency_analysis_df.index.values.tolist()
MonthOfYear_dates_list = [datetime.strptime(some_date, '%B, %Y').date() for some_date in MonthOfYear_list]
MonthOfYear_dates_list = sorted(MonthOfYear_dates_list)

#print('MonthOfYear_dates_list:')
#print(MonthOfYear_dates_list)
#print()
#
#print('len(MonthOfYear_dates_list):')
#print(len(MonthOfYear_dates_list))
#print()

FrequencyCount_list = frequency_analysis_df.FrequencyCount.values.tolist()

#print('FrequencyCount_list:')
#print(FrequencyCount_list)
#print()
#
#print('len(FrequencyCount_list):')
#print(len(FrequencyCount_list))
#print()

assert_equal(len(FrequencyCount_list), len(MonthOfYear_dates_list))

month_of_year_datapoints = []

start_date = '2021-10-1'
end_date = '2015-6-1'

current_datapoint = begin_datapoint = datetime.strptime(start_date, '%Y-%m-%d').date()
end_datapoint = datetime.strptime(end_date, '%Y-%m-%d').date()

while current_datapoint >= end_datapoint:
    month_of_year_datapoints.append(current_datapoint)
    current_datapoint -= relativedelta(months=1)

#print('month_of_year_datapoints:')
#print(month_of_year_datapoints)
#print()
#
#print('len(month_of_year_datapoints):')
#print(len(month_of_year_datapoints))
#print()

frequency_of_job_applications_datapoints = []
frequency_of_job_applications_datapoints = [0 for x in range(0, len(month_of_year_datapoints))]

assert_equal(len(frequency_of_job_applications_datapoints), len(month_of_year_datapoints))

# Note that zip runs only up to the shorter of the two lists(not a problem
# for equal length lists), but, in case of unequal length lists if you want
# to traverse the whole list then use itertools.izip_longest.
for index, (month, count) in enumerate(zip(month_of_year_datapoints, frequency_of_job_applications_datapoints)):
    for value1, value2 in zip(MonthOfYear_dates_list, FrequencyCount_list):
        if month == value1:
            # It is safe to do this as we only modify elements we have already traversed.
            frequency_of_job_applications_datapoints[index] = value2
            break

#print('frequency_of_job_applications_datapoints:')
#print(frequency_of_job_applications_datapoints)
#print()
#
#print('len(frequency_of_job_applications_datapoints):')
#print(len(frequency_of_job_applications_datapoints))
#print()

# Create a DataFrame for plotting:
frequency_count_data_df = pd.DataFrame(
    {'MonthOfYear': month_of_year_datapoints,
     'NumberOfApplications': frequency_of_job_applications_datapoints
    })

print('frequency_count_data_df:')
print(frequency_count_data_df)
print()

figure_2 = px.bar(frequency_count_data_df, 
                        x="MonthOfYear", 
                        y="NumberOfApplications", 
                        title="Nuertey Odzeyem's Historical Job Search Frequency Bar Chart - Obtained Via illinoisjoblink.illinois.gov",
                        hover_data=['MonthOfYear', 'NumberOfApplications'],
                        color='NumberOfApplications',
                        labels={'MonthOfYear':'Year and Month of Job Application'}
                        )
figure_2.show()

# Compare histograms to bar charts for the same dataset:
figure_3 = px.histogram(frequency_count_data_df, 
                        x="MonthOfYear", 
                        y="NumberOfApplications", 
                        histfunc='avg',
                        title="Nuertey Odzeyem's Historical Job Search Average Histogram - Obtained Via illinoisjoblink.illinois.gov",
                        hover_data=['MonthOfYear', 'NumberOfApplications'],
                        color=frequency_count_data_df.NumberOfApplications
                        )
figure_3.show()

# Let Plotly Express perform the aggregation itself automatically on the
# raw data with the count() function instead of manually as I did above:
figure_4 = px.histogram(monthly_analysis_df, 
                        x="MonthOfYear", 
                        title="Nuertey Odzeyem's Historical Job Search Histogram - Obtained Via illinoisjoblink.illinois.gov",
                        hover_data=['MonthOfYear'], # Counts is not accessible here. See later example.
                        color=monthly_analysis_df.DateApplied,
                        labels={'MonthOfYear':'Year and Month of Job Application'}
                        )
figure_4.show()

# ======================================================================
# Histogram Plotly Express Example(s):
# ======================================================================
df = px.data.tips()

print('df = px.data.tips().shape:')
print(df.shape)
print()

print('df = px.data.tips():')
print(df)
print()

print('df = px.data.tips().info():')
print(df.info())
print()

# Two superimposed histograms will be observed distinguished by the color
# "sex", since for our interested dataset, there exists a column sex=
# Male or Female that further qualifies the "total_bill" column. 
figure_5 = px.histogram(df, x="total_bill", color="sex")
figure_5.show()

# Accessing the counts (y-axis) values
#
# JavaScript calculates the y-axis (count) values on the fly in the browser,
# so it's not accessible in the fig. You can manually calculate it using
# np.histogram.
df = px.data.tips()
# create the bins
counts, bins = np.histogram(df.total_bill, bins=range(0, 60, 5))
bins = 0.5 * (bins[:-1] + bins[1:])

figure_6 = px.bar(x=bins, 
                  y=counts,
                  color=bins, 
                  labels={'x':'total_bill', 'y':'count'})
figure_6.show()
