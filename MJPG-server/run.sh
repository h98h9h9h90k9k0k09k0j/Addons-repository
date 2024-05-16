#!/bin/bash
#set -e

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual enviroment"

mjpg_streamer -i "input_uvc.so -d /dev/video0" -o "output_http.so -w ./www" &

# Start the WebSocket server in the background
python3 /app/websocket_entry.py &
echo "started websocket server in background"

# Wait for any process to edocker run -it --entrypoint /bin/sh aleksanderrdl/hass-distribute-addon:server_alpine_aarch64
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?