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
try:
    from collections.abc import Mapping
    from collections.abc import Sequence
except ImportError:
    from collections import Mapping
    from collections import Sequence

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
def flatten(nested_categories, indent=0):
    if isinstance(nested_categories, Mapping) and not isinstance(nested_categories, (str, bytes)):
        print("Found a dictionary:")
        #print(nested_categories)
        #print()
        culprit_line = ""
        for key, value in nested_categories.items():
            #print(nested_categories)
            #print()
            if key == 'children':
                # Sub-lists are sub-categories (or children) of the parent list:
                yield from flatten(value, indent+1)
            elif key == 'name':
                culprit_line = "{0}{1} : ".format(('\t' * (indent+1)), value)
            elif key == 'id':
                culprit_line = culprit_line + str(value)
                print(culprit_line)
                yield culprit_line
    elif isinstance(nested_categories, Sequence) and not isinstance(nested_categories, (str, bytes)):
        print("Found a list:")
        #print(nested_categories)
        #print()
        for entity in enumerate(nested_categories):
            print(entity)
            print()
            yield from flatten(entity, indent+1)
    else:
        print("Found an unexpected string or integer entity (i.e. a single category name or id):")
        print(nested_categories)
        print()
        yield nested_categories

def RecursiveTraverse(nested_categories, indent=0):
    if isinstance(nested_categories, Mapping):
        culprit_line = ""
        for key, value in nested_categories.items():
            if key == 'children':
                # Sub-lists are sub-categories (or children) of the parent list:
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
                #print(culprit_line)
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
#print(parsed_categories_data.dtypes)
#print()

# To reverse dataframe use the following, though testing proves that it
# does not work in the present case:
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

#all_categories_data = all_categories_data['children'].apply(pd.Series)
#print(all_categories_data)
#print()

#exploded_categories_data = all_categories_data.unstack(level=0)
#print(exploded_categories_data)
#print()

#exploded_categories_data = all_categories_data.explode('children')
#print(exploded_categories_data)
#print()

main_categories_data = all_categories_data[['name', 'id']]
print(main_categories_data)
print()

#print("Attempting to flatten... Output is as follows:")
#print()
#platypus = flatten(all_categories)

# platypus.next() has been renamed to platypus.__next__(). The reason for this is consistency: special methods like __init__() and __del__() all have double underscores (or "dunder" in the current vernacular), and .next() was one of the few exceptions to that rule. This was fixed in Python 3.0. [*]
# 
# But instead of calling platypus.__next__(), use next(platypus).
# 
# [*] There are other special attributes that have gotten this fix; func_name, is now __name__, etc.

#how_many = len(all_categories)
#print(how_many)
#print(next(platypus))
#for i in platypus:
#    print()
#    print(i, next(platypus))
#    print()
#    print("Calling next(platypus)..." )
#print()

# =====================================================================
# JUST A FURTHER PRACTICE SESSION TO TEST OUT SOME IDEAS
# =====================================================================
#
# .apply(pd.Series) seems intended to create a row-wise or column-wise
# dataframe from the source column. If the result is column-wise and you
# needed row-wise (or vice-versa), use .transpose() on result.
print("Tutorial 1...")
print()

the_dictionary = {'2017-9-11': {'Type1': [15, 115452.0, 3], 'Type2': [47, 176153.0, 4], 'Type3': [0, 0, 0]}, '2017-9-12': {'Type1': [26, 198223.0, 5], 'Type2': [39, 178610.0, 6], 'Type3': [0, 0, 0]}}

print(the_dictionary)
print()

df = pd.DataFrame.from_dict(the_dictionary, orient='index')
print(df)
print()

# I need to split values in the lists into different columns and group them by Types. 
# This is what I do:
#df_new = df[list(df)].unstack().apply(pd.Series)
#print(df_new)

# I think faster solution is DataFrame constructor, see timings:
s = df.unstack()
print(s)
print()

newest_df = pd.DataFrame(s.values.tolist(), index=s.index)
print(newest_df)
print()

# Or If values are strings:
#df = df.unstack().str.strip('[]').str.split(', ', expand=True).astype(float)
#print(df)
#print()

