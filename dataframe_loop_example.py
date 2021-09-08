# ======================================================================
# https://stackoverflow.com/questions/7837722/what-is-the-most-efficient-way-to-loop-through-dataframes-with-pandas
#
# EDIT 2020/11/10
#
# For what it is worth, here is an updated benchmark with some other alternatives
# (perf with MacBookPro 2,4 GHz Intel Core i9 8 cores 32 Go 2667 MHz DDR4)
# ======================================================================
#!/usr/bin/env python
import sys
import tqdm # tqdm is a Python library that allows you to output a smart
            # progress bar by wrapping around any iterable. A tqdm progress
            # bar not only shows you how much time has elapsed, but also
            # shows the estimated time remaining for the iterable.
import time
import pandas as pd

B = []
t = pd.DataFrame({'a': range(0, 10000), 'b': range(10000, 20000)})
for _ in tqdm.tqdm(range(10)): # Wrapping the iterable, i.e. 'run the test 10 times'.
    C = []
    A = time.time()
    for i,r in t.iterrows():
        C.append((r['a'], r['b']))
    B.append({"method": "iterrows", "time": time.time()-A})

    C = []
    A = time.time()
    for ir in t.itertuples():
        C.append((ir[1], ir[2]))
    B.append({"method": "itertuples", "time": time.time()-A})

    C = []
    A = time.time()
    # Nuertey Odzeyem addendum: the following zip() approach also works
    # for getting at the index of the DataFrame, r being the row(s):
    for r in zip(t.index, t['a'], t['b']):
        C.append((r[1], r[2]))
        #print("t.index")
        #print(r[0])
    B.append({"method": "zip", "time": time.time()-A})

    C = []
    A = time.time()
    for r in zip(*t.to_dict("list").values()):
        C.append((r[0], r[1]))
    B.append({"method": "zip + to_dict('list')", "time": time.time()-A})

    C = []
    A = time.time()
    for r in t.to_dict("records"):
        C.append((r["a"], r["b"]))
    B.append({"method": "to_dict('records')", "time": time.time()-A})

    A = time.time()
    t.agg(tuple, axis=1).tolist()
    B.append({"method": "agg", "time": time.time()-A})

    A = time.time()
    t.apply(tuple, axis=1).tolist()
    B.append({"method": "apply", "time": time.time()-A})

print()
print(f'Python {sys.version} on {sys.platform}')
print(f"Pandas version {pd.__version__}")

# Create a DataFrame from the list of dictionary values, and then groupby
# the culprit column "method". 
print(
    pd.DataFrame(B).groupby("method").agg(["mean", "std"]).xs("time", axis=1).sort_values("mean")
)
