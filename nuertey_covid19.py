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
import plotly
import plotly.offline as offline
import matplotlib.pyplot as plt
import pandas as pd
from covid import Covid

pd.set_option('display.max_rows', 100)

#cov_19 = Covid("worldometers")
cov_19 = Covid() # Default is John Hopkins data.
#data = cov_19.get_data()
#countries = cov_19.list_countries()
#print(countries)
#print()

data = cov_19.get_status_by_country_name("US")
print(data)
print()

data = cov_19.get_status_by_country_name("Ghana")
print(data)
print()

data = cov_19.get_status_by_country_name("Cameroon")
print(data)
print()

data = cov_19.get_status_by_country_name("Central African Republic")
print(data)
print()

#us_cases = cov_19.get_status_by_country_name("US")
#ghana_cases = cov_19.get_status_by_country_name("Ghana")
#cameroon_cases = cov_19.get_status_by_country_name("Cameroon")
#caf_cases = cov_19.get_status_by_country_name("Central African Republic")

#print(us_cases)
#print()
#print(ghana_cases)
#print()
#print(cameroon_cases)
#print()
#print(caf_cases)
#print()
