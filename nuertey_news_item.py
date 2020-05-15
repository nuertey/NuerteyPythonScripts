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
import pandas as pd

pd.set_option('display.max_rows', 100)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-h] | [-v] | [-c country] | [-t topic from_date]",
        description="Nuertey's News Aggregator. What is a country talking about? Or, what is the world talking about concerning a particular topic?",
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
        help="Specify the topic you are interested in and the date from which to query all news articles."
    )
    return parser

parser = init_argparse()
args = parser.parse_args()
country = args.country
topic = args.topic

print(country)
print()

print(topic)
print()

#if not args.download:
#    if not os.path.isfile(data_source_file_name):
#        print("The data source file specified \"{0}\" does not exist".format(data_source_file_name))
#        sys.exit()
#else:
#    source = "john_hopkins"  # Currently, the only source supported by this script.
#    cov_19 = Covid(source)
#
#token = open(".newsapi_token").read().rstrip('\n')

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
