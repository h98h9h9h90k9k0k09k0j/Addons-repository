# main client module
import asyncio
import json
import websockets
import base64
import cv2
import numpy as np
from .video_processing import VideoProcessor


class Client:
    def __init__(self, client_id: int, uri: str):
        self.uri = uri
        self.client_id = client_id

    async def process(self, frame, command):
        # Process the frame according to the command
        if command == 'motion_detection':
            VideoProcessor.motion_detection(frame)
        else:
            VideoProcessor.process_video(frame)
        # Add more options as needed

        return None  # Return the result of the processing

    async def start_listening(self, websocket):
        response = await websocket.recv()
        print(f"< Response from server: {response}")  # Pong

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

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            try:
                while True:
                    await self.start_listening(websocket)
            except KeyboardInterrupt as e:
                print("Closing Client")
            finally:
                await websocket.close()

    async def ping(websocket, ping_pong_interval_sec=10, message="keep going"):
        await websocket.send(message)
        response = await websocket.recv()
        print(f"< Response from the server: {response}")
        await asyncio.sleep(ping_pong_interval_sec)

    async def send_command(self):
        pass  #Maybe this function should just be a filter, depending on how we send commands
    
    async def send_message(self, websocket, data):
        message = data
        await websocket.send(data)
        print(f'Client sent: {data}')
        if message.startswith("CMD"):
            self.send_command()

    async def get_IoT_ip_address(websocket):
        remote_ip = websocket.remote_address[0]





#Client Class indeholder:
"""  O = first edition done  X = need further details before implementation  ? = unsure if needed
- __init__             X            improviser i guess
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

#Client connection management to Server
"""
- 
"""