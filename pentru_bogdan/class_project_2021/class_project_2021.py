#***********************************************************************
# @file
#
# Class Project 2021: Data Mining
#
# @note None
#
# @warning  None
#
#  Created: August 9, 2021
#   Author: Bogdan Constantinescu
#**********************************************************************/
#!/usr/bin/env python

import re
import pandas as pd  
from nose.tools import assert_equal
from tqdm import tqdm

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.options.mode.chained_assignment = None

laptops_resolution_horizontal_data = []
laptops_resolution_vertical_data = []
laptops_resolution_encoded_data = []

error_count = 0

screen_resolution_encoded_option_2 = []

screen_resolution_decoded_option_2 = []

def strip_text_from_numbers(laptop_resolution_input):
    match = re.match(r"([a-zA-Z+/\s4K]*)([0-9]+)[^r]([0-9]+)", laptop_resolution_input, re.I)
    if match:
        items = match.groups()
        
        # Uncomment to view output for debug and further understanding:
        #print("items:")
        #print(items)
        #print()
        
        horizontal_pixel_counts = items[-2]
        vertical_pixel_counts = items[-1]
        encoded_pixel_counts = int(str(horizontal_pixel_counts) + str(vertical_pixel_counts))
    
        # Uncomment to view output for debug and further understanding:
        #print("horizontal_pixel_counts:")    
        #print(horizontal_pixel_counts)
        #print()

        #print("vertical_pixel_counts:")    
        #print(vertical_pixel_counts)
        #print()

        #print("encoded_pixel_counts:")    
        #print(encoded_pixel_counts)
        #print()
                
        laptops_resolution_horizontal_data.append(horizontal_pixel_counts)
        laptops_resolution_vertical_data.append(vertical_pixel_counts)
        laptops_resolution_encoded_data.append(encoded_pixel_counts)
    else:
        global error_count
        error_count = error_count + 1
        print("Could not match on this string [%d]:", error_count)
        print(laptop_resolution_input)
        print()
        
    # End of function. Void return.

