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
from collections import defaultdict # This is the best way to get an 'invertible'
                                    # mapping from our EncodedPixelCounts to 'your
                                    # intended logical value-based approach...'.  
from nose.tools import assert_equal

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

print('Count of UNIQUE EncodedPixelCounts for VALIDATING our mapping results later:')
print(resolution_data_df.EncodedPixelCounts.nunique())
print()

print('SORTED EncodedPixelCounts (ALL, including duplicates) for visual VALIDATION:')
print(sorted(resolution_data_df['EncodedPixelCounts']))
print()

sorted_unique_list = sorted(resolution_data_df.EncodedPixelCounts.unique())
sorted_unique_df = pd.DataFrame(
    {'EncodedPixelCounts': sorted_unique_list
    })
print('SORTED and UNIQUE EncodedPixelCounts DataFrame for visual VALIDATION:')
print(sorted_unique_df)
print()

## Leverage a simple dictionary of key='sorted EncodedPixelCounts',
## value='value-based approach number signifying better resolution'
#resolution_data_dictionary = defaultdict(int)
#
## Ascending sort by default, hence will give us smallest to largest EncodedPixelCounts
## which will result in giving us a numeric number starting from 1 for the lowest
## resolution and incrementing by 1 to the largest resolution. Note that 
## duplicate resolutions will have the same EncodedPixelCounts and hence
## should have the same dictionary value:  
#for dictionary_key in sorted(resolution_data_df['EncodedPixelCounts']):
#    # For keys already in the dictionary, we do NOT want the numeric
#    # value mapping to increment, so do nothing in that case; otherwise:
#    if dictionary_key not in resolution_data_dictionary:
#        # New key for a higher resolution hence increment its numeric
#        # value mapping and append it to the mapping dictionary. This 
#        # should effectively give us, 'higher resolution, higher numeric
#        # value mapping'. 
#        resolution_data_dictionary[dictionary_key] += 1
#
## Validation step:
#assert_equal(len(resolution_data_dictionary), resolution_data_df.EncodedPixelCounts.nunique())
#
#print('resolution_data_dictionary.items()')
#print(resolution_data_dictionary.items())
#print()

temporary_list = []

# Store the equivalent NumericValueMapping in our DataFrame that we are
# going to be using as our "Master Mapping Table" going forward:
for current_row in zip(resolution_data_df.index, resolution_data_df['EncodedPixelCounts']):
    temporary_index = sorted_unique_df.index[sorted_unique_df['EncodedPixelCounts'] == current_row[1]].values
    temporary_list.append((temporary_index[0] + 1))
    # You can access the current index if you need to with the following:
    # current_row[0]

resolution_data_df['NumericValueMapping'] = temporary_list

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

# Henceforth we can easily and simply prove the invertibility of the numeric
# value mapping by leveraging the "Master Mapping Table" index:



# ======================================================================
# Option 2 for encoding and decoding, which might, make more sense. Of
# course it depends on what you intend to use this data for. Think of it
# with your group.... There is also "the bytes" value if the integer is
# too big. Such encodings and decodings "is more logical" than the manual
# stripping you had wanted me to do. Of course, your mileage may vary:
# ======================================================================
[encode_decode_screen_resolution_option_2(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]

# Creating a DataFrame for easier manipulation, analysis and processing:
option_2_data_df = pd.DataFrame(
    {'EncodedScreenResolution': screen_resolution_encoded_option_2,
     'DecodedScreenResolution': screen_resolution_decoded_option_2
    })

option_2_data_df['OriginalScreenResolution'] = laptops_data_df['ScreenResolution'].values

print('option_2_data_df:')
print(option_2_data_df)
print()

print('option_2_data_df.info():')
print(option_2_data_df.info())
print()
