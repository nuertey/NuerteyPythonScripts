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
    tail = laptop_resolution_input[len(head):]

    #print("head:")    
    #print(head)
    #print()

#    print("tail:") 
#    print(tail)
#    print()
    
    return tail

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

# Split on your separator at most once, and take the first piece:

vertical_separator = 'x'

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

#match = re.match(r"([a-z]+)([0-9]+)", laptops_data_df['ScreenResolution'], re.I)
#if match:
#    items = match.groups()
#print(items)
#print()

#laptops_resolution_data_df = []

# Example of a list comprehension in Python which gives faster processing:
#laptops_resolution_data_df['VerticalPixelCounts'] = [strip_text_from_numbers(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]
#
laptops_resolution_vertical_data = [strip_text_from_numbers(laptop_resolution_string) for laptop_resolution_string in laptops_data_df['ScreenResolution']]

print('laptops_resolution_vertical_data:')
print(laptops_resolution_vertical_data)
print()
