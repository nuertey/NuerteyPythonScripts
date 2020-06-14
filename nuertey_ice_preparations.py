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
#           strive and graft onto Hope.]
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

# National Institute of Statistics and Economic Studies (France) data:
#
# INSEE is the national statistical agency of France. It collects data
# on France's economy and society, such as socioeconomic indicators and
# national accounts.

# International prices of imported raw materials - Ivory Coast cocoa - 
# ICE (InterContinental Exchange), Atlanta - Price in US dollars per 
# tonne (Monthly).
data = quandl.get("INSEE/010002048", authtoken=token)
print(data)
print()

#print('Data type of each column of data:')
#print(data.dtypes)
#print()

data_source_file_name = "ivory_coast_cocoa-intercontinental_exchange.csv"
data.to_csv(data_source_file_name, index = True, header=True)

# International prices of imported raw materials - Arabica coffee 
# Contract C ICE (InterContinental Exchange), Atlanta - Price in US 
# cents per pound (Monthly).
coffee = quandl.get("INSEE/010002042", authtoken=token)
print(coffee)
print()

# International prices of imported raw materials - Gold, LME 
# (London Metal Exchange), London - Price in US dollars per troy ounce 
# (Monthly)
gold = quandl.get("INSEE/010002061", authtoken=token)
print(gold)
print()

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
figure.add_trace(go.Scatter(x=data.index, 
                            y=data['Value'],
                            mode='lines+markers',
                            name='Price in US dollars per tonne (Monthly)',
                            line=dict(color='red', width=1)
))
figure.update_layout(title='International Prices of Imported Ivory Coast Cocoa - InterContinental Exchange',
                     xaxis_title='Date',
                     yaxis_title='Price in US dollars per tonne (Monthly)')
figure.show()

figure = go.Figure()
figure.add_trace(go.Scatter(x=coffee.index, 
                            y=coffee['Value'],
                            mode='lines+markers',
                            name='Price in US cents per pound (Monthly)',
                            line=dict(color='red', width=1)
))
figure.update_layout(title='International Prices of Imported Arabica Coffee Contract C - InterContinental Exchange',
                     xaxis_title='Date',
                     yaxis_title='Price in US cents per pound (Monthly)')
figure.show()

figure = go.Figure()
figure.add_trace(go.Scatter(x=gold.index, 
                            y=gold['Value'],
                            mode='lines+markers',
                            name='Price in US dollars per troy ounce (Monthly)',
                            line=dict(color='red', width=1)
))
figure.update_layout(title='International Prices of  Gold - LME (London Metal Exchange) Exchange',
                     xaxis_title='Date',
                     yaxis_title='Price in US dollars per troy ounce (Monthly)')
figure.show()
