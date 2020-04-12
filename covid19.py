#***********************************************************************
# @file
#
# Python script for querying World Bank COVID-19 Statistics.
#
# @note 
#
# @warning  None
#
#  Created: April 12, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/  
#import time
#import pandas as pd
#import pandas_datareader as wb
#import matplotlib.pyplot as plt

import pandas as pd
import plotly
import plotly.offline as offline
import world_bank_data as wb

def version_to_int_list(version):
    return [int(s) for s in version.split('.')]

assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'

pd.set_option('display.max_rows', 100)

#topics = wb.get_topics()
#print(topics)
#print()
#
#sources = wb.get_sources()
#print(sources)
#print()
#
#indicators = wb.get_indicators(topic=3, source=2)
#print(indicators)
#print()

#deaths = wb.search_indicators('deaths')
#print(deaths)
#print()

# Birth rate, crude (per 1,000 people)
#births = wb.search_indicators('births')
#print(births)
#print()

#covid19_indicators = wb.search_indicators('COVID-19 Cases')
#print(covid19_indicators)
#print()

# Population dataset, by the World Bank (most recent value) indexed with the country code:
#population = wb.get_series('SP.POP.TOTL', id_or_value='id', simplify_index=True, mrv=1)
#print(population)
#print()

# Countries and associated regions
#countries = wb.get_countries()
#print(countries)
#print()
