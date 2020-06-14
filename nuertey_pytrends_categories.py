import os
import sys
import argparse
import time
import datetime
import pytrends
import pycountry
import collections
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, date, time
from pytrends.request import TrendReq
from argparse import RawTextHelpFormatter
from itertools import chain

pd.set_option('display.max_rows', 100)

def myprint(d, ident=0):
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v, ident+1)
        elif k != 'children':
            print('\t' * (ident+1) + "{0} : {1}\n".format(k, v))

# The yield from operator returns an item from a generator one at a time.
# This syntax for delegating to a subgenerator was added in 3.3
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

for ele in d.values():
    if isinstance(ele,dict):
       for k, v in ele.items():
           print(k,' ',v)

def RecursiveTraverse(nested_categories, indent=0):
    for element in nested_categories.values():
        element = str(element).strip('[').strip(']')
        if isinstance(element, dict):
            for key, value in element.items():
                # print('\t' * indent + str(key))
                if key == 'children':
                    RecursiveTraverse(value, indent+1)
                elif key == 'name':
                    #print('\t' * (indent+1) + str(value))
                    category_data = pd.DataFrame.from_dict(value)
                    #category_data = category_data['children'].apply(pd.Series)
                    print(category_data)
                    print()

        else:
            print('\t' * (indent+1) + "Warning! Not a dictionary:")
            print('\t' * (indent+1) + str(element))
            print()

pytrend = TrendReq()
all_categories = pytrend.categories()
print(all_categories)
print()
all_categories_data = pd.DataFrame.from_dict(all_categories)
all_categories_data = all_categories_data['children'].apply(pd.Series)
print(all_categories_data)
print()
main_categories_data = all_categories_data[['name', 'id']]
