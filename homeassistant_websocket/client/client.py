# main client module
import asyncio
import logging
import json
import websockets
import base64
import cv2
import numpy as np
import psutil
from datetime import datetime
from .video_processing import VideoProcessor


class Client:
    def __init__(self, client_id: int, uri: str):
        self.uri = uri
        self.client_id = client_id
        self.status = 0

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
        cpu_usage = psutil.cpu_percent()
        return cpu_usage
    
    async def update_status(self, websocket):
        self.status = await self.get_cpu_usage()
        if self.status > 80:
            await websocket.send(f"Caution! Client {self.client_id} working at {self.status}%")

    async def process(self, frame, command, message):
        try: 
            # Process the frame according to the command
            if command == 'motion_detection':
                VideoProcessor.motion_detection(frame)
            elif command == 'detect_motion':
                if VideoProcessor.motion_detected is True:
                    message = 'Motion detected'
                    return message
                    # await self.video_forwarded(websocket)
            elif command == 'emotion':
                VideoProcessor.emotion_recognition(frame)
            else:
                VideoProcessor.process_video(frame)
            # Add more options as needed

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
                result = await self.process(frame, command)
                print("Frame has been processed.")

                if result:
                    print("Sending success message to server...")
                    await websocket.send(f"RESULT{self.client_id}: Success => {result}")
                else:
                    print("Sending failure message to server...")
                    await websocket.send(f"RESULT{self.client_id}: Fail => {result}")
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

# Task list: 1) G̶e̶n̶n̶e̶m̶g̶a̶n̶g̶.̶ 2) Logik til framehandling + tags/homegrown "metadata" fra videofeed til server. 3) L̶a̶v̶ e̶n̶ c̶o̶m̶m̶a̶n̶d̶ l̶i̶s̶t̶ + m̶a̶n̶a̶g̶e̶m̶e̶n̶t̶.̶ 4) L̶o̶g̶g̶i̶n̶g̶.

# E̶t̶a̶b̶l̶e̶r̶ p̶i̶n̶g̶ c̶o̶n̶n̶e̶c̶t̶i̶o̶n̶ + d̶e̶t̶e̶c̶t̶ m̶o̶t̶i̶o̶n̶ p̶l̶a̶c̶e̶h̶o̶l̶d̶e̶r̶

# Overvej Executor til at wrap video processoren i en stand alone thread.

# Command list: H̶a̶n̶d̶s̶h̶a̶k̶e̶, camera settings, data transfer, request/response, 
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