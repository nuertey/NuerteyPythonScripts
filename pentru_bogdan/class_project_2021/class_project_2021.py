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

def strip_text_from_numbers(laptop_resolution_input):
    match = re.match(r"([a-z]+)([0-9]+)", laptop_resolution_input, re.I)
    if match:
        items = match.groups()
        print("items:")
        print(items)
        print()
#    else:
#        print("Caught an unexpected exception:")
#        print()

    head = laptop_resolution_input.rstrip('0123456789')
    pixel_counts = laptop_resolution_input.rstrip('x')
    vertical_pixel_counts = laptop_resolution_input[len(head):]

    print("pixel_counts:")    
    print(pixel_counts)
    print()
    
    #pixel_counts_list = [int(i) for i in pixel_counts.split() if i.isdigit()]
    
    vertical_separator = 'x'
    
    pixel_counts_list = pixel_counts.partition(vertical_separator)
    
    print("pixel_counts_list:")    
    print(pixel_counts_list)
    print()
    
    return vertical_pixel_counts

    #return items

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

# laptops_resolution_data_df['HorizontalPixelCounts']

# laptops_resolution_data_df['VerticalPixelCounts'] = laptops_data_df['ScreenResolution'].partition(vertical_separator)

#laptops_resolution_data_df['EncodedPixelCounts']

# print('laptops_resolution_data_df[\'HorizontalPixelCounts\']:')
# print(laptops_resolution_data_df['HorizontalPixelCounts'])
# print()

#print('laptops_resolution_data_df[\'VerticalPixelCounts\']:')
#print(laptops_resolution_data_df['VerticalPixelCounts'])
#print()

#print('laptops_resolution_data_df[\'EncodedPixelCounts\']:')
#print(laptops_resolution_data_df['EncodedPixelCounts'])
#print()

# Example of a list comprehension in Python which gives faster processing:
#laptops_resolution_data_df['VerticalPixelCounts'] = [strip_text_from_numbers(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]
#
laptops_resolution_vertical_data = [strip_text_from_numbers(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]

print('laptops_resolution_vertical_data:')
print(laptops_resolution_vertical_data)
print()
