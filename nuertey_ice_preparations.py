#***********************************************************************
# @file
#
# Python script for querying various market statistics via the Quandl API.
# Mainly I am assaying to query Intercontinental Exchange databases in 
# order to prepare myself for an interview that I have coming up with them.
#
# @note     None
#
# @warning  None
#
#  Created: May 14th, 2020
#   Author: Nuertey Odzeyem, [Yet in the middle of Despair, thou shalt 
#           strive and grasp for Hope.]
#**********************************************************************/
import io
import quandl
import base64
import matplotlib.pyplot as plt

# Free quandl API key:
token = open(".quandl_token").read()

# International prices of imported raw materials - Ivory Coast cocoa - 
# ICE (InterContinental Exchange), Atlanta - Price in US dollars per 
# tonne (Monthly).
data = quandl.get("INSEE/010002048", authtoken=token)
print(data)
print()

print('Data type of each column of data:')
print(data.dtypes)
print()

# International prices of imported raw materials - Gold, LME 
# (London Metal Exchange), London - Price in US dollars per troy ounce 
# (Monthly)

#retrieve stock data from quandl
#data = quandl.get('WIKI/AAPL', collapse = 'monthly')
#plt.style.use("ggplot")
#
##average of 99 days price
#data['100mean'] = data['Adj. Close'].rolling(window=100, min_periods=0).mean()
#
##I have created two plots in a single graph here
#axis1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
#axis2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
#
#axis1.plot(data.index, data['Adj. Close'])
#axis1.plot(data.index, data['100mean'])
#axis1.plot(data.index, data['High'])
#
#axis2.plot(data.index, data['Volume'])
#
#plt.title('Forex Daily Prices - US Dollars to Ghanaian Cedis')
#ax1 = data['3. low'].plot(color='blue', grid=True, label='low')
#ax2 = data['2. high'].plot(color='red', grid=True, secondary_y=True, label='high')
#ax3 = data['4. close'].plot(color='green', grid=True, secondary_y=True, label='close')
#ax1.legend(loc=1)
#ax2.legend(loc=2)
#ax3.legend(loc=3)
#plt.show()
