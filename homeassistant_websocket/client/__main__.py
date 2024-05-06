from .client import Client
import asyncio

def main() -> None:
    # it is hardcoded for now
    client_id = 1
    uri = "ws://localhost:3030"
    client = Client(client_id, uri)
    asyncio.get_event_loop().run_until_complete(client.connect())


if __name__ == "__main__":
    main()