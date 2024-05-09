# Capture the video stream directly from the camera or through homeassistant api
# Will send video to client for processing

import base64
import json
    
class VideoHandler:
    @staticmethod
    async def capture_video():
        pass

    # Encode video data if needed (e.g., base64 encoding for binary data)
    @staticmethod
    async def encode_video_data(video_data):
        return base64.b64encode(video_data.encode()).decode('utf-8')
    
    @staticmethod
    async def send_video_data(frame, websocket):
        response = {"type": "video_frame", "data": frame}
        await websocket.send(json.dumps(response))
        print(f"Sent frame to {websocket.remote_address}")
