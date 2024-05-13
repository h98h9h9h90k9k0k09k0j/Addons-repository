# main client module
import asyncio
import logging
import json
import websockets
import base64
import cv2
import numpy as np
import psutil
import os
import aiofiles
import time
from datetime import datetime
from .video_processing import VideoProcessor
from concurrent.futures import ThreadPoolExecutor


class Client:
    def __init__(self, client_id: int, uri: str):
        self.uri = uri
        self.client_id = client_id

    """ abstraction
    async def send_message(websocket, message):
        try:
            await websocket.send(message)
        except Exception as e:
            logging.error(f"Error occurred while sending message: {e}")
    """

    """ If we need to send the videofeed forward
    async def video_forwarded(self, websocket):
        try:
        # Forward the livestream to the server
            cap = cv2.VideoCapture(0)  # Capture frames from camera 0 
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Encode frame to base64
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer)

                # Send frame to the server
                await websocket.send(frame_base64)

            cap.release()
        except Exception as e:
            logging.error(f"Error occurred during livestream forwarding: {e}")
    """
    async def get_cpu_usage(self):
        return psutil.cpu_percent()
        
    async def get_cpu_load_avg(self):
        return psutil.getloadavg()[0]

    async def get_cpu_vmem(self):
        return psutil.virtual_memory().percent

    async def update_status(self, websocket):
        threshold_pct = 70
        duration_seconds = 20
        metric_functions = {
            "load": get_cpu_load_avg,
            "vmem_pct": get_cpu_vmem,
            "cpu_usage": get_cpu_usage
        }
        while True:
            surpassing_metric = None
            for metric, func in metric_functions.items(): 
                metric_value = await func()
                if metric_value > threshold_pct:
                    surpassing_metric = metric
                    break

            if surpassing_metric:
                start_time = asyncio.get_event_loop().time()

                while True:
                    usage_pct = await metric_functions[surpassing_metric]()

                    if usage_pct <= threshold_pct:
                        break

                    if asyncio.get_event_loop().time() - start_time >= duration_seconds:
                        await websocket.send(f"Caution! Client {self.client_id} {surpassing_metric} is working at {usage_pct}%!")
                        break

                    asyncio.sleep(1)

            asyncio.sleep(10)

    async def send_frames_to_server(self, websocket):
        self.img_folder = "img_motion_det"
        try:
            for filename in os.listdir(self.img_folder):
                if filename.endswith(".jpg"):
                    image_path = os.path.join(self.img_folder, filename)
                    async with aiofiles.open(image_path, mode="rb") as f:
                        image_data = await f.read()
                    encoded_image = base64.b64encode(image_data).decode("utf-8") # skal måske ikke bruges
                    await websocket.send(encoded_image) # Overvej om det er json.dump vi skal bruge
                    print(f"Sent {filename} to the server.")
                    os.remove(image_path)  # Delete the sent image. Image no longer occupies space. Do we wanna save this?
            print("All frames sent to the server.")
        except Exception as e:
            logging.error(f"Error occurred while sending frames to the server: {e}")

    def delete_frames(self):
        try:
            for filename in os.listdir(self.img_folder):
                if filename.endswith(".jpg"):
                    image_path = os.path.join(self.img_folder, filename)
                    os.remove(image_path)
                    print(f"Deleted {filename}.")
            print("All frames deleted.")
        except Exception as e:
            logging.error(f"Error occurred while deleting frames: {e}")

    async def process(self, frame, command, message):
        executor = ThreadPoolExecutor(max_workers=1)
        capture_task = None
        try: 
            # Process the frame according to the command
            if command == 'motion_detection':
                if capture_task is not None and not capture_task.done():
                    logging.info("Video capture is already running")
                capture_task = asyncio.ensure_future(asyncio.get_event_loop().run_in_executor(executor, VideoProcessor.motion_detection(frame)))
                message = 'Motion detected. Do you want to send the frames to the server? (yes/no)'
                return message
            elif command == 'detect_motion':
                if await VideoProcessor.motion_detected(frame):
                    message = 'Motion detected'
                    return message
                    # await self.video_forwarded(websocket)
            elif command == 'emotion':
                if capture_task is not None and not capture_task.done():
                    logging.info("Video capture is already running")
                VideoProcessor.emotion_recognition(frame)
                capture_task = asyncio.ensure_future(asyncio.get_event_loop().run_in_executor(executor, VideoProcessor.emotion_recognition(frame)))
            else:
                VideoProcessor.process_video(frame)
            # Add more options as needed

            executor.shutdown(wait=True)
            return None  # Return the result of the processing
        except Exception as e:
            logging.error(f"Error occurred during processing: {e}")
            return None

    async def start_listening(self, websocket):
        try:
            logging.info(f"Client {self.client_id} is now listening to the server.")
            await self.ping(websocket)
            await self.update_status(websocket)
            response = await websocket.recv()
            if response.startswith("CMD"):  # Check response start string
                command = response.split(" ", 1)[1]  # Extract the command
                print("Received a command processing request.")
            else:
                # Decode the frame
                b64_decoded = base64.b64decode(response)
                np_data = np.frombuffer(b64_decoded, dtype=np.uint8)
                frame = cv2.imdecode(np_data, flags=1)

                # Process the frame
                result = await self.process(frame, command) #Hvor kommer command fra? lige nu kan command undgås i linje 125
                print("Frame has been processed.")

                if result:
                    print("Sending success message to server...")
                    await websocket.send(f"RESULT{self.client_id}: Success => {result}")
                    response = input("Do you wish to retrieve the images? (yes/no): ").lower()
                    if response == "yes":
                        print("Sending frames to the server...")
                        await self.send_frames_to_server(websocket)
                    else:
                        print("Frames will not be sent to the server. Deleting frames...")
                        self.delete_frames()
                else:
                    print("Sending failure message to server...")
                    await websocket.send(f"RESULT{self.client_id}: Fail => {result}")
        except websockets.exceptions.ConnectionClosedError as e:
            logging.error(f"Connection to server closed unexpectedly: {e}")
        except Exception as e:
            logging.error(f"Error occurred during the communication with server: {e}")
    
    async def connect(self):
        logging.info(f"Client {self.client_id} trying to connect to the server.")
        async with websockets.connect(self.uri) as websocket:
            response = await websocket.recv()
            message = json.loads(response)
            logging.info(f"< Response from server: {message}")  # Pong

            logging.info(f"Client {self.client_id} trying to specify client type to the server.")
            await websocket.send(json.dumps({"client_type":"camera_client"}))
            response = await websocket.recv()
            message = json.loads(response)
            logging.info(f"< Response from server: {message}")  # Pong
            try:
                while True:
                    await self.start_listening(websocket)
            except KeyboardInterrupt as e:
                print(f"Closing Client: {e}")
            finally:
                await websocket.close()

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
        asyncio.get_event_loop().run_forever()

    async def ping(self, websocket, ping_pong_interval_sec=10):
        try:
            await websocket.send(json.dumps({"message": "ping"}))
            response = await websocket.recv()
            logging.info(f"< Response from the server: {response}")
            # await asyncio.sleep(ping_pong_interval_sec)
        except Exception as e:
            logging.error(f"Error occurred during ping-pong: {e}")

    async def get_IoT_ip_address(websocket):
        try:
            remote_ip = websocket.remote_address[0]
            return remote_ip
        except Exception as e:
            logging.error(f"Error occurred while retrieving remote IP address: {e}")
            return None

