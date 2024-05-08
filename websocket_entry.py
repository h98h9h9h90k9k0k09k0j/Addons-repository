"""Runs the server or client depending on the command line arguments."""

import sys
from homeassistant_websocket.server.__main__ import main as server_main
from homeassistant_websocket.client.__main__ import main as client_main

run_type = "server"

# The user should configure in the options file whether the script should run as a server or client
def run():
    if run_type == "server":
        return server_main()
    else:
        return client_main()

if __name__ == "__main__":
    try:
        sys.exit(run())
    except KeyboardInterrupt:
        sys.exit(0)