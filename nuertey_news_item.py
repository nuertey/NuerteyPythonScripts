#***********************************************************************
# @file
#
# Python script for interrogating the news per top headlines in any 
# country, or per particular topic worldwide. That is, "What is the whole  
# world talking about at this instant, and on this topic?"
#
# @note     None
#
# @warning  None
#
#  Created: May 15, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import os
import sys
import argparse
import datetime
import re
import requests
import json
import pandas as pd
from argparse import RawTextHelpFormatter
from nuertey_news_config import NEWS_API_COUNTRY_CODES

pd.set_option('display.max_rows', 100)
#pd.set_option('display.max_colwidth', -1)

country_codes = pd.DataFrame(NEWS_API_COUNTRY_CODES)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-h] | [-v] | [-c country] | [-t topic] [-b begin_date]",
        description="Welcome, Velkommen, Woé zɔ, Karibu, Mo-heee to Nuertey's News Aggregator. What is a country talking about most today? \nOr, what is the world talking about concerning a particular topic beginning from a particular date till now? \nWhat do you want to know? Ask me in the format below:",
        formatter_class=RawTextHelpFormatter,
        allow_abbrev=False,
        add_help=True
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 0.0.2"
    )
    parser.add_argument(
        "-c", "--country", action='store', choices=str(country_codes['code']),
        type=str,
        help="\nSpecify the country whose top news headlines you want to see. Where country MUST be denoted by one of the country codes from the \npossible News API range of countries below. By design limitations, these are the ONLY possible countries that News API curates \ntop headlines for: \n\n{0}".format(country_codes.to_string(index=False))
    )
    parser.add_argument(
        "-t", "--topic", action='store',
        type=str,
        help="Specify the topic you are interested in world-wide."
    )
    parser.add_argument(
        "-b", "--begin_date", action='store', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help="Specify the beginning date from which to query for all news articles. Date format is: yyyy-mm-dd"
    )
    return parser

parser = init_argparse()
args = parser.parse_args()
country = args.country
topic = args.topic
begin_date = args.begin_date

if country is None and topic is None:
    print("No primary arguments specified. Exiting...")
    sys.exit()
elif country is not None:
    culprit_country_name = country_codes.loc[country_codes['code'] == country,'country']
    culprit_country_name = next(iter(culprit_country_name), 'no match')
    print()
    print("Querying for {0} top news headlines...".format(culprit_country_name))
    print()
    token = open(".newsapi_token").read().rstrip('\n')
    news_api_url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        #print(json_dict)
        #print()
        #print(json_dict["totalResults"])
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            #print(sources)
            #print()
            
            # Concat the above to the DataFrame in place of the dict col:
            dict_col = data.pop('source')
            #pd.concat([data, sources['name']], axis=0)

            pd.set_option('display.max_colwidth', -1)        
            #print(data[['publishedAt', 'content', 'url']])
            print(data[['publishedAt', 'title']])
            print()
            print("And here are the URLS of the above articles for your reference:")
            print()
            print(data[['url']])
            print()
            print(data.columns)
        else:
            print("Sorry. No online news articles were discovered for \"{0}\". Check meatspace.".format(culprit_country_name))
            sys.exit()
    else:
        print('Error! Issue with the URL, HTTP Request, and/or the HTTP Response')
        sys.exit()
elif topic is not None and begin_date is not None:
    the_date_alone = begin_date.strftime('%Y-%m-%d')
    print(the_date_alone)
    print()
    print("Querying all world-wide news headlines for topics on \"{0}\" from {1} till now...".format(topic, the_date_alone))
    token = open(".newsapi_token").read().rstrip('\n')
    news_api_url = f"https://newsapi.org/v2/everything?q={topic}&from={the_date_alone}&sortBy=publishedAt&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        #print(json_dict)
        #print()
        #print(json_dict["totalResults"])
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            #print(sources)
            #print()
            
            # Concat the above to the DataFrame in place of the dict col:
            dict_col = data.pop('source')
            #pd.concat([data, sources['name']], axis=0)

            pd.set_option('display.max_colwidth', -1)        
            #print(data[['publishedAt', 'content', 'url']])
            print(data[['publishedAt', 'title']])
            print()
            print("And here are the URLS of the above articles for your reference:")
            print()
            print(data[['url']])
            print()
            print(data.columns)
        else:
            print("Sorry. No online news articles were discovered for \"{0}\". Check meatspace.".format(topic))
            sys.exit()
    else:
        print('Error! Issue with the URL, HTTP Request, and/or the HTTP Response')
        sys.exit()
elif topic is not None:
    print("Querying all world-wide news headlines for topics on \"{0}\"...".format(topic))
    token = open(".newsapi_token").read().rstrip('\n')
    print(token)
    print()

#country_business_news = "http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=" + api_key_newsapi,
#country_tech_news = "http://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=" + api_key_newsapi,
#country_health_news = "http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=" + api_key_newsapi,
#country_science_news = "http://newsapi.org/v2/top-headlines?country=us&category=science&apiKey=" + api_key_newsapi,
#country_entertainment_news = "http://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=" + \
#                            api_key_newsapi,
#country_sports_news = "http://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=" + \
#                            api_key_newsapi,