# Task list: 1) G̶e̶n̶n̶e̶m̶g̶a̶n̶g̶.̶ 2) L̶o̶g̶i̶k̶ t̶i̶l̶ f̶r̶a̶m̶e̶h̶a̶n̶d̶l̶i̶n̶g̶ +̶ t̶a̶g̶s̶/̶h̶o̶m̶e̶g̶r̶o̶w̶n̶ "̶m̶e̶t̶a̶d̶a̶t̶a̶"̶ f̶r̶a̶ v̶i̶d̶e̶o̶f̶e̶e̶d̶ t̶i̶l̶ s̶e̶r̶v̶e̶r̶. 3) L̶a̶v̶ e̶n̶ c̶o̶m̶m̶a̶n̶d̶ l̶i̶s̶t̶ + m̶a̶n̶a̶g̶e̶m̶e̶n̶t̶.̶ 4) L̶o̶g̶g̶i̶n̶g̶.

# E̶t̶a̶b̶l̶e̶r̶ p̶i̶n̶g̶ c̶o̶n̶n̶e̶c̶t̶i̶o̶n̶ + d̶e̶t̶e̶c̶t̶ m̶o̶t̶i̶o̶n̶ p̶l̶a̶c̶e̶h̶o̶l̶d̶e̶r̶