def encode_decode_screen_resolution_option_2(laptop_resolution_input):
    the_bytes_representation = str(laptop_resolution_input).encode('utf-8')
    the_integer_representation = int.from_bytes(the_bytes_representation, 'little')
    
    screen_resolution_encoded_option_2.append(the_integer_representation)

    recovered_bytes = the_integer_representation.to_bytes((the_integer_representation.bit_length() + 7) // 8, 'little')
    recovered_string = recovered_bytes.decode('utf-8')
    
    screen_resolution_decoded_option_2.append(recovered_string)
    
    # End of function. Void return.
    
laptops_data_df = pd.read_csv('laptops.csv')

# ======================================================================
# If you want to add new data it must be here before the "Master Mapping Table"
# is created. otherwise you have to recreate it with the new data attached.
# ======================================================================
  
# Answer to Mr. B's hypothetical question:
#hypothetical_resolution_not_in_dictionary = 'Bogdan Old McMaster Monitor 800x600'

# First you must add it to the dictionary for like in Mathematics, the 
# "set" must be bounded for one to be able to work with it. It cannot be
# an infinite unbounded set and still provide you with "valid mappings".
# I think this was one of the lemmas we studied in McMaster in the Complex
# Imaginary Advanced Math class which textbook I still have :).
#
# So, add it to our 'set' with these following steps:

# Bogdan, research more on this call as I have not been able to confirm
# so far that this call is working. Basically you must add it to the input
# dataset before constructing the mapping table.
#
# But think more on why you asked me that question? What scenario prompted it?
# The scenario itself will give you clues on how properly to solve it. And
# go over my previous solution to understand when you have time before we move on 
# to other questions. Okay brother, I am going back in the Sun to chill for
# a bit.  
#laptops_data_df.append({'ScreenResolution':hypothetical_resolution_not_in_dictionary}, ignore_index=True)

# Everything can now proceed as it was and it will all work. Nothing else to be done.
# ======================================================================

print('laptops_data_df.head():')
print(laptops_data_df.head())
print()

print('laptops_data_df.info():')
print(laptops_data_df.info())
print()

print('laptops_data_df[\'ScreenResolution\']:')
print(laptops_data_df['ScreenResolution'])
print()

# Example of a list comprehension in Python which gives faster processing:
# We are looping simply so we can display a progress bar on the execution
# of the list comprehension:
for i in tqdm(range(1)):
    [strip_text_from_numbers(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]

# Uncomment to view output for debug and further understanding:
#print('laptops_resolution_horizontal_data:')
#print(laptops_resolution_horizontal_data)
#print()

#print('laptops_resolution_vertical_data:')
#print(laptops_resolution_vertical_data)
#print()

#print('laptops_resolution_encoded_data:')
#print(laptops_resolution_encoded_data)
#print()

# Creating a DataFrame for easier manipulation, analysis and processing:
resolution_data_df = pd.DataFrame(
    {'HorizontalPixelCounts': laptops_resolution_horizontal_data,
     'VerticalPixelCounts': laptops_resolution_vertical_data,
     'EncodedPixelCounts': laptops_resolution_encoded_data
    })

print('SORTED EncodedPixelCounts (ALL, including duplicates) for visual VALIDATION:')
print(sorted(resolution_data_df['EncodedPixelCounts']))
print()

print('Count of UNIQUE EncodedPixelCounts for VALIDATING our mapping results later:')
print(resolution_data_df.EncodedPixelCounts.nunique())
print()

# Ascending sort by default, hence will give us smallest to largest EncodedPixelCounts
# which will result in giving us a numeric number starting from 1 for the lowest
# resolution and incrementing by 1 to the largest resolution. Note that 
# duplicate resolutions will have the same EncodedPixelCounts and hence
# should have the same dictionary value:  
sorted_unique_list = sorted(resolution_data_df.EncodedPixelCounts.unique())
sorted_unique_df = pd.DataFrame(
    {'EncodedPixelCounts': sorted_unique_list
    })
print('SORTED and UNIQUE EncodedPixelCounts DataFrame for visual VALIDATION:')
print(sorted_unique_df)
print()

temporary_list = []

# Store the equivalent NumericValueMapping in our DataFrame that we are
# going to be using as our "Master Mapping Table" going forward:
for i in tqdm(range(1)):
    for current_row in zip(resolution_data_df.index, resolution_data_df['EncodedPixelCounts']):
        # Leverage a simple dictionary-like approach of key='sorted EncodedPixelCounts',
        # value='value-based approach number signifying better resolution'
        temporary_index = sorted_unique_df.index[sorted_unique_df['EncodedPixelCounts'] == current_row[1]].values
        
        # This should effectively give us, 'higher resolution, higher numeric
        # value mapping': 
        temporary_list.append((temporary_index[0] + 1))
        # You can access the current index if you need to with the following:
        # current_row[0]

resolution_data_df['NumericValueMapping'] = temporary_list

# Important Validation Step Here:
assert_equal(resolution_data_df['NumericValueMapping'].max(), resolution_data_df.EncodedPixelCounts.nunique())

# You can store the original string description in the same DataFrame
# for easier visual validation, and, to aid the invertibility function: 
resolution_data_df['OriginalScreenResolution'] = laptops_data_df['ScreenResolution'].values

# View the relevant "Master Mapping Table" for visual validation:
print('Relevant columns in Master Mapping Table:')
print(resolution_data_df[['EncodedPixelCounts', 'NumericValueMapping', 'OriginalScreenResolution']])
print()

# For debug, can view the complete (all columns) of the "Master Mapping Table": 
#print('Relevant columns in Master Mapping Table:')
#print('resolution_data_df:')
#print(resolution_data_df)
#print()

print('resolution_data_df.info():')
print(resolution_data_df.info())
print()

# ==========================
# DEMONSTRATE INVERTIBILITY:
# ==========================
# Henceforth we can easily and simply prove the invertibility of the numeric
# value mapping by leveraging the "Master Mapping Table" index like so:
for i in tqdm(range(1)):
    for current_row in zip(resolution_data_df.index, 
                           resolution_data_df['NumericValueMapping'], 
                           resolution_data_df['EncodedPixelCounts'],
                           resolution_data_df['OriginalScreenResolution']):
        # Essentially the "Master Mapping Table" has already captured all that
        # info for us. No other complex operations to perform to get the inverse required:
        #print('NumericValueMapping: {}'.format(current_row[1]))
        #print('EncodedPixelCounts: {}'.format(current_row[2]))
        #print('OriginalScreenResolution: {}'.format(current_row[3]))
        #print()
        pass

# ======================================================================
# Option 2 for encoding and decoding, which might, make more sense. Of
# course it depends on what you intend to use this data for. Think of it
# with your group.... There is also "the bytes" value if the integer is
# too big. Such encodings and decodings "is more logical" than the manual
# stripping you had wanted me to do. Of course, your mileage may vary:
# ======================================================================
for i in tqdm(range(1)):
    [encode_decode_screen_resolution_option_2(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]

# Creating a DataFrame for easier manipulation, analysis and processing:
option_2_data_df = pd.DataFrame(
    {'EncodedScreenResolution': screen_resolution_encoded_option_2,
     'DecodedScreenResolution': screen_resolution_decoded_option_2
    })

option_2_data_df['OriginalScreenResolution'] = laptops_data_df['ScreenResolution'].values

# Option 2 output currently commented out for easier debugging:
#print('option_2_data_df:')
#print(option_2_data_df)
#print()

#print('option_2_data_df.info():')
#print(option_2_data_df.info())
#print()
