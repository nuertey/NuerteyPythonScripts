#***********************************************************************
# @file
#
# Python script for Airbnb Consultancy. Its primary goal is to aid Airbnb
# in better understanding their dataset relating to the price of their 
# listings on Amsterdam, North Holland, The Netherlands. For reference,
# this dataset was obtained via the location: 
#
#          http://insideairbnb.com/get-the-data.html
#                              ├── listings.csv.gz
#
# @note None
#
# @warning  None
#
#  Created: March 3, 2021
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas

import pandas as pd
import gzip # There is no need to pip install this module as it is 
            # contained within the standard library.

pd.set_option('display.max_rows', 50)
pd.set_option('display.min_rows', 50)

file_name = './listings.csv.gz'

the_compressed_file = gzip.open(file_name, 'rb')
airbnb_dataset_raw = the_compressed_file.read()

# For debugging, though the raw data is not yet processed and the output 
# would be unhelpful as yet:
#print(airbnb_dataset_raw)
#print()

# Compression : {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default ‘infer’ 
# for on-the-fly decompression of on-disk data. If ‘infer’ and 
# filepath_or_buffer is path-like, then detect compression from the 
# following extensions: ‘.gz’, ‘.bz2’, ‘.zip’, or ‘.xz’ (otherwise no 
# decompression).
#
# Reference: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
airbnb_dataset_df = pd.read_csv(file_name)
print(airbnb_dataset_df)
print()

# To ensure that we will have no issues plotting/visualizing the data,
# infer their proper data types:
airbnb_data = airbnb_dataset_df.infer_objects()

print('Data type of each column of cleaned up Airbnb Dataframe for Amsterdam after conversion:')
print(airbnb_data.dtypes)
print()
