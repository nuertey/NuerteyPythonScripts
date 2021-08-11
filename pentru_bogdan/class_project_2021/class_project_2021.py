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

print('resolution_data_df:')
print(resolution_data_df)
print()

print('resolution_data_df.info():')
print(resolution_data_df.info())
print()

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
