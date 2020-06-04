import random
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 100)

# ============================================================
# List Comprehensions
#
# Examples of python list comprehensions follow. Check the python user
# guide for more information and background on it next:
#
# https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Comprehensions.html
# https://docs.python.org/3/tutorial/datastructures.html#nested-list-comprehensions
#
# self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
# self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

# Refer to nuertey_covid19_final.py for an excellent example.

# [f(v) for (n, f), v in zip(cls.all_slots, values)]

# ============================================================
# Different choices for indexing
# 
# Object selection has had a number of user-requested additions in order to support more explicit location based indexing. Pandas now supports three types of multi-axis indexing.
# 
#     .loc is primarily label based, but may also be used with a boolean array. .loc will raise KeyError when the items are not found. Allowed inputs are:
# 
#             A single label, e.g. 5 or 'a' (Note that 5 is interpreted as a label of the index. This use is not an integer position along the index.).
# 
#             A list or array of labels ['a', 'b', 'c'].
# 
#             A slice object with labels 'a':'f' (Note that contrary to usual python slices, both the start and the stop are included, when present in the index! See Slicing with labels and Endpoints are inclusive.)
# 
#             A boolean array (any NA values will be treated as False).
# 
#             A callable function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above).
# 
#     .iloc is primarily integer position based (from 0 to length-1 of the axis), but may also be used with a boolean array. .iloc will raise IndexError if a requested indexer is out-of-bounds, except slice indexers which allow out-of-bounds indexing. (this conforms with Python/NumPy slice semantics). Allowed inputs are:
# 
#             An integer e.g. 5.
# 
#             A list or array of integers [4, 3, 0].
# 
#             A slice object with ints 1:7.
# 
#             A boolean array (any NA values will be treated as False).
# 
#             A callable function with one argument (the calling Series or DataFrame) and that returns valid output for indexing (one of the above).
# 
#     See more at Selection by Position, Advanced Indexing and Advanced Hierarchical.
# 
#     .loc, .iloc, and also [] indexing can accept a callable as indexer. See more at Selection By Callable.
# 
# Getting values from an object with multi-axes selection uses the following notation (using .loc as an example, but the following applies to .iloc as well). Any of the axes accessors may be the null slice :. Axes left out of the specification are assumed to be :, e.g. p.loc['a'] is equivalent to p.loc['a', :, :].
#
#
# Object Type    Indexers
# 
# Series         s.loc[indexer]
# 
# DataFrame      df.loc[row_indexer,column_indexer]
#
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

# Here we construct a simple time series data set to use for illustrating the indexing functionality:

dates = pd.date_range('1/1/2000', periods=8) # 8 months range of dates.

df = pd.DataFrame(np.random.randn(8, 4),
                  index=dates, columns=['A', 'B', 'C', 'D'])

print(df)
print()

s = df['A']
print(s)
print()
print(dates[5])
print(s[dates[5]])
print()

df[['B', 'A']] = df[['A', 'B']] # Manipulating lists of columns...
print(df)
print()

# Warning
# 
# pandas aligns all AXES when setting Series and DataFrame from .loc, and .iloc.
# This will not modify df because the column alignment is before value assignment.
print(df[['A', 'B']])
print()
df.loc[:, ['B', 'A']] = df[['A', 'B']]
print(df[['A', 'B']])
print()

# The correct way to swap column values is by using raw values:
df.loc[:, ['B', 'A']] = df[['A', 'B']].to_numpy()
print(df[['A', 'B']])
print()

# You may access an index on a Series or column on a DataFrame directly as an attribute:
sa = pd.Series([1, 2, 3], index=list('abc'))
print(sa)
print()

print(sa.b)
print()

sa.a = 5
print(sa)
print()

dfa = df.copy()

print(dfa.A)
print()

dfa.A = list(range(len(dfa.index)))  # ok if A already exists
print(dfa)
print()

dfa['A'] = list(range(len(dfa.index)))  # use this form to create a new column
print(dfa)
print()

# Warning
# 
#     You can use this access only if the index element is a valid Python identifier, e.g. s.1 is not allowed. See here for an explanation of valid identifiers.
# 
#     The attribute will not be available if it conflicts with an existing method name, e.g. s.min is not allowed, but s['min'] is possible.
# 
#     Similarly, the attribute will not be available if it conflicts with any of the following list: index, major_axis, minor_axis, items.
# 
#     In any of these cases, standard indexing will still work, e.g. s['1'], s['min'], and s['index'] will access the corresponding element or column.
# 

