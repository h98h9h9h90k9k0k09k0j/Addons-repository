#!/bin/bash
#set -e

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual enviroment"

# Start FFmpeg for streaming
#ffmpeg -f video4linux2 -i /dev/video0 -vcodec libx264 -f flv rtmp://localhost/live/stream &

ffmpeg -f video4linux2 -i /dev/video0 -vcodec libx264 -f rtsp rtsp://localhost:8554/mystream &

#ffmpeg -f video4linux2 -i /dev/video0 -vcodec libx264 -f rtp rtp://localhost:1234



# Start the WebSocket server in the background
python3 /app/websocket_entry.py &
echo "started websocket server in background"

# Wait for any process to edocker run -it --entrypoint /bin/sh aleksanderrdl/hass-distribute-addon:server_alpine_aarch64
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?