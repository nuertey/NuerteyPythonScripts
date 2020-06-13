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
import json
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
from itertools import chain

def myprint(d, ident=0):
    for k, v in d.items():
        if isinstance(v, dict):
            myprint(v, ident+1)
        elif k != 'children':
            print('\t' * (ident+1) + "{0} : {1}\n".format(k, v))

def pretty(d, indent=0):
    next_key = None
    temp = iter(d) 
    for iter_key, (key, value) in zip(temp, d.items()):
        # print('\t' * indent + str(key))
        next_key = next(temp, None)
        if iter_key == 'children' and next_key != 'children' and next_key != None:
            category_data = pd.DataFrame.from_dict(value)
            #category_data = category_data['children'].apply(pd.Series)
            print(category_data)
            print()
        else:
            #print('\t' * (indent+1) + str(value))
            pretty(value, indent+1)

# Run output of script for Emile on topics trending in Cameroon by region
# ISO-3166-2 and on the category, "politics". Plot it.

# Also run output of script for Emile on Cameroon as a topic trending 
# by Country (ISO-3166-1) world-wide for 20 years. Plot it. 
#
# country_name = pycountry.countries.get({country_code}).name

pd.set_option('display.max_rows', 100)

list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)] 
countries_data = pd.DataFrame(np.column_stack([list_alpha_2]), columns=['country_code_2'])
countries_data['country_name'] = [ pycountry.countries.get(alpha_2=code).name for code in countries_data['country_code_2'] ] 
print(countries_data)
print()

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# category Category to search within (number defaults to all categories)

# Returns Categories dictionary for potential usage in help text.
all_categories = pytrend.categories()
#print(all_categories['children'][:1])
#print()

#print(list(chain.from_iterable(all_categories['children'].items())))
#print()
#print(all_categories.keys())
#print()
#print(all_categories.values())
#print()
# keyList = sorted(all_categories.keys())
# print(keyList)
# print()
#all_categories = pd.DataFrame(all_categories)
#all_categories = pd.concat({k: pd.DataFrame(v).T for k, v in all_categories.items()}, axis=0)
all_categories_data = pd.DataFrame.from_dict(all_categories)
all_categories_data = all_categories_data['children'].apply(pd.Series)
all_categories_data = all_categories_data['children'].apply(pd.Series)
print(all_categories_data)
print()
main_categories_data = all_categories_data[['name', 'id']]
#main_categories_data.set_index('name', inplace=True)
print(main_categories_data)
print()

#json_dict = json.loads(str(all_categories))
#data_list = [ {'name': country, 'id': identifier} for country, identifier in zip(all_categories['name'], all_categories['id']) ] 
# data = pd.DataFrame(all_categories, columns=['name', 'id'])
# print(data)
# print()
#pp = pprint.PrettyPrinter(width=160)
#pp.pprint(dict(all_categories))
#print()
#myprint(all_categories)

# TBD Nuertey Odzeyem, ask Wayo when he wakes, "Would 'topic keyword', 'country' 
# and 'category' inputs to this new python script satisfy his requirement 
# for the future usage of the google trending API prototype? And in what
# order would he prefer these input arguments? Example: 
#
# python nuertey_trending_topics.py -c ghana -g music -t christmas
#
#                     or
#
# python nuertey_trending_topics.py -c ghana -g fashion -t kente "
#
# where -c denotes country for which to monitor for realtime trending topics (list of ISO_3166-2 country codes will be displayed in help text)
#       -g denotes Google Trends Categories listing (list of 25 major category entries will be displayed in help text)
#       -v denotes Google Trends Categories listing (verbosely list all 1427 categories and sub-categories recursively in help text)
#       -t denotes a trending topic keyword of interest

# Create payload and capture API tokens. Only needed for interest_over_time(),
# interest_by_region() & related_queries():
#
# Google returns a response with code 400 when a key word is > 100 characters.
pytrend.build_payload(kw_list=['covid', 'somanya', 'ewe'], timeframe='today 12-m', geo = 'GH', cat = 71)

# Interest Over Time
interest_over_time_data = pytrend.interest_over_time()
#print(interest_over_time_data.head())
print(interest_over_time_data)
print()

sns.set(color_codes=True)
dx = interest_over_time_data.plot.line(figsize = (9,6), title = "Interest Over Time")
dx.set_xlabel('Date')
dx.set_ylabel('Trends Index')
dx.tick_params(axis='both', which='major', labelsize=13)

# Interest by Region
interest_by_region_data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
#print(interest_by_region_data.head())
print(interest_by_region_data)
print()

interest_by_region_data.reset_index().plot(x='geoName', y=['covid', 'somanya', 'ewe'], figsize=(120, 10), kind='bar')

# Related Topics, returns a dictionary of dataframes
related_topics_dict = pytrend.related_topics()
print(related_topics_dict)
print()

# Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrend.related_queries()
print(related_queries_dict)
print()

# Get Google Hot Trends data
trending_searches_data = pytrend.trending_searches(pn='ghana') # trending searches in real time for Ghana
#print(trending_searches_data.head())
print(trending_searches_data)
print()

# Get Google Top Charts. Can also specify date as so: "date=201912"
top_charts_data = pytrend.top_charts(cid='Ghana Music', date=2019, hl='en-US', tz=300, geo='GLOBAL')
#print(top_charts_data.head())
print(top_charts_data)
print()

# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword='Ghana')
print(suggestions_dict)
print()
