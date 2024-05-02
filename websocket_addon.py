import asyncio
import websockets
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

async def websocket_handler(websocket, path):
    logging.info(f"Client connected from {websocket.remote_address}")
    try:
        async for message in websocket:
            echo_message = f"Echo: {message}"
            await websocket.send(echo_message)
            logging.info(f"Received message: {message} | Sent: {echo_message}")
    except websockets.exceptions.WebSocketException as e:
        logging.error(f"A WebSocket error occurred: {e}")
    finally:
        logging.info("WebSocket connection closed.")

start_server = websockets.serve(websocket_handler, "0.0.0.0", 3030)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    logging.info("WebSocket server started on ws://0.0.0.0:3030")
    asyncio.get_event_loop().run_forever()
