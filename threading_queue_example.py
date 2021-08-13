# Here's a simple example: you need to try a few alternative URLs and 
# return the contents of the first one to respond.
# 
# This is a case where threading is used as a simple optimization: each 
# subthread is waiting for a URL to resolve and respond, to put its contents
# on the queue; each thread is a daemon (won't keep the process up if the 
# main thread ends -- that's more common than not); the main thread starts 
# all subthreads, does a get on the queue to wait until one of them has 
# done a put, then emits the results and terminates (which takes down 
# any subthreads that might still be running, since they're daemon threads).
#
# Proper use of threads in Python is invariably connected to I/O operations
# (since CPython doesn't use multiple cores to run CPU-bound tasks anyway,
# the only reason for threading is not blocking the process while there's
# a wait for some I/O). Queues are almost invariably the best way to farm
# out work to threads and/or collect the work's results, by the way, and
# they're intrinsically threadsafe, so they save you from worrying about
# locks, conditions, events, semaphores, and other inter-thread 
# coordination/communication concepts.

import queue
import threading
import urllib.request as urllib2

# Called by each thread
def get_url(q, url):
    q.put(urllib2.urlopen(url).read())

theurls = ["http://google.com", "http://yahoo.com"]

q = queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get() # Blocks on the first item to be available. i.e. ConcurrentQueue
print(s)

# ----------------------------------------------------------------------
# NOTE: For actual parallelization in Python, you should use the multiprocessing module to fork multiple processes that execute in parallel (due to the global interpreter lock, Python threads provide interleaving, but they are in fact executed serially, not in parallel, and are only useful when interleaving I/O operations).
#
# However, if you are merely looking for interleaving (or are doing I/O operations that can be parallelized despite the global interpreter lock), then the threading module is the place to start. As a really simple example, let's consider the problem of summing a large range by summing subranges in parallel:
import threading

class SummingThread(threading.Thread):
     def __init__(self,low,high):
         super(SummingThread, self).__init__()
         self.low=low
         self.high=high
         self.total=0

     def run(self):
         for i in range(self.low,self.high):
             self.total+=i


thread1 = SummingThread(0,500000)
thread2 = SummingThread(500000,1000000)
thread1.start() # This actually causes the thread to run
thread2.start()
thread1.join()  # This waits until the thread has completed
thread2.join()
# At this point, both threads have completed
result = thread1.total + thread2.total
print result

# Note that the above is a very stupid example, as it does absolutely no I/O and will be executed serially albeit interleaved (with the added overhead of context switching) in CPython due to the global interpreter lock.
