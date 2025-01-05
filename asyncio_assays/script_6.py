# aiohttp client example

import aiohttp
import asyncio

async def session_coroutine():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://python.org') as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.text()
                print("Body:", html[:15], "...")
    except Exception as e:
        print(f' Exception exercising aiohttp client session!')
        print(f' {type(e)}')  # the exception type.
        print(f' {e.args}')   # arguments stored in .args
        print(f' {e}\n')      # __str__ allows args to be printed directly, but may be overridden in exception subclasses   

if __name__ ==  '__main__':
    asyncio.run(session_coroutine())

