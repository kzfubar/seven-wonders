import asyncio
import sys

from bot.BotClient import BotClient

if __name__ == "__main__":
    print("Launching Bot...")
    client = BotClient()
    asyncio.run(client.start(sys.argv[1]))
