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
import json
import plotly
import plotly.offline as offline
import matplotlib.pyplot as plt
import pandas as pd
from covid import Covid

pd.set_option('display.max_rows', 100)

#source="worldometers"
source="john_hopkins"
#cov_19 = Covid() # Default is John Hopkins data.
cov_19 = Covid(source)
#data = cov_19.get_data()
country_list = cov_19.list_countries()
#print(country_list)
#print()

data = pd.DataFrame(country_list)
#print(data)
#print()

# Example output:
#
# 149 Sao Tome and Principe
# {'id': '149', 'country': 'Sao Tome and Principe', 'confirmed': 4, 'active': 4, 'deaths': 0, 'recovered': 0, 'latitude': 0.18636, 'longitude': 6.613081, 'last_update': 1587655832000}
for row in data.itertuples(index=True, name='Pandas'):
    country_id = getattr(row, "id")
    country_name = getattr(row, "name")
    print(country_id, country_name)
    data = cov_19.get_status_by_country_name(str(country_name))
    print(data)
    print()

