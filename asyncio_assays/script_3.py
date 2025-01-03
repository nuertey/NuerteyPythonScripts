# Explanation:
# 
#     Import necessary libraries:
#         asyncio for asynchronous operations.
#         websockets for WebSocket client functionality. 
#     Define an asynchronous function:
#         hello() is an asynchronous function that handles the WebSocket connection and communication. 
#     Connect to the WebSocket server:
#         websockets.connect("ws://localhost:8765") establishes a connection to the WebSocket server running on localhost at port 8765.
#         The async with statement ensures proper cleanup of the connection. 
#     Send a message to the server:
#         await websocket.send("Hello, server!") sends a message to the server. 
#     Receive a message from the server:
#         greeting = await websocket.recv() receives a message from the server and stores it in the greeting variable. 
#     Print the received message:
#         print(f"Received: {greeting}") prints the received message to the console. 
#     Run the asynchronous function:
#         asyncio.run(hello()) executes the hello() function within an asyncio event loop. 
# 
# To run this example:
# 
#     Make sure you have a WebSocket server running on ws://localhost:8765. You can find examples of WebSocket servers in the websockets documentation.
#     Install the websockets library: 
# 
# Code
# 
#    pip install websockets
# 
#     Run the client script: 
# 
# Code
# 
#    python your_client_script.py
# 
# Replace "ws://localhost:8765" with the actual address of your WebSocket server.

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello, server!")
        greeting = await websocket.recv()
        print(f"Received: {greeting}")

asyncio.run(hello())
