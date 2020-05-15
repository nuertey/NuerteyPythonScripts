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
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import plotly.graph_objects as go
import plotly.express as px

# Quandl has a vast collection of free and open data collected from a 
# variety of organizations: central banks, governments, multinational 
# organizations and more. You can use it without payment and with few 
# restrictions.
#
# Rate limits
#
# Authenticated users have a limit of 300 calls per 10 seconds, 
# 2,000 calls per 10 minutes and a limit of 50,000 calls per day.
#
# Authenticated users of free datasets have a concurrency limit of one; 
# that is, they can make one call at a time and have an additional call
# in the queue.

# Free quandl API key:
token = open(".quandl_token").read().rstrip('\n')

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

# Notwithstanding the notion being quite quaint and subjective, the 
# following matplotlib styles seem interesting to me:
#
# classic, ggplot, seaborn-bright, seaborn-dark 
#plt.style.use("ggplot")
#
#plt.title('International Prices of Imported Ivory Coast Cocoa - InterContinental Exchange')
#plt.xlabel("Date")
#plt.ylabel("Price (US dollars per tonne)")
#plt.plot(data.index, data['Value'], "-r", label="Price in US dollars per tonne (Monthly)")
#plt.legend(loc="upper left")
##plt.ylim(-1.5, 2.0)
#plt.show()

#figure = px.line(data, x=data.index, y='Value', title='International Prices of Imported Ivory Coast Cocoa - InterContinental Exchange')
#figure.show()

#fig = go.Figure([go.Scatter(x=data.index, y=data['Value'])])
#fig.show()

figure = go.Figure()
# Create and style traces:
figure.add_trace(go.Scatter(x=data.index, 
                            y=data['Value'],
                            mode='lines+markers',
                            name='Price in US dollars per tonne (Monthly)',
                            line=dict(color='firebrick', width=4,
                            dash='dash') # dash options include 'dash', 'dot', and 'dashdot'
))

# Edit the layout
figure.update_layout(title='International Prices of Imported Ivory Coast Cocoa - InterContinental Exchange',
                     xaxis_title='Date',
                     yaxis_title='Price in US dollars per tonne (Monthly)')
figure.show()
