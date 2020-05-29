setup = ''' 
import pandas as pd
import numpy as np
df_small = pd.DataFrame(np.random.randn(10, 1), columns=[str(1)])
df_medium = pd.DataFrame(np.random.randn(100, 10), columns=[str(i) for i in range(0, 10)])
df_large = pd.DataFrame(np.random.randn(1000, 100), columns=[str(i) for i in range(0, 100)])
'''

if __name__ == '__main__':
	import timeit

	print('ignore_index = False')
	print('small, append', timeit.timeit('df = df_small.append(df_small)', setup=setup, number=1000)) 
	print('medium, append', timeit.timeit('df = df_medium.append(df_medium)', setup=setup, number=1000))
	print('large, append', timeit.timeit('df = df_large.append(df_large)', setup=setup, number=1000))
	print('small, concat ignore_index=True', timeit.timeit('df = pd.concat([df_small, df_small])', setup=setup, number=1000))
	print('medium, concat ignore_index=True', timeit.timeit('df = pd.concat([df_medium, df_medium])', setup=setup, number=1000))
	print('large, concat ignore_index=True', timeit.timeit('df = pd.concat([df_large, df_large])', setup=setup, number=1000))
	
	print('ignore_index = True')
	print('small, append', timeit.timeit('df = df_small.append(df_small, ignore_index = True)', setup=setup, number=1000)) 
	print('medium, append', timeit.timeit('df = df_medium.append(df_medium, ignore_index = True)', setup=setup, number=1000))
	print('large, append', timeit.timeit('df = df_large.append(df_large, ignore_index = True)', setup=setup, number=1000))
	print('small, concat ignore_index=True', timeit.timeit('df = pd.concat([df_small, df_small], ignore_index = True)', setup=setup, number=1000))
	print('medium, concat ignore_index=True', timeit.timeit('df = pd.concat([df_medium, df_medium], ignore_index = True)', setup=setup, number=1000))
	print('large, concat ignore_index=True', timeit.timeit('df = pd.concat([df_large, df_large], ignore_index = True)', setup=setup, number=1000))