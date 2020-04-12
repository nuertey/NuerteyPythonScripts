#***********************************************************************
# @file
#
# Python utility for querying FOREX Currency Exchanges, and stock 
# intraday time series.
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
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import matplotlib.pyplot as plt

# Forex: Alpha Vantage provides realtime currency exchange rates 
# (for physical and digital currencies). Below is the access key that 
# they granted me for Software Development purposes:
API_KEY = 'MZ9Q5U40PRWBMA6T'
os.environ["ALPHAVANTAGE_API_KEY"] = "MZ9Q5U40PRWBMA6T"

print('\t\tTime now:-> %s\n' % time.ctime())

# Retrieve realtime United States Dollar to Ghana Cedi (USD/GHS),
# Cameroon Central African CFA Franc BEAC, Chinese Yuan, Japanese Yen, etc. 
# exchange rates and multiple other Bitcoin exchange rate pairs:
forex = pdr.DataReader(["USD/GHS", "USD/XAF", "BTC/GHS"], "av-forex", 
                        api_key=os.getenv('ALPHAVANTAGE_API_KEY'))
print(forex)
print()

########################################################################
# Note that when using Alpha Vantage, the standard API call frequency is
# 5 calls per minute and 500 calls per day.
########################################################################    
fe = ForeignExchange(key=API_KEY, output_format='pandas')
data, meta_data = fe.get_currency_exchange_daily(from_symbol='USD', to_symbol='GHS', outputsize='full')

print("1. Information: ", meta_data['1. Information'])
print("2. From Symbol: ", meta_data['2. From Symbol'])
print("3. To Symbol: ", meta_data['3. To Symbol'])
print("4. Output Size: ", meta_data['4. Output Size'])
print("5. Last Refreshed: ", meta_data['5. Last Refreshed'])
print("6. Time Zone: ", meta_data['6. Time Zone'])
print()

plt.title('Forex Daily Prices - US Dollars to Ghanaian Cedis')
ax1 = data['3. low'].plot(color='blue', grid=True, label='low')
ax2 = data['2. high'].plot(color='red', grid=True, secondary_y=True, label='high')
ax3 = data['4. close'].plot(color='green', grid=True, secondary_y=True, label='close')
ax1.legend(loc=1)
ax2.legend(loc=2)
ax3.legend(loc=3)
plt.show()

ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')

print("1. Information: ", meta_data['1. Information'])
print("2. Symbol: ", meta_data['2. Symbol'])
print("3. Last Refreshed: ", meta_data['3. Last Refreshed'])
print("4. Interval: ", meta_data['4. Interval'])
print("5. Output Size: ", meta_data['5. Output Size'])
print()

plt.title('Intraday Times Series for the MSFT stock (1 min)')
ax1 = data['3. low'].plot(color='blue', grid=True, label='low')
ax2 = data['2. high'].plot(color='red', grid=True, secondary_y=True, label='high')
ax3 = data['4. close'].plot(color='green', grid=True, secondary_y=True, label='close')
ax1.legend(loc=1)
ax2.legend(loc=2)
ax3.legend(loc=3)
plt.show()
