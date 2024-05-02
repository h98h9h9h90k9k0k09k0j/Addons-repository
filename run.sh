#!/bin/bash

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual enviroment"

# Start the WebSocket server in the background
python3 /app/websocket_addon.py &
echo "started websocket server in background"

# Serve static files from the public directory on port 8080
cd /app/dashboard/public
python3 -m http.server 8000 &
echo "serve static files on port 8000"

# Wait for any process to exit
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?