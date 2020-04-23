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
import world_bank_data as wb
from covid import Covid

pd.set_option('display.max_rows', 100)

#source="worldometers"
source="john_hopkins"
#cov_19 = Covid() # Default is John Hopkins data.
cov_19 = Covid(source)
#data = cov_19.get_data()
#country_list = cov_19.list_countries()
#print(countries)
#print()

# Workaround for bug:
#
# https://stackoverflow.com/questions/25610592/how-to-set-dtypes-by-column-in-pandas-dataframe
#data = pd.DataFrame.from_dict(countries).astype({0: int, 1:str})
#data = pd.DataFrame({'id':pd.Series(countries['id'], dtype='int'),
#                   'name':pd.Series(countries['name'], dtype='string')})
#json_dict = json.loads(countries)
print(country_list[1])
print()

countries = []
for country in country_list:
    countries.append(country['name'])
print(countries)

data = pd.DataFrame.from_dict(country_list)
print(data)
print()

sorted_data = data.sort_values(by=['id'], ascending=True)
print(sorted_data)
print()

#for row in df.itertuples(index=True, name='Pandas'):
#    print getattr(row, "c1"), getattr(row, "c2")
#
#for country in countries['name']:
#    print(data)
#    data = cov_19.get_status_by_country_name(str(country))
#    print(data)
#    print()

#if source == "worldometers":
#    data = cov_19.get_status_by_country_name("USA")
#    print(data)
#    print()
#    
#    data = cov_19.get_status_by_country_name("Ghana")
#    print(data)
#    print()
#    
#    data = cov_19.get_status_by_country_name("Cameroon")
#    print(data)
#    print()
#    
#    data = cov_19.get_status_by_country_name("car")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Ecuador")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Brazil")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Cuba")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Jamaica")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Greece")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("New Zealand")
#    print(data)
#    print()
#else:
#    data = cov_19.get_status_by_country_name("US")
#    print(data)
#    print()
#    
#    data = cov_19.get_status_by_country_name("Ghana")
#    print(data)
#    print()
#    
#    data = cov_19.get_status_by_country_name("Cameroon")
#    print(data)
#    print()
#    
#    data = cov_19.get_status_by_country_name("Central African Republic")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Ecuador")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Brazil")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Cuba")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Jamaica")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("Greece")
#    print(data)
#    print()
#
#    data = cov_19.get_status_by_country_name("New Zealand")
#    print(data)
#    print()
