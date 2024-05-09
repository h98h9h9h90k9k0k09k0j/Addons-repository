# The main server module

import asyncio
import logging
import websockets
from .connection_handler import ConnectionHandler

class WebSocketServer:
    def __init__(self, host="0.0.0.0", port=3030):
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to manage connections
        logging.basicConfig(level=logging.INFO)

    async def handler(self, websocket):
        logging.info(f"Client attempting to connect from {websocket.remote_address}")
        client_id = await ConnectionHandler.register(websocket, self.clients)
        logging.info(f"New connection: {websocket.remote_address}")
        try:
            await ConnectionHandler.manage_client(websocket, self.clients, client_id)
        finally:
            await ConnectionHandler.unregister(websocket, self.clients, client_id)
            logging.info(f"Connection closed: {websocket.remote_address}")

    def run(self):
        start_server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        logging.info(f"Server started at ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_forever()


    
#Server Class indeholder:
""" O = first edition done  X = need further details before implementation  ? = unsure if needed
    - __init__                          se https://github.com/PpoSil/SSTUDE_HOUSE/blob/82fe7d5ab7750bd2ff86e7e45bf64d4854b70f8b/iot/utils/web_socket.py#L10
    - start                             se https://github.com/PpoSil/SSTUDE_HOUSE/blob/82fe7d5ab7750bd2ff86e7e45bf64d4854b70f8b/iot/utils/web_socket.py#L10
    - stop                              se https://github.com/PpoSil/SSTUDE_HOUSE/blob/82fe7d5ab7750bd2ff86e7e45bf64d4854b70f8b/iot/utils/web_socket.py#L10
    - publish/subscribe design pattern  se https://github.com/python-websockets/websockets/blob/main/experiments/broadcast/server.py
    - signal_event                      ingen held
    - logging/diagnostics/error_messages    se https://github.com/iotile/coretools/blob/642f5fefa6018c3e0c8004c90adccec6edb17702/transport_plugins/websocket/iotile_transport_websocket/websocket_implementation.py#L4
    - handle_client                     se https://github.com/psychopy/psychopy/blob/bb8ac059d06b94475d2e61f920b4c9dcaf1041a3/psychopy/liaison.py#L64 _connectionHandler metode
    - handle_command                    se måske https://github.com/diffthanatad/WaterBeats/blob/9a4c88925e3ef3e7f71f5c41629e8cd5edc7efb1/IoTActuator/actuator.py#L42
    har muligvis brug for adhoc fil. se client_handler
"""
#Rogue primitiv camera handling     se https://github.com/miracle3070/share42/blob/d388def8ccc770fd5c4218430c6b7528295d1f38/AMAG_Project/IoT/rasberrypi/webscoket.py#L4
#Rogue simulation af IoT input      se https://github.com/Priyanshu-Mallick/IOT-PROJECT/blob/a52abc5639d05cb42b7c800a83fcf8eea07c7500/Hardware/sps.py#L3