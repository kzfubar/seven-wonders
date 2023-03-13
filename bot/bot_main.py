import asyncio
import sys

from bot.BotClient import BotClient
from networking.Config import Config
from networking.messaging.RemoteReceiver import RemoteReceiver
from networking.messaging.RemoteSender import RemoteSender


async def main():
    print("Launching Bot...")
    config = Config()

    host = config.get("server_ip")
    port = config.get("server_port")
    print(f"Connecting to {host}:{port}")
    reader, writer = await asyncio.open_connection(host=host, port=port)
    receiver = RemoteReceiver(reader)
    sender = RemoteSender(writer)

    client = BotClient(sys.argv[1], sender, receiver)
    await client.logon()
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
