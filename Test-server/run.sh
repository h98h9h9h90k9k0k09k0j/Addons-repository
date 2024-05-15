#!/bin/bash
set -e

# Start the GStreamer pipeline
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! videoconvert ! v4l2h264enc ! rtph264pay config-interval=1 ! gdppay ! tcpserversink host=0.0.0.0 port=3030

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual enviroment"

# Start the WebSocket server in the background
python3 /app/websocket_entry.py &
echo "started websocket server in background"

# Wait for any process to exit
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?