import pandas as pd

# Pandas concat vs append vs join vs merge
# 
#     Concat gives the flexibility to join based on the axis( all rows or all columns)
# 
#     Append is the specific case(axis=0, join='outer') of concat
# 
#     Join is based on the indexes (set by set_index) on how variable =['left','right','inner','couter']
# 
#     Merge is based on any particular column each of the two dataframes, this columns are variables on like 'left_on', 'right_on', 'on'

# ========================================================
# Returning a view versus a copy

# When setting values in a pandas object, care must be taken to avoid what is called chained indexing. # Here is an example.
dfmi = pd.DataFrame([list('abcd'),
                     list('efgh'),
                     list('ijkl'),
                     list('mnop')],
                    columns=pd.MultiIndex.from_product([['one', 'two'],
                                                        ['first', 'second']]))
print(dfmi)
print()

# But it turns out that assigning to the product of chained indexing has 
# inherently unpredictable results. To see this, think about how the Python
# interpreter executes this code:

# Compare these two access methods:

# Preferred (and much faster!):
# Contrast the previous method to df.loc[:,('one','second')] which passes 
# a nested tuple of (slice(None),('one','second')) to a single call to
# __getitem__. This allows pandas to deal with this as a single entity. 
# Furthermore this order of operations can be significantly faster, and
# allows one to index both axes if so desired.
print(dfmi.loc[:, ('one', 'second')])
# becomes
# dfmi.loc.__setitem__((slice(None), ('one', 'second')), value)
print()

# dfmi['one'] selects the first level of the columns and returns a DataFrame 
# that is singly-indexed. Then another Python operation dfmi_with_one['second'] 
# selects the series indexed by 'second'. This is indicated by the variable 
# dfmi_with_one because pandas sees these operations as separate events. 
# e.g. separate calls to __getitem__, so it has to treat them as linear 
# operations, they happen one after another.
print(dfmi['one']['second'])
# becomes
# dfmi.__getitem__('one').__setitem__('second', value)
print()

# See that __getitem__ in there? Outside of simple cases, it’s very hard 
# to predict whether it will return a view or a copy (it depends on the 
# memory layout of the array, about which pandas makes no guarantees), and
# therefore whether the __setitem__ will modify dfmi or a temporary object
# that gets thrown out immediately afterward. That’s what SettingWithCopy 
# is warning you about!

# ========================================================
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']},
                   index=[0, 1, 2, 3])


df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                    'B': ['B4', 'B5', 'B6', 'B7'],
                    'C': ['C4', 'C5', 'C6', 'C7'],
                    'D': ['D4', 'D5', 'D6', 'D7']},
                   index=[4, 5, 6, 7])


df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                    'B': ['B8', 'B9', 'B10', 'B11'],
                    'C': ['C8', 'C9', 'C10', 'C11'],
                    'D': ['D8', 'D9', 'D10', 'D11']},
                   index=[8, 9, 10, 11])


frames = [df1, df2, df3]

# Note:
# It is worth noting that concat() (and therefore append()) makes a full
# copy of the data, and that constantly reusing this function can create
# a significant performance hit. If you need to use the operation over 
# several datasets, use a list comprehension.
result = pd.concat(frames)
print(frames)
print()

result = pd.concat(frames, keys=['x', 'y', 'z'])
print(frames)
print()

print(result.loc['y'])
print()

# It’s not a stretch to see how this can be very useful. More detail on 
# this functionality below:
# 
# frames = [ process_your_file(f) for f in files ]
# result = pd.concat(frames)

# More here:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
