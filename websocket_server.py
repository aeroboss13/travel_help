import asyncio
import websockets

# List to keep track of connected clients
clients = set()

async def handle_chat(websocket, path):
    # Add the client to the set of connected clients
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the received message to all connected clients
            await asyncio.gather(*[client.send(message) for client in clients])
    finally:
        # Remove the client from the set upon disconnection
        clients.remove(websocket)

async def main():
    # Set up the WebSocket server
    server = await websockets.serve(handle_chat, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
