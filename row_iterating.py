def compose_status_by_country_name(country_name_input):
    country_status = cov_19.get_status_by_country_name(str(country_name_input))
    #print(country_status)
    #print()
    combined_output.loc[row].country_id = country_status['id']
    combined_output.loc[row].country = country_status['country']
    combined_output.loc[row].confirmed = country_status['confirmed']
    combined_output.loc[row].active = country_status['active']
    combined_output.loc[row].deaths = country_status['deaths']
    combined_output.loc[row].recovered = country_status['recovered']
    combined_output.loc[row].latitude = country_status['latitude']
    combined_output.loc[row].longitude = country_status['longitude']
    combined_output.loc[row].last_update = country_status['last_update']
    return combined_output

# iterating over one column - `f` is some function that processes your data
result = [compose_status_by_country_name(x) for x in data['name']]

# iterating over two columns, use `zip`
result = [f(x, y) for x, y in zip(df['col1'], df['col2'])]

# iterating over multiple columns
result = [f(row[0], ..., row[n]) for row in df[['col1', ...,'coln']].values]

ser = pd.Series([['a', 'b', 'c'], ['d', 'e'], ['f', 'g']] * 10000) ; %timeit pd.Series(y for x in ser for y in x) ; %timeit pd.Series([y for x in ser for y in x])

>>> squares = []
>>> for x in range(10):
...     squares.append(x**2)
...
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Note that this creates (or overwrites) a variable named x that still exists after the loop completes. We can calculate the list of squares without any side effects using:

squares = list(map(lambda x: x**2, range(10)))

#or, equivalently:

squares = [x**2 for x in range(10)]

