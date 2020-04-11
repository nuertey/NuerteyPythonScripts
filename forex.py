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
import os   
import time
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
forex = pdr.DataReader(["USD/GHS", "USD/XAF", "USD/CNY", "USD/JPY",
                        "BTC/CNY", "BTC/USD"], "av-forex", 
                        api_key=os.getenv('ALPHAVANTAGE_API_KEY'))
print(forex)
print()
