#!/bin/bash

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