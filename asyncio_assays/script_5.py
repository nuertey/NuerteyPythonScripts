# asyncio-mqtt combines the stability of the time-proven paho-mqtt 
# library with a modern, asyncio-based interface.
# 
#     No more callbacks! 👍
#     No more return codes (welcome to the MqttError)
#     Graceful disconnection (forget about on_unsubscribe, on_disconnect, etc.)
#     Compatible with async code
#     Fully type-hinted
#     Did we mention no more callbacks?
import time
import random
import threading
import asyncio
from aiomqtt import Client

# Python coroutines employ a strategy termed cooperative multitasking.
#
# async: declare a coroutine
#
# await: execute the coroutine

async def sleep():
    print(f'Time: {time.time() - start:.2f}')
    await asyncio.sleep(1)

# Coroutines (specialized generator functions) are the heart of async IO in Python.
async def subscriber_coroutine():
    async with Client("test.mosquitto.org") as client:
        topic = "humidity/#"
        
        print(f"Subscribing to topic: {topic} ...")
        await client.subscribe(topic)
        
        # It is less common (and only recently legal in Python) to use yield in an 'async def'
        # block. This creates an asynchronous generator, which you iterate over with 'async for'. 
        async for message in client.messages:
            try:
                print(f"Received message needing decoding: {message.payload.decode()}")
            except:
                print(f"Received message: {message.payload}")

# Coroutines (specialized generator functions) are the heart of async IO in Python.
async def publisher_coroutine():
    async with Client("test.mosquitto.org") as client:
        topic = "humidity/outside"
        
        for index, value in enumerate(range(0, 9)):
            payload = "{:.2f}".format(random.uniform(0, 100))
            
            print(f"Publishing ...\n\ttopic = {topic}\n\tpayload = {payload}")
            await client.publish(topic, payload=payload)
            
            await sleep()

def subscriber():
    asyncio.run(subscriber_coroutine())

def publisher():
    asyncio.run(publisher_coroutine())

if __name__ ==  '__main__':
    start = time.time() 

    # Concurrency encompasses both multiprocessing (ideal for CPU-bound tasks),
    # and threading (suited for IO-bound tasks).
    thread_1 = threading.Thread(target=subscriber, name="MQTT_Subscriber")
    thread_1.daemon = True 
    thread_1.start()

    thread_2 = threading.Thread(target=publisher, name="MQTT_Publisher")
    thread_2.daemon = True 
    thread_2.start()
    
    thread_2.join()
    thread_1.join()

