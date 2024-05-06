from .server import WebSocketServer


def main() -> None:
    server = WebSocketServer()
    server.run()


if __name__ == "__main__":
    main()