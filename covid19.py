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
import time
import pandas as pd
import plotly
import plotly.offline as offline
import world_bank_data as world_bank
from pandas_datareader import wb
import matplotlib.pyplot as plt

def version_to_int_list(version):
    return [int(s) for s in version.split('.')]

assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'

pd.set_option('display.max_rows', 100)

# Birth rate, crude (per 1,000 people) indexed with the country code:
births = world_bank.get_series('SP.DYN.CBRT.IN', id_or_value='id', simplify_index=True, mrv=1)
#print(births)
#print()

# Death rate, crude (per 1,000 people) indexed with the country code:
deaths = world_bank.get_series('SP.DYN.CDRT.IN', id_or_value='id', simplify_index=True, mrv=1)
#print(deaths)
#print()

# Population ages 15-64 (% of total population)
# SP.POP.1564.TO.ZS
pop64 = wb.download(indicator='SP.POP.1564.TO.ZS', country=['US'], start=1990, end=2020)
print(pop64)
print()

# Population ages 65 and above (% of total population)
# SP.POP.65UP.TO.ZS
pop65 = wb.download(indicator='SP.POP.65UP.TO.ZS', country=['US'], start=1990, end=2020)
print(pop65)
print()

# Population ages 15-64 (% of total population)
# SP.POP.1564.TO.ZS
pop64_gh = wb.download(indicator='SP.POP.1564.TO.ZS', country=['GH'], start=1990, end=2020)
print(pop64_gh)
print()

# Population ages 65 and above (% of total population)
# SP.POP.65UP.TO.ZS
pop65_gh = wb.download(indicator='SP.POP.65UP.TO.ZS', country=['GH'], start=1990, end=2020)
print(pop65_gh)
print()

plt.figure()
plt.title('US Population - Ages 15-64 vs. Ages 65 and above (% of total population)', fontweight='bold')
ax1 = pop64['SP.POP.1564.TO.ZS'].plot(color='blue', grid=True, label='Ages 15-64 (% of total population)')
ax2 = pop65['SP.POP.65UP.TO.ZS'].plot(color='red', grid=True, label='Ages 65 and above (% of total population)')
ax1.legend(loc=1)
ax2.legend(loc=2)
plt.xlabel('Year')
plt.ylabel('% of total population')
plt.show()

plt.figure()
plt.title('Ghana Population - Ages 15-64 vs. Ages 65 and above (% of total population)', fontweight='bold')
ax1 = pop64_gh['SP.POP.1564.TO.ZS'].plot(color='blue', grid=True, label='Ages 15-64 (% of total population)')
ax2 = pop65_gh['SP.POP.65UP.TO.ZS'].plot(color='red', grid=True, label='Ages 65 and above (% of total population)')
ax1.legend(loc=1)
ax2.legend(loc=2)
plt.xlabel('Year')
plt.ylabel('% of total population')
plt.show()
