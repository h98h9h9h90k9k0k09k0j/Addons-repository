import asyncio
import websockets
import logging
import json

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

client_id = 1
uri = "ws://localhost:3030"
class Client:
    def __init__():
        pass

    async def process(data):
        #se evt. library RPi.GPIO
        pass

    async def start_listening(websocket):
        response = await websocket.recv()
        print(f"< Response from server: {response}")  # Pong
        
        if response.startswith("CMD"): #Check response start string
            data = json.loads(response.split(" ", 1)[1]) # Don't know why/how data is split up
            print("Received a command processing request.")
            result = await process(data)  # Process the data
            print("Command has been processed.")

            if result:
                print("Sending success message to server...")
                await websocket.send(f"RESULT{client_id}: Success => {result}")
            else:
                print("Sending failure message to server...")
                await websocket.send(f"RESULT{client_id}: Fail => {result}")
        else:
            await websocket.send(response)  # Send back what was received

    async def connect():
        async with websockets.connect(uri) as websocket:
            try:
                while True:
                    start_listening(websocket)
            except KeyboardInterrupt as e:
                print("Closing Client")
            finally:
                websocket.close()

    async def ping(websocket, ping_pong_interval_sec=10, message="keep going"):
        await websocket.send(message)
        response = await websocket.recv()
        print(f"< Response from the server: {response}")
        await asyncio.sleep(ping_pong_interval_sec)

    async def send_command():
        pass  #Maybe this function should just be a filter, depending on how we send commands
    
    async def send_message(websocket, data):
        message = data
        await websocket.send(data)
        print(f'Client sent: {data}')
        if message.startswith("CMD"):
            send_command()

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

class Server:
    async def __init__():
        pass

    async def start():
        pass

    async def stop():
        pass

    async def handle_command():
        pass

    async def handle_client():
        pass
    
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