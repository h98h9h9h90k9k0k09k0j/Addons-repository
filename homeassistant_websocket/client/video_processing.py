# Does processing on the received video data
# Should respond to the server depending on the type of processing

class VideoProcessor:
    @staticmethod
    async def process_video(message, websocket, clients):
        # Placeholder for video processing logic
        pass

    @staticmethod
    async def motion_detection(message, websocket, clients):
        # Placeholder for video processing logic
        pass

    # Logic to send commands back to server depending on the processing
    @staticmethod
    async def send_command(message, websocket, clients):
        # Placeholder for sending commands back to server
        pass