# Overvej Executor til at wrap video processoren i en stand alone thread. Threading or await?
# Refactor structure

# Command list: H̶a̶n̶d̶s̶h̶a̶k̶e̶, c̶a̶m̶e̶r̶a̶ s̶e̶t̶t̶i̶n̶g̶s̶, d̶a̶t̶a̶ t̶r̶a̶n̶s̶f̶e̶r̶, request/response, 
# Load balancing, e̶r̶r̶o̶r̶ h̶a̶n̶d̶l̶i̶n̶g̶, p̶i̶n̶g̶/̶p̶o̶n̶g̶, s̶t̶a̶t̶u̶s̶ u̶p̶d̶a̶t̶e̶, program updates, shutdown/restart.

#Client Class indeholder:
"""  O = first edition done  X = need further details before implementation  ? = unsure if needed
- __init__             O            improviser i guess
- publish/subscribe design pattern  se https://github.com/python-websockets/websockets/blob/main/experiments/broadcast/server.py eller https://github.com/python-websockets/websockets/issues/124 4.kommentar
- get_IoT              ?            Link ubrugeligt 
- get_IoT_ip_address   X            se https://websockets.readthedocs.io/en/stable/faq/server.html ctrl+f ip ad
- set_wifi_credentials ?            se https://github.com/search?q=repo%3Ahome-assistant-libs/python-matter-server%20set_wifi_credentials&type=code bøvlet = nødvendigt?
- ping/pong_IoT        O            se https://github.com/alpapago/brushbuddy/blob/57aca96a7a1189337a5d738a21c2998f6fd2a694/IoT/client.py#L2
- logging/diagnostics/error_messages    se https://github.com/iotile/coretools/blob/642f5fefa6018c3e0c8004c90adccec6edb17702/transport_plugins/websocket/iotile_transport_websocket/websocket_implementation.py#L4 ellers https://websockets.readthedocs.io/en/stable/howto/cheatsheet.html
- remove_IoT           ?            bare delete?
- send_message         O            se https://blog.stackademic.com/websockets-in-python-e8f845d52640
- send_command         X            det samme som ^^^^^^ ?
- handle_event         ?            se https://websockets.readthedocs.io/en/stable/intro/tutorial1.html  Minder meget om process(data) = nødvendigt?
- connect              O            se https://websockets.readthedocs.io/en/stable/faq/client.html
- start_listening      O            se https://community.tempest.earth/t/basic-python-websockets-example-to-retrieve-current-tempest-data/9310/2 basically bare .recv()
- disconnect           O            se https://websockets.readthedocs.io/en/stable/faq/client.html
- parse_data           X            se https://pypi.org/project/RPi.GPIO/ pga. https://dataheadhunters.com/academy/how-to-use-python-for-iot-projects-detailed-steps/ ref
"""