#                     0         1    2
# Type1 2017-9-11  15.0  115452.0  3.0
#       2017-9-12  26.0  198223.0  5.0
# Type2 2017-9-11  47.0  176153.0  4.0
#       2017-9-12  39.0  178610.0  6.0
# Type3 2017-9-11   0.0       0.0  0.0
#       2017-9-12   0.0       0.0  0.0

# Or is possible convert values to lists:
# import ast
# 
# s = df.unstack().apply(ast.literal_eval)
# df = pd.DataFrame(s.values.tolist(), index=s.index).astype(float)
# print(df)
# print()

#                     0         1    2
# Type1 2017-9-11  15.0  115452.0  3.0
#       2017-9-12  26.0  198223.0  5.0
# Type2 2017-9-11  47.0  176153.0  4.0
#       2017-9-12  39.0  178610.0  6.0
# Type3 2017-9-11   0.0       0.0  0.0
#       2017-9-12   0.0       0.0  0.0

# =====================================================================
print("Tutorial 2...")
print()

df = pd.DataFrame({
    'name': ['john', 'smith'],
    'id': [1, 2],
    'apps': [[['app1', 'v1'], ['app2', 'v2'], ['app3','v3']], 
             [['app1', 'v1'], ['app4', 'v4']]]
})
print(df)
print()

# Instead of .apply(pd.Series) (which is awfully slow), use pd.DataFrame(df.apps.tolist()): 
dftmp = df.apps.apply(pd.Series).T.melt().dropna()
print("dftmp:\n", dftmp)
print()

df_faster = pd.DataFrame(df.apps.tolist())
print("df_faster:\n", df_faster)
print()

dfapp = (dftmp.value
              .apply(pd.Series)
              .set_index(dftmp.variable)
              .rename(columns={0:'app_name', 1:'app_version'})
        )
print(dfapp)
print()

print("Merging...")
print()

df_final = df[['name', 'id']].merge(dfapp, left_index=True, right_index=True)

print(df_final)
print()

# ---------------------------------------------------------------------
# Alternate approaches of above documented below:

# Chain of pd.Series easy to understand, also if you would like know more
# methods, check unnesting:
print("Tutorial 3...")
print()

print(df)
print()

print("Method 1 (apply(pd.Series) twice):")
print()

df_output = df.set_index(['name','id']).apps.apply(pd.Series).\
         stack().apply(pd.Series).\
            reset_index(level=[0,1]).\
                rename(columns={0:'app_name',1:'app_version'})
print(df_output)
print()

# Out[541]: 
#     name  id app_name app_version
# 0   john   1     app1          v1
# 1   john   1     app2          v2
# 2   john   1     app3          v3
# 0  smith   2     app1          v1
# 1  smith   2     app4          v4

print("Method 2 (call unnesting()) python method on column you intend to explode):")
print()

# Method two slightly modify the function I write:
def unnesting(df, explode):
    idx = df.index.repeat(df[explode[0]].str.len())
    df1 = pd.concat([
        pd.DataFrame({x: sum(df[x].tolist(),[])}) for x in explode], axis=1)
    df1.index = idx
    return df1.join(df.drop(explode, 1), how='left')

# And then:
yourdf = unnesting(df, ['apps'])
print(yourdf)
print()

yourdf['app_name'], yourdf['app_version'] = yourdf.apps.str[0], yourdf.apps.str[1]
print(yourdf)
print()

# Out[548]: 
#          apps  id   name app_name app_version
# 0  [app1, v1]   1   john     app1          v1
# 0  [app2, v2]   1   john     app2          v2
# 0  [app3, v3]   1   john     app3          v3
# 1  [app1, v1]   2  smith     app1          v1
# 1  [app4, v4]   2  smith     app4          v4

print("Method 3 (compact way to call unnesting() and reindex at the same time):")
print()

# Or, alternatively to all the above:
yourdf = unnesting(df, ['apps']).reindex(columns=df.columns.tolist()+['app_name','app_version'])
print(yourdf)
print()

yourdf[['app_name','app_version']] = yourdf.apps.tolist()
print(yourdf)
print()

# Out[567]: 
#          apps  id   name app_name app_version
# 0  [app1, v1]   1   john     app1          v1
# 0  [app2, v2]   1   john     app2          v2
# 0  [app3, v3]   1   john     app3          v3
# 1  [app1, v1]   2  smith     app1          v1
# 1  [app4, v4]   2  smith     app4          v4
