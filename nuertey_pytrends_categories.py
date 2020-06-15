import pytrends
import functools
import collections
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
from __future__ import print_function

@staticmethod
def displayDataFrame(dataframe, displayNumRows=True, displayIndex=True, leftJustify=True):
    # type: (pd.DataFrame, bool, bool, bool) -> None
    """
    :param dataframe: pandas DataFrame
    :param displayNumRows: If True, show the number or rows in the output.
    :param displayIndex: If True, then show the indexes
    :param leftJustify: If True, then use technique to format columns left justified.
    :return: None
    """

    if leftJustify:
        formatters = {}

        for columnName in list(dataframe.columns):
            columnType = type(columnName)  # The magic!!
            print("{} =>  {}".format(columnName, columnType))
            if columnType == type(bool):
                form = "{{!s:<8}}".format()
            elif columnType == type(float):
                form = "{{!s:<5}}".format()
            elif columnType == type(int):
                form = "{{!s:<5}}".format()
            else:
                max = dataframe[columnName].str.len().max()
                form = "{{:<{}s}}".format(max)

            formatters[columnName] = functools.partial(str.format, form)

        print(dataframe.to_string(index=displayIndex, formatters=formatters), end="\n\n")
    else:
        print(dataframe.to_string(index=displayIndex), end="\n\n")

    if displayNumRows:
        print("Num Rows: {}".format(len(dataframe)), end="\n\n")

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
    if isinstance(nested_categories, collections.abc.Mapping):
        culprit_line = ""
        for key, value in nested_categories.items():
            if key == 'children':
                RecursiveTraverse(value, indent+1)
            elif key == 'name':
                culprit_line = '\t' * (indent+1) + str(value)
                culprit_string = "{0}{1}".format(('\t' * (indent+1)), value)
                #category_names_list.append(value)
                category_names_list.append(culprit_line)
                #category_names_list.append(culprit_string)
            elif key == 'id':
                culprit_line = culprit_line + " : " + str(value)
                category_ids_list.append(value)
                print(culprit_line)
    else:
        # enumerate() effectively 'removes' the square brackets as the
        # square brackets were simply denoting a list.
        for i, element in enumerate(nested_categories):
            RecursiveTraverse(element, indent+1)

pytrend = TrendReq()
all_categories = pytrend.categories()
print(all_categories)
print()

RecursiveTraverse(all_categories)
parsed_categories_data = pd.DataFrame({'name': category_names_list, 'id': category_ids_list})
print(parsed_categories_data.to_string(formatters={'name':'{{:<{}s}}'.format(parsed_categories_data['name'].str.len().max()).format}, index=True))
#print(parsed_categories_data)
print()

all_categories_data = pd.DataFrame.from_dict(all_categories)
all_categories_data = all_categories_data['children'].apply(pd.Series)
#print(all_categories_data)
#print()

main_categories_data = all_categories_data[['name', 'id']]
#print(main_categories_data)
#print()