# You can also assign a dict to a row of a DataFrame:
x = pd.DataFrame({'x': [1, 2, 3], 'y': [3, 4, 5]})
print(x)
print()
x.iloc[1] = {'x': 9, 'y': 99} # I guess curly braces denotes a dict, like json.
print(x)
print()

# ============================================================
# Slicing ranges
# 
# The most robust and consistent way of slicing ranges along arbitrary axes is described in the Selection by Position section detailing the .iloc method. For now, we explain the semantics of slicing using the [] operator.
# 
# With Series, the syntax works exactly as with an ndarray, returning a slice of the values and the corresponding labels:
print(s[:5])   # First 5 elements and their labels (indices)
print()

print(s[::2])  # Every other element(2) and their labels (indices)
print()

print(s[::-1]) # Reverse the series and its labels (indices)
print()

# Note that setting works as well:
s2 = s.copy()

s2[:5] = 0

print(s2)
print()

# With DataFrame, slicing inside of [] slices the rows. This is provided largely as a convenience since it is such a common operation.
print(df[:3])
print()

print(df[::-1])
print()

# Selection by label
# 
# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may depend on the context. This is sometimes called chained assignment and should be avoided. See Returning a View versus Copy.
#
# Warning
# 
#     .loc is strict when you present slicers that are not compatible (or convertible) with the index type. For example using integers in a DatetimeIndex. These will raise a TypeError.
#
# Nuertey Odzeyem Addendum: Very good behavior indeed above! Take advantage of .loc in your slicing operations for added type checking.
dfl = pd.DataFrame(np.random.randn(5, 4),
                columns=list('ABCD'),
                index=pd.date_range('20130101', periods=5))


print(dfl)
print()

# TypeError: cannot do slice indexing on <class 'pandas.tseries.index.DatetimeIndex'> with these indexers [2] of <type 'int'>
try:
    print(dfl.loc[2:3])
    print()
except Exception as e:
    print("Caught TypeError exception as expected...")
    print(e)
    print()

# String likes in slicing can be convertible to the type of the index and lead to natural slicing.
#
# Nuertey Odzeyem Addendum: Very good behavior indeed above! Take advantage of it in your slicing.
dfl.loc['20130102':'20130104']

# Warning
# 
# Starting in 0.21.0, pandas will show a FutureWarning if indexing with a list with missing labels. In the future this will raise a KeyError. See list-like Using loc with missing keys in a list is Deprecated.

# pandas provides a suite of methods in order to have purely label based indexing. This is a strict inclusion based protocol. Every label asked for must be in the index, or a KeyError will be raised. When slicing, both the start bound AND the stop bound are included, if present in the index. Integers are valid labels, but they refer to the label and not the position.
# 
# The .loc attribute is the primary access method. The following are valid inputs:
# 
#     A single label, e.g. 5 or 'a' (Note that 5 is interpreted as a label of the index. This use is not an integer position along the index.).
# 
#     A list or array of labels ['a', 'b', 'c'].
# 
#     A slice object with labels 'a':'f' (Note that contrary to usual python slices, both the start and the stop are included, when present in the index! See Slicing with labels.
# 
#     A boolean array.
# 
#     A callable, see Selection By Callable.
s1 = pd.Series(np.random.randn(6), index=list('abcdef'))

# Nuertey Odzeyem Addendum: note that series are presented vertically
# instead of the more logical horizontally.
print(s1)
print()

print(s1.loc['c':])
print()

print(s1.loc['b'])
print()

# Note that setting works as well:
s1.loc['c':] = 0

print(s1)
print()

# With a DataFrame:
df1 = pd.DataFrame(np.random.randn(6, 4),
                   index=list('abcdef'),
                   columns=list('ABCD'))

print(df1)
print()

print(df1.loc[['a', 'b', 'd'], :])
print()

# Accessing via label slices:
print(df1.loc['d':, 'A':'C'])
print()

# For getting a cross section using a label (equivalent to df.xs('a')):
print(df1.loc['a'])
print()

