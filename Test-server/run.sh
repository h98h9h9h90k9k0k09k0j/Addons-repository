#!/bin/bash
#set -e

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual enviroment"

gst-inspect-1.0 v4l2src
gst-inspect-1.0 videoconvert
gst-inspect-1.0 v4l2h264enc
gst-inspect-1.0 rtph264pay
gst-inspect-1.0 gdppay
gst-inspect-1.0 tcpserversink

# Start the GStreamer pipeline
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw,framerate=15/1 ! videoconvert ! v4l2h264enc ! rtph264pay config-interval=1 ! gdppay ! tcpserversink host=0.0.0.0 port=3030 

# Start the WebSocket server in the background
python3 /app/websocket_entry.py &
echo "started websocket server in background"

# Wait for any process to edocker run -it --entrypoint /bin/sh aleksanderrdl/hass-distribute-addon:server_alpine_aarch64
xit
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?