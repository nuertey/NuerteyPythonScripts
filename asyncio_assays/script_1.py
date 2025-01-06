import time
import asyncio

async def sleep():
    print(f'Time: {time.time() - start:.2f}')
    await asyncio.sleep(2)

async def io_related_coroutine(name):
    print(f'{name} started')
    await sleep()
    print(f'{name} finished')
    
    return name

async def test_1():
    # When a coroutine is wrapped into a Task with functions like asyncio.create_task() 
    # the coroutine is automatically scheduled to run soon
    task1 = asyncio.create_task(io_related_coroutine("first"))
    task2 = asyncio.create_task(io_related_coroutine("second"))
    task3 = asyncio.create_task(io_related_coroutine("third"))
    task4 = asyncio.create_task(io_related_coroutine("fourth"))
    task5 = asyncio.create_task(io_related_coroutine("fifth"))
    task6 = asyncio.create_task(io_related_coroutine("sixth"))
    
    #await task1
    #await task2
    #await task3
    #await task4
    #await task5
    #await task6
    
    # Do other things while tasks run in the background
    # ...
    
    # Purpose: Runs multiple coroutines or tasks concurrently and waits for all of them to complete.
    results = await asyncio.gather(task1, 
                                   task2,
                                   task3,
                                   task4,
                                   task5,
                                   task6
                                  )
    
    # Returns: A list of results, one for each awaitable passed to gather. 
    # The order of results corresponds to the order of the awaitables. 
    print(results)

if __name__ ==  '__main__':
    start = time.time()
    
    asyncio.run(test_1())
    
    end = time.time()
    print(f'Time: {end-start:.2f} sec')
