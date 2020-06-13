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
import time
import datetime
import pycountry
import pytrends
import pandas as pd
from datetime import datetime, date, time
from pytrends.request import TrendReq

# Run output of script for Emile on topics trending in Cameroon by region
# ISO-3166-2 and on the category, "politics". Plot it.

# Also run output of script for Emile on Cameroon as a topic trending 
# by Country (ISO-3166-1) world-wide for 20 years. Plot it. 
#
# country_name = pycountry.countries.get({country_code}).name

pd.set_option('display.max_rows', 100)

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Returns Categories dictionary for potential usage in help text.
all_categories = pytrends.categories()

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
#       -g denotes Google Trends Categories listing (list of 1427 category entries will be displayed in help text)
#       -t denotes a trending topic keyword of interest

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
pytrend.build_payload(kw_list=['bofrot', 'palm oil', 'fried rice', 'somanya', 'pojoss'], timeframe='today 10-y', geo = 'GH')

# Interest Over Time
interest_over_time_data = pytrend.interest_over_time()
#print(interest_over_time_data.head())
print(interest_over_time_data)
print()

# Interest by Region
interest_by_region_data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
#print(interest_by_region_data.head())
print(interest_by_region_data)
print()

#interest_by_region_data.reset_index().plot(x=’geoName’, y=’Taylor Swift’, figsize=(120, 10), kind =’bar’)

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
