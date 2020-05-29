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
from http import HTTPStatus
from argparse import RawTextHelpFormatter
from nuertey_news_config import NEWS_API_COUNTRY_CODES

pd.set_option('display.max_rows', 100)

country_codes = pd.DataFrame(NEWS_API_COUNTRY_CODES)

# parser.choices seems to better prefer dict objects to strings. 
# Better input matching and option display:
codes_dictionary = country_codes.to_dict('list') 
#print(codes_dictionary)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-h] | [-v] | [-c country] | [-t topic] [-b begin_date]",
        description="Welcome, Velkommen, Woé zɔ, Karibu, Mo-heee to Nuertey's News Aggregator. What is a country talking about most today? \nOr, what is the world talking about concerning a particular topic beginning from a particular date till now? \nWhat do you want to know? Ask me in the format below:",
        epilog="Enjoy using Nuertey's News Aggregator to latch upon the World's pulse!",
        formatter_class=RawTextHelpFormatter,
        allow_abbrev=False,
        add_help=True
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 0.0.3"
    )
    parser.add_argument(
        "-c", "--country", action='store', choices=codes_dictionary['code'],
        help="\nSpecify the country whose top news headlines you want to see. Where country MUST be denoted by one of the country codes from the \npossible News API range of countries below. Per News API design, these are the ONLY possible countries that News API curates \ntop headlines for: \n\n{0}\n".format(country_codes.to_string(index=False)),
        metavar='COUNTRY_CODE_FROM_LIST_BELOW'
    )
    parser.add_argument(
        "-t", "--topic", action='store',
        type=str,
        help="Specify the topic you are interested in world-wide."
    )
    parser.add_argument(
        "-b", "--begin_date", action='store', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help="Specify the beginning date from which to query for all news articles. Note that as we are using a \nfree News API subscription, date CANNOT be older than 2020-04-27. Date format is: yyyy-mm-dd"
    )
    return parser

parser = init_argparse()
args = parser.parse_args()
country = args.country
topic = args.topic
begin_date = args.begin_date

if country is None and topic is None:
    print()
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
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
            # Concat the above to the DataFrame in place of the dict col:
            dict_col = data.pop('source')
            #pd.concat([data, sources['name']], axis=0)
            #data.append(sources['name'])

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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()

    print()
    print("Querying for {0} Business news headlines...".format(culprit_country_name))
    print()
    news_api_url = f"http://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()

    print()
    print("Querying for {0} Technology news headlines...".format(culprit_country_name))
    print()
    news_api_url = f"http://newsapi.org/v2/top-headlines?country={country}&category=technology&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()

    print()
    print("Querying for {0} Health news headlines...".format(culprit_country_name))
    print()
    news_api_url = f"http://newsapi.org/v2/top-headlines?country={country}&category=health&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()

    print()
    print("Querying for {0} Science news headlines...".format(culprit_country_name))
    print()
    news_api_url = f"http://newsapi.org/v2/top-headlines?country={country}&category=science&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()

    print()
    print("Querying for {0} Entertainment news headlines...".format(culprit_country_name))
    print()
    news_api_url = f"http://newsapi.org/v2/top-headlines?country={country}&category=entertainment&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()

    print()
    print("Querying for {0} Sports news headlines...".format(culprit_country_name))
    print()
    news_api_url = f"http://newsapi.org/v2/top-headlines?country={country}&category=sports&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()
elif topic is not None and begin_date is not None:
    the_date_alone = begin_date.strftime('%Y-%m-%d')
    print()
    print("Querying all world-wide news headlines for topics on \"{0}\" from {1} till now...".format(topic, the_date_alone))
    token = open(".newsapi_token").read().rstrip('\n')
    news_api_url = f"https://newsapi.org/v2/everything?q={topic}&from={the_date_alone}&sortBy=publishedAt&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            
            # Concat the above to the DataFrame in place of the dict col:
            dict_col = data.pop('source')
            #pd.concat([data, sources['name']], axis=0)

            pd.set_option('display.max_colwidth', -1)        
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()
elif topic is not None:
    print()
    print("Querying all world-wide news headlines for topics on \"{0}\" ...".format(topic))
    token = open(".newsapi_token").read().rstrip('\n')
    news_api_url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&apiKey={token}"
    reply = requests.get(news_api_url)
    if reply.ok:
        text_data = reply.text
        json_dict = json.loads(text_data)
        if json_dict["totalResults"] > 0:
            data = pd.DataFrame.from_dict(json_dict["articles"])
            sources = data['source'].apply(pd.Series)
            #print(sources)
            #print()
            
            # Concat the above to the DataFrame in place of the dict col:
            dict_col = data.pop('source')
            #pd.concat([data, sources['name']], axis=0)

            pd.set_option('display.max_colwidth', -1)        
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
        print(f'{reply.status_code} :-> {HTTPStatus(reply.status_code).phrase}')
        print()
        reply_json = json.loads(reply.text)
        print(json.dumps(reply_json, indent=2))
        sys.exit()
