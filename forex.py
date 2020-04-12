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
r = requests.get('https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=USD&to_symbol=GHS&outputsize=compact&apikey=MZ9Q5U40PRWBMA6T')

if r.ok:
    # The response fields...:
    print("HTTP Response Status Code:-> ", r.status_code)
    print("HTTP Response Content Type:-> ", r.headers['content-type'])
    print("HTTP Response Encoding:-> ", r.encoding)
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
    #timeSeriesFX = pandas.DataFrame.from_dict(r.json())
    
    # This way fails interpretation with the following error:
    #
    # ValueError: Invalid file path or buffer object type: <class 'dict'>
    #timeSeriesFX = pandas.read_json(r.json())
    #timeSeriesFX = timeSeriesFX.set_index("date")
    
    #print("1. Information: ", timeSeriesFX['Meta Data']['1. Information'])
    #print("2. From Symbol: ", timeSeriesFX['Meta Data']['2. From Symbol'])
    #print("3. To Symbol: ", timeSeriesFX['Meta Data']['3. To Symbol'])
    #print("4. Last Refreshed: ", timeSeriesFX['Meta Data']['4. Last Refreshed'])
    #print("5. Time Zone: ", timeSeriesFX['Meta Data']['5. Time Zone'])
    #print()
    
    #timeSeriesFX.head() # This will give us the first 5 lines of data
    #timeSeriesFX.tail() #This will give us the last 5 lines of data
    
    #print(timeSeriesFX['Time Series FX (Weekly)'])
    #print()
    
    fe = ForeignExchange(key=API_KEY, output_format='pandas')
    data, meta_data = fe.get_currency_exchange_daily(from_symbol='USD', to_symbol='GHS', outputsize='full')
    
    #print(meta_data)
    #print()

    print("1. Information: ", meta_data['1. Information'])
    print("2. From Symbol: ", meta_data['2. From Symbol'])
    print("3. To Symbol: ", meta_data['3. To Symbol'])
    print("4. Output Size: ", meta_data['4. Output Size'])
    print("5. Last Refreshed: ", meta_data['5. Last Refreshed'])
    print("6. Time Zone: ", meta_data['6. Time Zone'])
    print()
    
    #print(data)
    #print()
    #data['4. close'].plot()
    #data['4. close'].plot()
    #plt.title('Forex Daily Prices - US Dollars to Ghanaian Cedis')
    #plt.show()

    #plt.figure(figsize=(12,5))
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
    
    #print(data)
    #print()
    
    data['4. close'].plot()
    plt.title('Intraday Times Series for the MSFT stock (1 min)')
    plt.show()
    
    # How to reset the index of a DataFrame
    #Dataset.dropna(inplace=True)
else:
    print('Error! Issue with the URL, HTTP Request, and/or the HTTP Response')
