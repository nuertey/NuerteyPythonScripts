#***********************************************************************
# @file
#
# Python script showing how to recursively parse and display Google Trends 
# Categories Dictionary/List.
#
# @note     Note that the Google Trends Categories listing is returned
#           from the pytrends API as a dictionary of a list of a dictionary
#           of a list and so on, nested several levels deep. 
#
# @warning  None
#
#  Created: June 14, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
# pylint: disable=C0103,C0200,R0205
from __future__ import print_function
import pytrends
import functools
import collections
import numpy as np
import pandas as pd
from pytrends.request import TrendReq

#pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 200)
pd.set_option('display.min_rows', 200)
pd.set_option('display.expand_frame_repr', True)

def displayDataFrame(dataframe, displayNumRows=True, displayIndex=False, leftJustify=True):
    # type: (pd.DataFrame, bool, bool, bool) -> None
    """
    :param dataframe: pandas DataFrame
    :param displayNumRows: If True, show the number or rows in the output.
    :param displayIndex: If True, then show the indexes
    :param leftJustify: If True, then use below technique to format columns left justified.
    :return: None
    """

    if leftJustify:
        format_mappings = {}

        for columnName in list(dataframe.columns):
            columnType = type(columnName)  # The magic!!
            #print("{} =>  {}".format(columnName, columnType))
            #print()
            form = "{{}}".format()
            if columnType == type(bool):
                form = "{{!s:<8}}".format()
            elif columnType == type(float):
                form = "{{!s:<5}}".format()
            elif columnType == type(int):
                form = "{{!s:<5}}".format()
            elif columnType == type(str):
                max = dataframe[columnName].str.len().max()
                form = "{{:<{}s}}".format(max)

            format_mappings[columnName] = functools.partial(str.format, form)
        
        # TBD Nuertey Odzeyem; can also apply the format_mappings to the
        # whole dataframe at once like the following, and then print the
        # whole dataframe with one call instead of looping:
        #dataframe = dataframe.to_string(index=displayIndex, formatters=format_mappings)
        #print(dataframe, end="\n\n")
        for key, value in format_mappings.items():
            dataframe[key] = dataframe[key].apply(format_mappings[key])

        # Google Trends Categories seem to be returned in the reverse 
        # logical order. Fix it in a way that makes sense so that top-level
        # categories are displayed first and then their sub-categories 
        # are displayed after. That this will result in a reverse 
        # alphabetical ordering of the category listings is of comparatively
        # minor importance.  
        for idx in reversed(dataframe.index):
            print(dataframe.name[idx], dataframe.id[idx])
        print()
    else:
        print(dataframe.to_string(index=displayIndex), end="\n\n")

    if displayNumRows:
        print("Num Rows: {}".format(len(dataframe)), end="\n\n")

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
    if isinstance(nested_categories, collections.abc.Mapping):
        culprit_line = ""
        for key, value in nested_categories.items():
            if key == 'children':
                RecursiveTraverse(value, indent+1)
            elif key == 'name':
                culprit_line = '\t' * (indent+1) + str(value) + " : "
                #culprit_string = "{0}{1}".format(('\t' * (indent+1)), value)
                #category_names_list.append(value)
                category_names_list.append(culprit_line)
                #category_names_list.append(culprit_string)
            elif key == 'id':
                culprit_line = culprit_line + str(value)
                category_ids_list.append(value)
                print(culprit_line)
    else:
        # enumerate() effectively 'removes' the square brackets as the
        # square brackets are simply denoting lists embedded in the dictionary.
        for i, element in enumerate(nested_categories):
            RecursiveTraverse(element, indent+1)

pytrend = TrendReq()
all_categories = pytrend.categories()
#print(all_categories)
#print()

RecursiveTraverse(all_categories)
parsed_categories_data = pd.DataFrame({'name': category_names_list, 'id': category_ids_list})
#parsed_categories_data.reindex(index=parsed_categories_data.index[::-1])
#or simply:
#parsed_categories_data.iloc[::-1]
#print(parsed_categories_data)

# To left-justify only one particular dataframe column, use the following:
#print(parsed_categories_data.to_string(formatters={'name':'{{:<{}s}}'.format(parsed_categories_data['name'].str.len().max()).format}, index=False))

displayDataFrame(parsed_categories_data)
print()

all_categories_data = pd.DataFrame.from_dict(all_categories)
all_categories_data = all_categories_data['children'].apply(pd.Series)
#print(all_categories_data)
#print()

main_categories_data = all_categories_data[['name', 'id']]
#print(main_categories_data)
#print()

# =====================================================================
# JUST A FURTHER PRACTICE SESSION TO TEST OUT SOME IDEAS
# =====================================================================
the_dictionary = {'2017-9-11': {'Type1': [15, 115452.0, 3], 'Type2': [47, 176153.0, 4], 'Type3': [0, 0, 0]}, '2017-9-12': {'Type1': [26, 198223.0, 5], 'Type2': [39, 178610.0, 6], 'Type3': [0, 0, 0]}}

print(the_dictionary)
print()

df = pd.DataFrame.from_dict(the_dictionary, orient='index')
print(df)
print()

# I need to split values in the lists into different columns and group them by Types. 
# This is what I do:
df_new = df[list(df)].unstack().apply(pd.Series)
print(df_new)
