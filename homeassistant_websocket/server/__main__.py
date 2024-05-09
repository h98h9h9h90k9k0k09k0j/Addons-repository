from .server import WebSocketServer
import logging

logging.basicConfig(level=logging.INFO)
def main() -> None:
    try:
        server = WebSocketServer()
        server.run()
    except Exception as e:
        logging.error(f"Error in server.run: {e}")


if __name__ == "__main__":
    main()