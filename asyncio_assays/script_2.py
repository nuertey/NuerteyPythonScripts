# If you need to get the return value of these async functions, then gather is useful. The following example is inspired from the documentation.
#
# https://docs.python.org/3/library/asyncio-task.html#asyncio.gather

import asyncio

async def factorial(n):
    f = 1
    for i in range(2, n + 1):
        print(f"Computing factorial({n}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    return f

async def main():
    # Schedule three calls concurrently:
    L = await asyncio.gather(factorial(2), 
                             factorial(3), 
                             factorial(4)
                            )
    print(L)  # [2, 6, 24]

asyncio.run(main())
