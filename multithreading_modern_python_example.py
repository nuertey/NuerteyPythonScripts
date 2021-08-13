# https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python

# Since this question was asked in 2010, there has been real simplification in how to do simple multithreading with Python with map and pool.

# The code below comes from an article/blog post that you should definitely check out (no affiliation) - Parallelism in one line: A Better Model for Day to Day Threading Tasks. I'll summarize below - it ends up being just a few lines of code:
#
# https://docs.python.org/2/library/functions.html#map
# https://docs.python.org/2/library/multiprocessing.html
#
# https://chriskiehl.com/article/parallelism-in-one-line

from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(4)
results = pool.map(my_function, my_array)

# Which is the multithreaded version of:

results = []
for item in my_array:
    results.append(my_function(item))

# Description
# 
#     Map is a cool little function, and the key to easily injecting parallelism into your Python code. For those unfamiliar, map is something lifted from functional languages like Lisp. It is a function which maps another function over a sequence.
# 
#     Map handles the iteration over the sequence for us, applies the function, and stores all of the results in a handy list at the end.
# 

# Implementation
# 
#     Parallel versions of the map function are provided by two libraries:multiprocessing, and also its little known, but equally fantastic step child:multiprocessing.dummy.
# 
# multiprocessing.dummy is exactly the same as multiprocessing module, but uses threads instead (an important distinction - use multiple processes for CPU-intensive tasks; threads for (and during) I/O):
# 
#     multiprocessing.dummy replicates the API of multiprocessing, but is no more than a wrapper around the threading module.
# 

import urllib.request as urllib2
from multiprocessing.dummy import Pool as ThreadPool

urls = [
  'http://www.python.org',
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.python.org/getit/',
  'http://www.python.org/community/',
  'https://wiki.python.org/moin/',
]

# Make the Pool of workers
pool = ThreadPool(4)

# Open the URLs in their own threads
# and return the results
results = pool.map(urllib2.urlopen, urls)

# Close the pool and wait for the work to finish
pool.close()
pool.join()

# And the timing results:
# 
# Single thread:   14.4 seconds
#        4 Pool:   3.1 seconds
#        8 Pool:   1.4 seconds
#       13 Pool:   1.3 seconds

# Passing multiple arguments (works like this only in Python 3.3 and later):
#   
# https://stackoverflow.com/a/28975239/2327328

# To pass multiple arrays:

results = pool.starmap(function, zip(list_a, list_b))

# Or to pass a constant and an array:

results = pool.starmap(function, zip(itertools.repeat(constant), list_a))