# For getting values with a boolean array:
print(df1.loc['a'] > 0)
print()

print(df1.loc[:, df1.loc['a'] > 0])
print()

# NA values in a boolean array propagate as False:
# 
# Changed in version 1.0.2: mask = pd.array([True, False, True, False, pd.NA, False], dtype=”boolean”) mask df1[mask]

# For getting a value explicitly:
# this is also equivalent to ``df1.at['a','A']``
print(df1.loc['a', 'A'])
print()

# Slicing with labels
# 
# When using .loc with slices, if both the start and the stop labels are present in the index, then elements located between the two (including them) are returned:
s = pd.Series(list('abcde'), index=[0, 3, 2, 5, 4])

print(s)
print()

# The '3' and '5' here are labels, not numerical indices.
print(s.loc[3:5])
print()

# If at least one of the two is absent, but the index is sorted, and can be compared against start and stop labels, then slicing will still work as expected, by selecting labels which rank between the two:
print(s.sort_index())
print()

print(s.sort_index().loc[1:6])
print()

# However, if at least one of the two is absent and the index is not sorted, an error will be raised (since doing otherwise would be computationally expensive, as well as potentially ambiguous for mixed type indexes). For instance, in the above example, s.loc[1:6] would raise KeyError.
try:
    print(s.loc[1:6])
    print()
except Exception as e:
    print("Caught KeyError exception as expected...")
    print(e)
    print()

# Nuertey Odzeyem Addendum: I dont understand the below so well as my intuition does not coincide with the results of the test case scenarios. Therefore prefer selection by labels instead.
# 
# Selection by position
#
# Warning
# 
# Whether a copy or a reference is returned for a setting operation, may depend on the context. This is sometimes called chained assignment and should be avoided. See Returning a View versus Copy below.
# 
# Pandas provides a suite of methods in order to get purely integer based indexing. The semantics follow closely Python and NumPy slicing. These are 0-based indexing. When slicing, the start bound is included, while the upper bound is excluded. Trying to use a non-integer, even a valid label will raise an IndexError.
# 
# The .iloc attribute is the primary access method. The following are valid inputs:
# 
#     An integer e.g. 5.
# 
#     A list or array of integers [4, 3, 0].
# 
#     A slice object with ints 1:7.
# 
#     A boolean array.
# 
#     A callable, see Selection By Callable.
s1 = pd.Series(np.random.randn(5), index=list(range(0, 10, 2)))

print(s1)
print()

print(s1.iloc[:3])
print()

print(s1.iloc[3])
print()

# Note that setting works as well:
s1.iloc[:3] = 0

print(s1)
print()

# With a DataFrame:
df1 = pd.DataFrame(np.random.randn(6, 4), index=list(range(0, 12, 2)), columns=list(range(0, 8, 2)))

print(df1)
print()

print(df1.iloc[:3])
print()

print(df1.iloc[1:5, 2:4])
print()

# Select via integer list:
print(df1.iloc[[1, 3, 5], [1, 3]])
print()

print(df1.iloc[1:3, :])
print()

print(df1.iloc[:, 1:3])
print()

# this is also equivalent to ``df1.iat[1,1]``
print(df1.iloc[1, 1])
print()

# For getting a cross section using an integer position (equiv to df.xs(1)):
print(df1.iloc[1])
print()

# Out of range slice indexes are handled gracefully just as in Python/Numpy.

# these are allowed in python/numpy.
x = list('abcdef')

print(x)
print()

print(x[4:10])
print()

print(x[8:10])
print()

s = pd.Series(x)

print(s)
print()

print(s.iloc[4:10])
print()

print(s.iloc[8:10])
print()

# Note that using slices that go out of bounds can result in an empty axis (e.g. an empty DataFrame being returned).
dfl = pd.DataFrame(np.random.randn(5, 2), columns=list('AB'))

print(dfl)
print()

print(dfl.iloc[:, 2:3])
print()

print(dfl.iloc[:, 1:3])
print()

print(dfl.iloc[4:6])
print()

# A single indexer that is out of bounds will raise an IndexError. A list of indexers where any element is out of bounds will raise an IndexError:
try:
    print(dfl.iloc[[4, 5, 6]])
    print()
except Exception as e:
    print("Caught IndexError exception as expected...")
    print(e)
    print()

