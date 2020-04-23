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

#source="worldometers"
source="john_hopkins"
#cov_19 = Covid() # Default is John Hopkins data.
cov_19 = Covid(source)
#data = cov_19.get_data()
countries = cov_19.list_countries()
print(countries)
print()

if source == "worldometers":
    data = cov_19.get_status_by_country_name("USA")
    print(data)
    print()
    
    data = cov_19.get_status_by_country_name("Ghana")
    print(data)
    print()
    
    data = cov_19.get_status_by_country_name("Cameroon")
    print(data)
    print()
    
    data = cov_19.get_status_by_country_name("car")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Ecuador")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Brazil")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Cuba")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Jamaica")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Greece")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("New Zealand")
    print(data)
    print()
else:
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

    data = cov_19.get_status_by_country_name("Ecuador")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Brazil")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Cuba")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Jamaica")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("Greece")
    print(data)
    print()

    data = cov_19.get_status_by_country_name("New Zealand")
    print(data)
    print()
