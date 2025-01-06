# Let’s take the immersive approach and write some async IO code. 
# This short program is the Hello World of async IO but goes a long way 
# towards illustrating its core functionality:

#!/usr/bin/env python3
# countasync.py

import asyncio

# The syntax 'async def' introduces either a native coroutine or an 
# asynchronous generator. The expressions 'async with' and 'async for' are also valid.
async def count():
    print("One")
    
    # The keyword await passes function control back to the event loop. 
    # (It suspends the execution of the surrounding coroutine.) If Python 
    # encounters an await f() expression in the scope of g(), this is how
    # await tells the event loop, “Suspend execution of g() until whatever 
    # I’m waiting on—the result of f()—is returned. In the meantime, go 
    # let something else run.”
    await asyncio.sleep(1)
    
    print("Two")

async def main():
    # Presumably, the below is the better way to invoke asyncio.gather().
    # The thing to note is that a task does not have to be created and launched
    # (create_task()) before composing asyncio.gather(). The coroutines can
    # be 'asyncio gathered' directly.
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
