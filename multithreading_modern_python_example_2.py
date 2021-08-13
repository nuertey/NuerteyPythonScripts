# https://stackoverflow.com/questions/54942503/cant-read-write-to-files-using-multithreading-in-python/54943940?noredirect=1#comment96651673_54943940

# QUESTION:

# Can't read/write to files using multithreading in python

# I have an input file which will contain a long list of URLs. Lets assume this in mylines.txt:
# 
# https://yahoo.com
# https://google.com
# https://facebook.com
# https://twitter.com
# 
# What I need to do is:
# 
#     [1] Read a line from the input file mylines.txt
# 
#     [2] Execute myFun function. Which will perform some tasks. And produce an output that consists of a line. It is more complex in my real code. But something like this in concept.
# 
#     [3] Write the output to the results.txt file
# 
# Since I have large input. I need to leverage python multithreading. I looked at this good post here. But unfortunately, it assumes input in a simple list, and does not assume I want to write the output of the function in a file.
# 
# I need to ensure that each input's output is written in a single line (i.e. the danger if multithreads are writing to the same line so I get incorrect data).
# 
# I tried to mess around. But no success. I did not use python's multithreading before but it is time to learn as it is inevitable in my case. I have a very long list which can not finish in a reasonable time without multithreading.
# 

# ======================================================================
# ANSWER:

# Rather than have the worker pool threads print the result out, which is not guaranteed to buffer the output correctly, instead create one more thread, which reads results from a second Queue and prints them.

# I've modified your solution so it builds its own threadpool of workers. There's little point giving the queue an inifinite length, since the main thread will block when the queue reaches maximum size: you only need it to be long enough to make sure there's always work to be processed by the worker threads - the main thread will block and unblock as the queue size increases and decreases.

# It also identifies the thread responsible for each item on the output queue, which should give you some confidence that the multithreading approach is working, and prints the response code from the server. I found I had to strip the newlines from the URLs.

# Since now only one thread is writing to the file, writes are always perfectly in sync and there is no chance of them interfering with each other.

import threading
import requests
import queue
POOL_SIZE = 4

def myFunc(inq, outq):  # worker thread deals only with queues
    while True:
        url = inq.get()  # Blocks until something available
        if url is None:
            break
        response = requests.get(url.strip(), timeout=(2, 5))
        outq.put((url, response, threading.currentThread().name))


class Writer(threading.Thread):
    def __init__(self, q):
        super().__init__()
        self.results = open("myresults","a") # "a" to append results
        self.queue = q
    def run(self):
        while True:
            url, response, threadname = self.queue.get()
            if response is None:
                self.results.close()
                break
            print("****url is:",url, ", response is:", response.status_code, response.url, "thread", threadname, file=self.results)

#load up a queue with your data, this will handle locking
inq = queue.Queue()  # could usefully limit queue size here
outq = queue.Queue()

# start the Writer
writer = Writer(outq)
writer.start()

# make the Pool of workers
threads = []
for i in range(POOL_SIZE):
    thread = threading.Thread(target=myFunc, name=f"worker{i}", args=(inq, outq))
    thread.start()
    threads.append(thread)

# push the work onto the queues
with open("mylines.txt","r") as worker_data: # open my input file.
    for url in worker_data:
        inq.put(url.strip())
for thread in threads:
    inq.put(None)

# close the pool and wait for the workers to finish
for thread in threads:
    thread.join()

# Terminate the writer
outq.put((None, None, None))
writer.join()

# ----------------------------------------------------------------------
# Using the data given in mylines.txt I see the following output:
# 
# ****url is: https://www.google.com , response is: 200 https://www.google.com/ thread worker1
# ****url is: https://twitter.com , response is: 200 https://twitter.com/ thread worker2
# ****url is: https://facebook.com , response is: 200 https://www.facebook.com/ thread worker0
# ****url is: https://www.censys.io , response is: 200 https://censys.io/ thread worker1
# ****url is: https://yahoo.com , response is: 200 https://uk.yahoo.com/?p=us thread worker3
