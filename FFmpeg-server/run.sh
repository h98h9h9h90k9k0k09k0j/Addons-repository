#!/bin/bash
#set -e

# Activate the virtual environment
source /opt/venv/bin/activate
echo "activated virtual enviroment"

#gst-inspect-1.0 v4l2src
#gst-inspect-1.0 videoconvert
#gst-inspect-1.0 v4l2h264enc
#gst-inspect-1.0 rtph264pay
#gst-inspect-1.0 gdppay
#gst-inspect-1.0 tcpserversink

#sleep 2

# Start the GStreamer pipeline
#gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! autovideosink

# test on local
#gst-launch-1.0 v4l2src device=/dev/video0 ! image/jpeg,framerate=30/1 ! jpegdec ! videoconvert ! autovideosink


#gst-launch-1.0 v4l2src device=/dev/video0 ! image/jpeg,framerate=30/1 ! jpegdec ! videoconvert ! video/x-raw,format=I420 ! x264enc ! rtph264pay config-interval=1 ! gdppay ! tcpserversink host=0.0.0.0 port=8080 

GST_DEBUG=4 gst-launch-1.0 v4l2src device=/dev/video0 ! image/jpeg,framerate=30/1 ! jpegdec ! videoconvert ! x264enc ! rtph264pay config-interval=1 ! gdppay ! tcpserversink host=0.0.0.0 port=8080

# test on local
#gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! x264enc ! mp4mux ! filesink location=/addon_configs/capture.mp4


# Start the WebSocket server in the background
python3 /app/websocket_entry.py &
echo "started websocket server in background"

# Wait for any process to edocker run -it --entrypoint /bin/sh aleksanderrdl/hass-distribute-addon:server_alpine_aarch64
echo "waiting for process to exit"
wait -n

# Exit with status of process that exited first
echo "exiting"
exit $?