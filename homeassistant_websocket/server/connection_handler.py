import asyncio
import json
from .video_capture import VideoHandler
import cv2
from concurrent.futures import ThreadPoolExecutor
import logging

# Manages the server connections
# Will handle behaviour between the server, client and frontend


class ConnectionHandler:
    logging.basicConfig(level=logging.INFO)
    
    @staticmethod
    async def register(websocket, clients):
        try:
            await websocket.send(json.dumps({"message": "Connected to server"}))
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                if "client_type" in data:
                    client_type = data["client_type"]
                    if client_type == "frontend":
                        clients[websocket] = {"id": len(clients)+1, "websocket": websocket, "type": "frontend"}
                        await websocket.send(json.dumps({"message": "Registered as frontend client", "id": clients[websocket]["id"]}))
                        break
                    elif client_type == "camera_client":
                        clients[websocket] = {"id": len(clients)+1, "websocket": websocket, "type": "camera_client"}
                        await websocket.send(json.dumps({"message": "Registered as backend client", "id": clients[websocket]["id"]}))
                        break
                    else:
                        await websocket.send(json.dumps({"message": "Invalid client type"}))
            return clients[websocket]["id"]
        except Exception as e:
            logging.error(f"Error in register: {e}")

    @staticmethod
    async def unregister(websocket, clients, client_id):
        try:
            del clients[websocket]
            logging.info(f"Client {client_id} disconnected")
        except Exception as e:
            logging.error(f"Error in unregister: {e}")

    @staticmethod
    async def manage_client(websocket, clients, client_id):
        try:
            if clients[websocket]["type"] == "frontend":
                await ConnectionHandler.frontend_client_handler(websocket, client_id)
            elif clients[websocket]["type"] == "camera_client":
                await ConnectionHandler.camera_client_handler(websocket, client_id)
        except Exception as e:
            logging.error(f"Error in manage_client: {e}")

    @staticmethod
    async def frontend_client_handler(websocket, client_id):
        try:
            async for message in websocket:
                logging.info(f"Received message from {client_id}: {message}")
                if "ping" in message:
                    await websocket.send(json.dumps({"message": "pong"}))
        except Exception as e:
            logging.error(f"Error in frontend_client_handler: {e}")

    @staticmethod
    async def camera_client_handler(websocket, client_id):
        running = False
        cap = None
        executor = ThreadPoolExecutor(max_workers=1)
        capture_task = None

        async def capture_video():
            nonlocal running
            nonlocal cap
            try:
                while running:
                    ret, frame = cap.read()
                    if not ret:
                        logging.error("Error: Can't receive frame.")
                        running = False
                    else:
                        await VideoHandler.send_video_data(frame, websocket)
            except Exception as e:
                logging.error(f"Error in capture_video: {e}")
            finally:
                if cap is not None:
                    cap.release()
                    cv2.destroyAllWindows()

        try:
            async for message in websocket:
                logging.info(f"Received message from {client_id}: {message}")
                if "ping" in message:
                    await websocket.send(json.dumps({"message": "pong"}))

                if "start_video" in message:
                    if capture_task is not None and not capture_task.done():
                        logging.info("Video capture is already running")
                        continue
                    # Open the video device
                    cap = cv2.VideoCapture('/dev/video0')
                    if not cap.isOpened():
                        logging.error("Error: Camera could not be accessed.")
                        return
                    running = True
                    # Run the video capture in a separate thread
                    capture_task = asyncio.ensure_future(asyncio.get_event_loop().run_in_executor(executor, capture_video))

                if "stop_video" in message:
                    logging.info("Video stream stopped")
                    running = False
                    if capture_task is not None and not capture_task.done():
                        capture_task.cancel()
                        try:
                            await capture_task
                        except asyncio.CancelledError:
                            logging.info("Video capture task was cancelled")

        finally:
            if capture_task is not None and not capture_task.done():
                capture_task.cancel()
                try:
                    await capture_task
                except asyncio.CancelledError:
                    logging.info("Video capture task was cancelled")
            executor.shutdown(wait=True)
