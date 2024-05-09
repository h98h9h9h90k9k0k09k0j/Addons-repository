from .client import Client
import asyncio

def main() -> None:
    # it is hardcoded for now
    client_id = 1
    uri = "ws://host.docker.internal:3030"
    client = Client(client_id, uri)
    client.run()


if __name__ == "__main__":
    main()