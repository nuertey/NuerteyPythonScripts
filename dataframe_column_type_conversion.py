dataTypeSeries = combined_output.dtypes 
print('Data type of each column of combined_output Dataframe :')
print(dataTypeSeries)

# https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas

# you could do something like the following to downcast integer columns
# to the smallest (integer) dtype that will hold the values:
df.apply(pd.to_numeric, downcast="integer", errors="ignore") 

# As long as your values can all be converted, here is all you need:
# convert column "a" of a DataFrame
df["a"] = pd.to_numeric(df["a"])

# convert all columns of DataFrame
df = df.apply(pd.to_numeric) # convert all columns of DataFrame

# convert just columns "a" and "b"
df[["a", "b"]] = df[["a", "b"]].apply(pd.to_numeric)

df["y"] = pd.to_numeric(df["y"])
df["z"] = pd.to_datetime(df["z"])  

# ==================================
#The only way I can set them is by looping through each column variable and recasting with astype.

dtypes = {'x':'object','y':'int'}
mydata = pd.DataFrame([['a','1'],['b','2']],
                      columns=['x','y'])
for c in mydata.columns:
    mydata[c] = mydata[c].astype(dtypes[c])
print mydata['y'].dtype   #=> int64
