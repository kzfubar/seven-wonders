import asyncio

from networking.server.AsyncServer import AsyncServer

if __name__ == "__main__":
    print("Starting WondersServer")
    asyncio.run(AsyncServer().start())
