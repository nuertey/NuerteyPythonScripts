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
import pandas as pd

pd.set_option('display.max_rows', 100)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-h] | [-v] | [-c country] | [-t topic] [-b begin_date]",
        description="Nuertey's News Aggregator. What is a country talking about most today? Or, what is the world talking about concerning a particular topic beginning from a particular date till now?",
        allow_abbrev=False,
        add_help=True
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 0.0.1"
    )
    parser.add_argument(
        "-c", "--country", action='store',
        type=str,
        help="Specify the country whose top news headlines you want to see."
    )
    parser.add_argument(
        "-t", "--topic", action='store',
        type=str,
        help="Specify the topic you are interested in."
    )
    parser.add_argument(
        "-b", "--begin_date", action='store', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help="Specify the beginning date from which to query for all news articles. Format: yyyy-mm-dd"
    )
    return parser

parser = init_argparse()
args = parser.parse_args()
country = args.country
topic = args.topic
begin_date = args.begin_date

print(country)
print()

print(topic)
print()

print(begin_date)
print()

if country is None and topic is None:
    print("No primary arguments specified. Exiting...")
    sys.exit()
elif country is not None:
    print("Querying for {0} top news headlines...".format(country.capitalize()))
    token = open(".newsapi_token").read().rstrip('\n')
    print(token)
    print()
elif topic is not None and begin_date is not None:
    print("Querying all world-wide news headlines for topics on \"{0}\" from {1} till now...".format(topic, begin_date))
    token = open(".newsapi_token").read().rstrip('\n')
    print(token)
    print()
elif topic is not None:
    print("Querying all world-wide news headlines for topics on \"{0}\"...".format(topic))
    token = open(".newsapi_token").read().rstrip('\n')
    print(token)
    print()

# Accept argument input for either a country's top headlines or a topic discussed worldwide.

# Top news by country
# All world-wide news concerning a topic from a beginning period to present 

# Live news articles on the 'COVID-19' topic via newsapi much like follows:
#
#https://newsapi.org/v2/top-headlines?country=us&apiKey=f048819049c24d6d86bd424daa2349f1
#
#http://newsapi.org/v2/everything?q=ghana&from=2020-01-01&sortBy=publishedAt&apiKey=f048819049c24d6d86bd424daa2349f1
#
# NEWS_API_KEY = config("NEWS_API_KEY")
# NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
#
# Notice the use of the python 3.6 introduced f-strings in the statement
# above. F-strings can be further explained by this code snippet:
#
# >>> name = "Adjoa"
# >>> age = 15
# >>> f"Hello, {name}. You are {age}."
# 'Hello, Adjoa. You are 15.'
