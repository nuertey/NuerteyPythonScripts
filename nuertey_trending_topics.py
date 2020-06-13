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
from pytrends.request import TrendReq

pd.set_option('display.max_rows', 100)

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Returns Categories dictionary for potential usage in help text.
all_categories = pytrends.categories()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
pytrend.build_payload(kw_list=['Ghana', 'palm oil'])

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

# Get Google Top Charts
top_charts_data = pytrend.top_charts(cid='Ghana Music', date=201912, hl='en-US', tz=300, geo='GLOBAL')
#print(top_charts_data.head())
print(top_charts_data)
print()

# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword='Ghana')
print(suggestions_dict)
print()
