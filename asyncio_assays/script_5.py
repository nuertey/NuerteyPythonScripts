# asyncio-mqtt combines the stability of the time-proven paho-mqtt 
# library with a modern, asyncio-based interface.
# 
#     No more callbacks! 👍
#     No more return codes (welcome to the MqttError)
#     Graceful disconnection (forget about on_unsubscribe, on_disconnect, etc.)
#     Compatible with async code
#     Fully type-hinted
#     Did we mention no more callbacks?

Subscriber

async with Client("test.mosquitto.org") as client:
    async with client.messages() as messages:
        await client.subscribe("humidity/#")
        async for message in messages:
            print(message.payload)

Publisher

async with Client("test.mosquitto.org") as client:
    await client.publish("humidity/outside", payload=0.38)

