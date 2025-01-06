# Let’s take the immersive approach and write some async IO code. 
# This short program is the Hello World of async IO but goes a long way 
# towards illustrating its core functionality:

#!/usr/bin/env python3
# countasync.py

import asyncio

async def count():
    print("One")
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