try:
    print(dfl.iloc[:, 4])
    print()
except Exception as e:
    print("Caught IndexError exception as expected...")
    print(e)
    print()

# Selection by callable
# 
# .loc, .iloc, and also [] indexing can accept a callable as indexer. The callable must be a function with one argument (the calling Series or DataFrame) that returns valid output for indexing.
df1 = pd.DataFrame(np.random.randn(6, 4), index=list('abcdef'), columns=list('ABCD'))

print(df1)
print()

print(df1.loc[lambda df: df['A'] > 0, :])
print()

print(df1.loc[:, lambda df: ['A', 'B']])
print()

print(df1.iloc[:, lambda df: [0, 1]])
print()

print(df1[lambda df: df.columns[0]])
print()

# You can use callable indexing in Series.
print(df1['A'].loc[lambda s: s > 0])
print()

# Using these methods / indexers, you can chain data selection operations without using a temporary variable.
bb = pd.read_csv('data/baseball.csv', index_col='id')

print(bb)
print()

cincinnati = bb.loc[bb['team'] == 'CIN', ['team', 'r']]
print(cincinnati)
print()

print(cincinnati['r'].sum())
print()

# Create a new index by amalgamating two columns, sum the values over each unique year 
# and each unique team and then locate which of the sum of r's exceeds 100:
print(bb.groupby(['year', 'team']).sum())
print()

print(bb.groupby(['year', 'team']).sum().loc[lambda df: df['r'] > 100])
print()

# IX indexer is deprecated
# 
# Warning
# 
# Starting in 0.20.0, the .ix indexer is deprecated, in favor of the more strict .iloc and .loc indexers.
# 
# .ix offers a lot of magic on the inference of what the user wants to do. To wit, .ix can decide to index positionally OR via labels depending on the data type of the index. This has caused quite a bit of user confusion over the years.
# 
# The recommended methods of indexing are:
# 
#     .loc if you want to label index.
# 
#     .iloc if you want to positionally index.
dfd = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=list('abc'))

print(dfd)
print()

# Previous behavior, where you wish to get the 0th and the 2nd elements from the index in the ‘A’ column.
print(dfd.ix[[0, 2], 'A'])
print()

# Using .loc. Here we will select the appropriate indexes from the index, then use label indexing.
print(dfd.loc[dfd.index[[0, 2]], 'A'])
print()

# This can also be expressed using .iloc, by explicitly getting locations on the indexers, and using positional indexing to select things.
print(dfd.iloc[[0, 2], dfd.columns.get_loc('A')])
print()

# For getting multiple indexers, using .get_indexer:
print(dfd.iloc[[0, 2], dfd.columns.get_indexer(['A', 'B'])])
print()

# Indexing with list with missing labels is deprecated
# 
# Warning
# 
# Starting in 0.21.0, using .loc or [] with a list with one or more missing labels, is deprecated, in favor of .reindex.
# 
# In prior versions, using .loc[list-of-labels] would work as long as at least 1 of the keys was found (otherwise it would raise a KeyError). This behavior is deprecated and will show a warning message pointing to this section. The recommended alternative is to use .reindex().
# 
# For example.
s = pd.Series([1, 2, 3])

print(s)
print()

# Selection with all keys found is unchanged.
print(s.loc[[1, 2]])
print()

print(s.loc[[1, 2, 3]])
print()

# Unlike the current behavior, passing list-likes to .loc with any non-matching elements will raise
# KeyError in the future, you can use .reindex() as an alternative.
# 
# See the documentation here:
# https://pandas.pydata.org/pandas-docs/stable/indexing.html#deprecate-loc-reindex-listlike

# Reindexing
# 
# The idiomatic way to achieve selecting potentially not-found elements is via .reindex(). See also the section on reindexing.

print(s.reindex([1, 2, 3]))
print()

# Alternatively, if you want to select only valid keys, the following is idiomatic and efficient; it is guaranteed to preserve the dtype of the selection.
labels = [1, 2, 3]

print(s.loc[s.index.intersection(labels)])
print()

# Having a duplicated index will raise for a .reindex():
s = pd.Series(np.arange(4), index=['a', 'a', 'b', 'c'])

labels = ['c', 'd']

try:
    print(s.reindex(labels))
    print()
