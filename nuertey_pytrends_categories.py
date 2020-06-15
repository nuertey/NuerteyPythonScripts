import ast
import pytrends
import collections
import numpy as np
import pandas as pd
from pytrends.request import TrendReq

pd.set_option('display.max_rows', 200)

category_names_list = []
category_ids_list   = []

# The yield from operator returns an item from a generator one at a time.
# This syntax for delegating to a subgenerator was added in 3.3
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def RecursiveTraverse(nested_categories, indent=0):
    print('\t' * (indent) + "Within RecursiveTraverse() ... ")
    print()
    if isinstance(nested_categories, collections.abc.Mapping):
        print('\t' * (indent+1) + "Success! Expected! A dictionary.")
        print()
        culprit_line = ""
        for key, value in nested_categories.items():
            #print(key)
            #print()
            #print(value)
            #print()
            if key == 'children':
                #value = str(value)[1:-1] # Strip off the square brackets.
                print(value)
                print()
                RecursiveTraverse(value, indent+1)
            elif key == 'name':
                culprit_line = '\t' * (indent+1) + str(value)
                category_names_list.append(value)
            elif key == 'id':
                culprit_line = culprit_line + " : " + str(value)
                category_ids_list.append(value)
                print(culprit_line)
                print()
    else:
        print('\t' * (indent+1) + "Warning! Unexpected! Not a dictionary:")
        print('\t' * (indent+1) + str(nested_categories))
        print()
        # enumerate() effectively 'removes' the square brackets as the
        # square brackets were simply denoting a list.
        for i, element in enumerate(nested_categories):
            #print(i, ": ", element)
            RecursiveTraverse(element, indent+1)

pytrend = TrendReq()
all_categories = pytrend.categories()
#print(all_categories)
#print()

all_categories_data = pd.DataFrame.from_dict(all_categories)
all_categories_data = all_categories_data['children'].apply(pd.Series)
#print(all_categories_data)
#print()

main_categories_data = all_categories_data[['name', 'id']]
#print(main_categories_data)
#print()

#all_categories = str(all_categories).replace('[', '')
#all_categories = all_categories.replace(']', '')
#all_categories = "'{}'".format(all_categories) # Set thing up so we can convert back to dict.
#all_categories = ast.literal_eval(all_categories) # Convert back to dictionary.
RecursiveTraverse(all_categories)
all_categories_data = pd.DataFrame({'name': category_names_list, 'id': category_ids_list})
pd.set_option('display.max_rows', 200)
print(all_categories_data)
print()
