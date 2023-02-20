import asyncio

from networking.client.AsyncClient import AsyncClient

import sys

if __name__ == "__main__":
    print("Launching WondersClient...")
    client = AsyncClient()
    if len(sys.argv) > 1:
        asyncio.run(client.start(sys.argv[1]))
    else:
        asyncio.run(client.start())
