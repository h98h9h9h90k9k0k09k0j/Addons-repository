# Manages the server connections
# Will handle behaviour between the server, client and frontend

import asyncio
import json
from server.video_capture import VideoCapture

class ConnectionHandler:
    @staticmethod
    async def register(websocket, clients):
        clients[websocket] = {"id": len(clients)+1, "websocket": websocket}
        await websocket.send(json.dumps({"message": "Connected to server", "id": clients[websocket]["id"]}))
        return clients[websocket]["id"]

    @staticmethod
    async def unregister(websocket, clients, client_id):
        del clients[websocket]
        print(f"Client {client_id} disconnected")

    @staticmethod
    async def manage_client(websocket, clients, client_id, VideoCapture):
        async for message in websocket:
            print(f"Received message from {client_id}: {message}")

            # Assuming the message triggers video streaming
            if "video" in message:
                # Here we might need to parse the message further to understand what type of video action is needed
                video_data = await VideoCapture.capture_video()
                # await VideoCapture.encode_video_data(video_data)
                await VideoCapture.send_video_data(video_data, websocket)

    @staticmethod
    async def send_to_all(message, clients):
        for client in clients.values():
            await client['websocket'].send(message)
