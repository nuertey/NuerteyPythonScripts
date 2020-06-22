#***********************************************************************
# @file
#
# Python script for interrogating trending topics in any topic category
# world-wide.  
#
# @note     None
#
# @warning  None
#
#  Created: June 13, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import os
import sys
import argparse
import time
import datetime
import pytrends
import pycountry
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, date, time
from pytrends.request import TrendReq
from argparse import RawTextHelpFormatter

pd.set_option('display.max_rows', 200)
pd.set_option('display.min_rows', 200)
pd.set_option('display.expand_frame_repr', True)

flattened_category_ids = []
hierarchical_categories_text = []
hierarchical_bullet_points = ['\u2022', '\u25CB', '\u25AA', '\u25AA',
                              '\u25AA', '\u25AA', '\u25AA']

def recursive_flatten(nested_categories, indent=0):
    row_text = ('    ' * indent) + str(hierarchical_bullet_points[indent]) + '  ' + nested_categories['name'] + ': '
    hierarchical_categories_text.append(row_text)
    flattened_category_ids.append(nested_categories['id'])
    try:
        cats = nested_categories['children']
        if len(cats) >= 1: # Ensure that we do contain child sub-categories.
            for i in range(len(cats)):
                cat = cats[i]
                recursive_flatten(cat, (indent+1))
    except Exception as e:
        pass

# Note that during testing, it was discovered that Kenya as country input
# is failing. See the following pytrends github issue that is tracking it:
#
# https://github.com/GeneralMills/pytrends/issues/316

# Login to Google. Only need to run this once, the rest of requests will
# use the same session.
pytrend = TrendReq()

# Returns all possible countries and their ISO-3166-1 codes for usage in help text.
list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)] 
countries_data = pd.DataFrame(np.column_stack([list_alpha_2]), columns=['country_code_2'])
countries_data['country_name'] = [ pycountry.countries.get(alpha_2=code).name for code in countries_data['country_code_2'] ] 

# Returns all main Google Trends categories and their ids for usage in help text.
all_categories = pytrend.categories()
recursive_flatten(all_categories)
categories_dataframe = pd.DataFrame(np.column_stack([hierarchical_categories_text]), columns=['name'])
categories_dataframe['id'] = flattened_category_ids

# parser.choices seems to better prefer dict objects to strings. 
# Better input matching and option display:
country_codes_dictionary = countries_data.to_dict('list') 
category_ids_dictionary = categories_dataframe.to_dict('list') 

# In the future, explicitly set the argument types (type=str|int|bool) 
# to ensure that argument parsing does not fail.
def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-h] | [-v] | [-c country_code] | [-g category] [-t topic]",
        description="Welcome, Velkommen, Woé zɔ, Karibu, Mo-heee to Nuertey's Trending Topics Displayer. How has this topic been trending in the various regions of this country for the past years? Program options described below:",
        epilog="Enjoy using Nuertey's Trending Topics Displayer to latch upon the World's pulse!",
        formatter_class=RawTextHelpFormatter,
        allow_abbrev=False,
        add_help=True
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 0.0.2"
    )
    parser.add_argument(
        "-c", "--country", action='store', choices=country_codes_dictionary['country_code_2'],
        help="\nSpecify the country whose trending topics you want to see. Where country MUST be denoted by one of the country codes from the \npossible Google Trends API range of countries below: \n\n{0}\n\n".format(countries_data.to_string(index=False)),
        nargs='?', default='GH',
        metavar='COUNTRY_CODE_FROM_LIST_BELOW'
    )
    parser.add_argument(
        "-g", "--category", action='store', type=int, choices=category_ids_dictionary['id'],
        help="\nOptionally specify the category from which to query the trending topics. Default is all categories. Where category MUST be denoted by one of the category ids from the \npossible Google Trends API range of categories below: \n\n{0}\n\n".format(categories_dataframe.to_string(formatters={'name':'{{:<{}s}}'.format(categories_dataframe['name'].str.len().max()).format}, index=False)),
        nargs='?', default=0,
        metavar='CATEGORY_ID_FROM_LIST_BELOW'
    )
    parser.add_argument(
        "-t", "--topics", action='store',
        nargs='*', default=['covid', 'somanya', 'ewe', 'cocoa', 'gold'],
        type=str,
        help="Specify the topics that you are interested in monitoring. A maximum of 5 topics are supported like for example:\n-t 'jumia cameroon' 'covid 19 cameroon' 'cameroon online' 'cameroon news' 'cameroon music'"
    )
    return parser

parser = init_argparse()
args = parser.parse_args()
country = args.country
category = args.category
topics = args.topics

culprit_country_name = countries_data.loc[countries_data['country_code_2'] == country,'country_name']
culprit_country_name = next(iter(culprit_country_name), 'no match')
print(culprit_country_name)
print()

# Create payload and capture API tokens. Only needed for interest_over_time(),
# interest_by_region() & related_queries():
#
# Google returns a response with code 400 when a key word is > 100 characters.
pytrend.build_payload(kw_list=topics, timeframe='today 12-m', geo=country, cat=category)

# Interest Over Time
interest_over_time_data = pytrend.interest_over_time()
print(interest_over_time_data)
print()

sns.set(color_codes=True)
dx = interest_over_time_data.plot.line(figsize = (9,6), title = "Trending Topics In " +  culprit_country_name + " - Interest Over Time")
dx.set_xlabel('Date')
dx.set_ylabel('Trends Index')
dx.tick_params(axis='both', which='major', labelsize=13)

# Interest by Region
interest_by_region_data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
print(interest_by_region_data)
print()

interest_by_region_data.reset_index().plot(x='geoName', y=topics, figsize=(120, 10), kind='bar')

# Related Topics, returns a dictionary of dataframes
related_topics_dict = pytrend.related_topics()
print(related_topics_dict)
print()

# Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrend.related_queries()
print(related_queries_dict)
print()

# Get Google Hot Trends data. Trending searches in real time:
# For now there is a bug with this API in pytrends that is being 
# investigated at:
#
# https://github.com/GeneralMills/pytrends/issues/403
# https://github.com/GeneralMills/pytrends/pull/406/commits/e8efdabbe3158d7382130ca4f00aa2e14af965d1
trending_searches_data = pytrend.trending_searches(pn='kenya') 
#trending_searches_data = pytrend.trending_searches()
print(trending_searches_data)
print()

# Get Google Top Charts. Can also specify date as so: "date=201912"
# For now there is a bug with this API in pytrends that is being 
# investigated at:
#
# https://github.com/GeneralMills/pytrends/issues/355

#top_charts_data = pytrend.top_charts(date=2019, geo=country)
#top_charts_data = pytrend.top_charts(date=2019, geo='NG')
top_charts_data = pytrend.top_charts(date=2019, geo='KE')
print(top_charts_data)
print()

# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword=culprit_country_name)
print(suggestions_dict)
print()

plt.show()
