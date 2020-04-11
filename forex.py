#***********************************************************************
# @file
#
# Python utility for querying FOREX Currency Exchanges.
#
# @note 
#
# @warning  None
#
#  Created: April 11, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import io
import os   
import time
import requests
import pandas
import pandas_datareader as pdr

# Forex: Alpha Vantage provides realtime currency exchange rates 
# (for physical and digital currencies). Below is the access key that 
# they granted me for Software Development purposes:
os.environ["ALPHAVANTAGE_API_KEY"] = "MZ9Q5U40PRWBMA6T"
#print(os.environ["ALPHAVANTAGE_API_KEY"])

print('\t\tTime now:-> %s\n' % time.ctime())

# Retrieve realtime United States Dollar to Ghana Cedi (USD/GHS),
# Cameroon Central African CFA Franc BEAC, Chinese Yuan, Japanese Yen, etc. 
# exchange rates and multiple other Bitcoin exchange rate pairs:
#forex = pdr.DataReader(["USD/XAF", "USD/GHS", "USD/CNY",
#                        "BTC/CNY", "BTC/USD"], "av-forex", 
#                        api_key=os.getenv('ALPHAVANTAGE_API_KEY'))
#print(forex)
print()

########################################################################
# Note that when using Alpha Vantage, the standard API call frequency is
# 5 calls per minute and 500 calls per day.
########################################################################

# Behold, the power of Requests:
#r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
r = requests.get('https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=USD&to_symbol=GHS&outputsize=full&apikey=MZ9Q5U40PRWBMA6T')

# The response fields...:
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)
#print(r.text)
#print(r.json())
print()

# This way fails interpretation with the following error:
#
# pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 3, saw 5
#timeSeriesFX = pandas.read_csv(io.StringIO(r.content.decode('utf-8')))

# This way fails interpretation with the following error:
#
# pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 3, saw 5
#timeSeriesFX = pandas.read_csv(io.StringIO(r.text))

# This way fails interpretation with the following error:
#
# TypeError: initial_value must be str or None, not Response
#timeSeriesFX = pandas.read_csv(io.StringIO(r))

# This way seems to work, though with some output NaN values and in strictly JSON format:
#timeSeriesFX = pandas.read_json(r.text)

# This way works; also in strictly JSON format:
timeSeriesFX = pandas.DataFrame.from_dict(r.json())

# This way fails interpretation with the following error:
#
# ValueError: Invalid file path or buffer object type: <class 'dict'>
#timeSeriesFX = pandas.read_json(r.json())
print(timeSeriesFX)
