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

#Client Class indeholder:
"""
- __init__                          improviser i guess
- publish/subscribe design pattern  se https://github.com/python-websockets/websockets/blob/main/experiments/broadcast/server.py eller https://github.com/python-websockets/websockets/issues/124 4.kommentar
- get_IoT                           se https://p403n1x87.github.io/iot-with-websockets-and-pythons-asyncio.html God gennemgang
- get_IoT_ip_address                se https://websockets.readthedocs.io/en/stable/faq/server.html ctrl+f ip ad
- set_wifi_credentials              se https://github.com/search?q=repo%3Ahome-assistant-libs/python-matter-server%20set_wifi_credentials&type=code bøvlet = nødvendigt?
- ping/pong_IoT                     se https://github.com/alpapago/brushbuddy/blob/57aca96a7a1189337a5d738a21c2998f6fd2a694/IoT/client.py#L2
- logging/diagnostics/error_messages    se https://github.com/iotile/coretools/blob/642f5fefa6018c3e0c8004c90adccec6edb17702/transport_plugins/websocket/iotile_transport_websocket/websocket_implementation.py#L4 ellers https://websockets.readthedocs.io/en/stable/howto/cheatsheet.html
- remove_IoT                        bare delete?
- send_message                      se https://blog.stackademic.com/websockets-in-python-e8f845d52640
- send_command                      det samme som ^^^^^^ ?
- handle_event                      se https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
- connect                           se https://websockets.readthedocs.io/en/stable/faq/client.html
- start_listening                   se https://community.tempest.earth/t/basic-python-websockets-example-to-retrieve-current-tempest-data/9310/2 basically bare .recv()
- disconnect                        se https://websockets.readthedocs.io/en/stable/faq/client.html
- parse_data                        se https://pypi.org/project/RPi.GPIO/ pga. https://dataheadhunters.com/academy/how-to-use-python-for-iot-projects-detailed-steps/ ref
"""

#Client connection management to Server
"""
- 
"""
#Server Class indeholder:
"""
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