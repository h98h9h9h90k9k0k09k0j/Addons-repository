# Capture the video stream directly from the camera or through homeassistant api
# Will send video to client for processing

import base64
import json
    
class VideoCapture:
    @staticmethod
    async def capture_video():
        # This would be the camera/homeassistant extraction logic
        # Maybe need to be called in a loop or from a callback that produces frames
        video_data = "video_stream_data"  
        return video_data
    
    # Encode video data if needed (e.g., base64 encoding for binary data)
    @staticmethod
    async def encode_video_data(video_data):
        return base64.b64encode(video_data.encode()).decode('utf-8')
    
    @staticmethod
    async def send_video_data(video_data, websocket):
        response = {"type": "video", "data": video_data}
        await websocket.send(json.dumps(response))
        print(f"Sent video data to {websocket.remote_address}")