import pandas as pd

dfd = pd.DataFrame({'Date': ['2011-06-09', '2011-07-09', '2011-09-10', '2011-11-02'],
                    'Group': ['tri23_1', 'hsgç_T2', 'bbbj-1Y_jn', 'hsgç_T2'],
                    'Family': ['Laavin', 'Grendy', 'Fantol', 'Gondow'],
                    'Bonus': [456, 679, 431, 569]})

print(dfd)
print()

df2 = pd.DataFrame({'Group': ['tri23_1', 'hsgç_T2', 'bbbj-1Y_jn', 'mlkl_781', 'vchs_94'],
                    'Hotel': ['Jamel', 'Frank', 'Luxy', 'Grand Hotel', 'Vancouver']})

print(df2)
print()

# If you set the index to the 'Group' column on the other df then you can replace using map on your original df 'Group' column:
dfd['Group'] = dfd['Group'].map(df2.set_index('Group')['Hotel'])
print(dfd)
print()
