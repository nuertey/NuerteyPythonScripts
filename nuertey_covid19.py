#***********************************************************************
# @file
#
# Python script for querying COVID-19 statistics via several publicly
# available APIs.
#
# @note 
#
# @warning  None
#
#  Created: April 12, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/  
import time
import requests
import pandas
import pandas_datareader as pdr
import pandas as pd
import plotly
import plotly.offline as offline
import matplotlib.pyplot as plt
import pydantic
from covid import Covid

#help(covid)
#print()
#dir(covid)

# type: "GET",
# dataType:"json",
COVID_19_API_1 = 'https://thevirustracker.com/free-api?countryTotals=ALL'

# End point:
# URL                           Method  Description
# api/ncov/all                  GET     get all country data
# api/ncov/countrylist          GET     get all list of country affected by NCOV
# api/ncov/country/{country}    GET     get data by country
COVID_19_API_2 = 'https://www.worldometers.info/coronavirus/country/ghana'

r = requests.get(COVID_19_API_1)

if r.ok:
    print("HTTP Response Status Code:-> ", r.status_code)
    print("HTTP Response Content Type:-> ", r.headers['content-type'])
    print("HTTP Response Encoding:-> ", r.encoding)
    print()

    data = pandas.DataFrame.from_dict(r.json())
    #print(r.text)
    print(data)
    print()
else:
    print('Error! Issue with the URL, HTTP Request, and/or the HTTP Response')

cov = covid.Covid(source="worldometers")
#covid = covid.Covid()
data = cov.get_data()
print(data)
print()
