import yaml
import asyncio
import websockets

async def send_message(websocket_url, device_id, message):
    async with websockets.connect(websocket_url) as websocket:
        data = {
            "device_id": device_id,
            "message": message
        }
        await websocket.send(yaml.dump(data))

def main():
    with open("/config.yaml") as f:
        config = yaml.safe_load(f)
    
    websocket_url = config['websocket_url']
    device_id = config['device_id']
    message = "Hello, device!"
    
    asyncio.get_event_loop().run_until_complete(send_message(websocket_url, device_id, message))

if __name__ == "__main__":
    main()