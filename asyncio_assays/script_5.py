# asyncio-mqtt combines the stability of the time-proven paho-mqtt 
# library with a modern, asyncio-based interface.
# 
#     No more callbacks! 👍
#     No more return codes (welcome to the MqttError)
#     Graceful disconnection (forget about on_unsubscribe, on_disconnect, etc.)
#     Compatible with async code
#     Fully type-hinted
#     Did we mention no more callbacks?
import threading
import asyncio
from asyncio_mqtt import Client

async def subscriber_coroutine():
    async with Client("test.mosquitto.org") as client:
        topic = "humidity/#"
        async with client.filtered_messages(topic) as messages:
            print(f"Subscribing to topic: {topic} ...")
            await client.subscribe(topic)
            async for message in messages:
                try:
                    print(f"Received message: {message.payload.decode()}")
                except:
                    print(f"Received message: {message.payload}")

async def publisher_coroutine():
    async with Client("test.mosquitto.org") as client:
        topic = "humidity/outside"
        payload = 0.38
        print(f"Publishing ...\n\ttopic = {topic}\n\tpayload = {payload}")
        await client.publish(topic, payload=payload)

def subscriber():
    asyncio.run(subscriber_coroutine())

def publisher():
    asyncio.run(publisher_coroutine())

if __name__ ==  '__main__':
    thread_1 = threading.Thread(target=subscriber, name="MQTT_Subscriber")
    thread_1.daemon = True 

    thread_2 = threading.Thread(target=publisher, name="MQTT_Publisher")
    thread_2.daemon = True 
    
    thread_1.start()
    thread_2.start()
    
    thread_2.join()
    thread_1.join()