except Exception as e:
    print("Caught ValueError exception as expected...")
    print(e)
    print()

# Generally, you can intersect the desired labels with the current axis, and then reindex.
print(s.loc[s.index.intersection(labels)].reindex(labels))
print()

# However, this would still raise if your resulting index is duplicated.
labels = ['a', 'd']

try:
    print(s.loc[s.index.intersection(labels)].reindex(labels))
    print()
except Exception as e:
    print("Caught ValueError exception as expected...")
    print(e)
    print()

# Selecting random samples
# 
# A random selection of rows or columns from a Series or DataFrame with the sample() method. The method will sample rows by default, and accepts a specific number of rows/columns to return, or a fraction of rows.
s = pd.Series([0, 1, 2, 3, 4, 5])
print(s)
print()

# When no arguments are passed, returns 1 row.
print(s.sample())
print()

# One may specify either a number of rows:
print(s.sample(n=3))
print()

# Or a fraction of the rows:
print(s.sample(frac=0.5)) # s.size()*0.5 = 3
print()

# By default, sample will return each row at most once, but one can also sample with replacement using the replace option:
s = pd.Series([0, 1, 2, 3, 4, 5])

# Without replacement (default):
print(s.sample(n=6, replace=False))
print()

# With replacement:
print(s.sample(n=6, replace=True))
print()

# By default, each row has an equal probability of being selected, but if you want rows to have different probabilities, you can pass the sample function sampling weights as weights. These weights can be a list, a NumPy array, or a Series, but they must be of the same length as the object you are sampling. Missing values will be treated as a weight of zero, and inf values are not allowed. If weights do not sum to 1, they will be re-normalized by dividing all weights by the sum of the weights. For example:
s = pd.Series([0, 1, 2, 3, 4, 5])

example_weights = [0, 0, 0.2, 0.2, 0.2, 0.4]

print(s.sample(n=3, weights=example_weights))
print()

# Weights will be re-normalized automatically
example_weights2 = [0.5, 0, 0, 0, 0, 0]

print(s.sample(n=1, weights=example_weights2))
print()

# When applied to a DataFrame, you can use a column of the DataFrame as sampling weights (provided you are sampling rows and not columns) by simply passing the name of the column as a string.
df2 = pd.DataFrame({'col1': [9, 8, 7, 6], 'weight_column': [0.5, 0.4, 0.1, 0]})
print(df2)
print()

print(df2.sample(n=3, weights='weight_column'))
print()

# sample also allows users to sample columns instead of rows using the axis argument.
df3 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [2, 3, 4]})
print(df3)
print()

print(df3.sample(n=1, axis=1)) # axis = 0 is the index.
print()

# Finally, one can also set a seed for sample’s random number generator using the random_state argument, which will accept either an integer (as a seed) or a NumPy RandomState object.
df4 = pd.DataFrame({'col1': [1, 2, 3], 'col2': [2, 3, 4]})

# With a given seed, the sample will always draw the same rows.
print(df4.sample(n=2, random_state=2))
print()

print(df4.sample(n=2, random_state=2))
print()

# Setting with enlargement
# 
# The .loc/[] operations can perform enlargement when setting a non-existent key for that axis.
# 
# In the Series case this is effectively an appending operation.
se = pd.Series([1, 2, 3])
print(se)
print()

se[5] = 5.

print(se)
print()

# A DataFrame can be enlarged on either axis via .loc.
dfi = pd.DataFrame(np.arange(6).reshape(3, 2), columns=['A', 'B'])
print(dfi)
print()

dfi.loc[:, 'C'] = dfi.loc[:, 'A']

print(dfi)
print()

# This is like an append operation on the DataFrame.
dfi.loc[3] = 5

print(dfi)
print()

# ======================================================
# Pandas concat vs append vs join vs merge (**** 'Tis more performant still to append on the lists and then create the Pandas dataframe with the complete list. See nuertey_covid19_final.py)
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

# When setting values in a pandas object, care must be taken to avoid what is called chained indexing. Here is an example.
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

# ==============================================
# This is the correct access method:

dfc = pd.DataFrame({'A': ['aaa', 'bbb', 'ccc'], 'B': [1, 2, 3]})

# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
dfc.loc[0, 'A'] = 11 # Do not do "dfc['A'][0] = 111"!!!

print(dfc)
