
# To work with MQTT in Python using asyncio, you can use the asyncio-mqtt library. 
# Below is a simple example demonstrating how to publish and subscribe to messages:

# Explanation:
# 
#     1. Import necessary libraries:
#     Import asyncio for asynchronous operations and Client from asyncio-mqtt to interact with the MQTT broker.
#     2. Connect to the broker:
#     Create an asynchronous context manager using async with Client("localhost") as client: to establish a connection to the MQTT broker running on your local machine.
#     3. Subscribe to a topic:
#     Use await client.subscribe("my/topic") to subscribe to the desired MQTT topic.
#     4. Publish a message:
#     Use await client.publish("my/topic", payload="Hello, World!") to publish a message to the subscribed topic.
#     5. Receive messages:
#     Use async with client.filtered_messages("my/topic") as messages: to create an asynchronous iterator that filters messages based on the subscribed topic. Iterate over these messages using async for message in messages: and print the received payloads.
#     6. Run the asynchronous code:
#     Call asyncio.run(main()) to execute the asynchronous main() function. 
# 
# Installation:
# To install the asyncio-mqtt library, use pip:
# Code
# 
# pip install asyncio-mqtt

import asyncio
from asyncio_mqtt import Client

async def mqtt_client_process():
    async with Client("localhost") as client:
        await client.subscribe("my/topic")

        async with client.filtered_messages("my/topic") as messages:
            await client.publish("my/topic", payload="Hello, World!")
            async for message in messages:
                print(f"Received message: {message.payload.decode()}")

if __name__ == "__main__":
    asyncio.run(mqtt_client_process())
