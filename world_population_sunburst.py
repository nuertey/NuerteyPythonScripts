#***********************************************************************
# @file
#
# Python script for generating world population sunburst plot.
#
# @note 
#
# @warning  None
#
#  Created: April 12, 2020
#   Author: Nuertey Odzeyem
#**********************************************************************/
import pandas as pd
import plotly
import plotly.offline as offline
import world_bank_data as wb

def version_to_int_list(version):
    return [int(s) for s in version.split('.')]

assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'

pd.set_option('display.max_rows', 100)

# Countries and associated regions
countries = wb.get_countries()
#print(countries)
#print()

# Population dataset, by the World Bank (most recent value)
# The data set is indexed with the country code
population = wb.get_series('SP.POP.TOTL', id_or_value='id', simplify_index=True, mrv=1)
print(population)
print()

# Aggregate region, country and population
df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
df['population'] = population
#print(df)
#print()

# +
# The sunburst plot requires weights (values), labels, and parent (region, or World)
# We build the corresponding table here
columns = ['parents', 'labels', 'values']

level1 = df.copy()
level1.columns = columns
level1['text'] = level1['values'].apply(lambda pop: '{:,.0f}'.format(pop))

level2 = df.groupby('region').population.sum().reset_index()[['region', 'region', 'population']]
level2.columns = columns
level2['parents'] = 'World'
# move value to text for this level
level2['text'] = level2['values'].apply(lambda pop: '{:,.0f}'.format(pop))
level2['values'] = 0

level3 = pd.DataFrame({'parents': [''], 'labels': ['World'],
                       'values': [0.0], 'text': ['{:,.0f}'.format(population.loc['WLD'])]})

all_levels = pd.concat([level1, level2, level3], axis=0, sort=True).reset_index(drop=True)
#print(all_levels)
#print()
# -

# And now we can plot the World Population
offline.plot(dict(
    data=[dict(type='sunburst', hoverinfo='text', **all_levels)],
    layout=dict(title='World Population (World Bank, 2018)<br>Click on a region to zoom',
                width=800, height=800)),
    validate=False)
