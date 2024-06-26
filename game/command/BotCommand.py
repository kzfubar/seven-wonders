import asyncio
import queue
from typing import List

from bot.BotClient import BotClient
from game.command.GameCommand import GameCommand
from networking.messaging.LocalParsingSender import LocalParsingSender
from networking.messaging.LocalReceiver import LocalReceiver
from networking.messaging.LocalSender import LocalSender
from networking.server.ClientConnection import ClientConnection


class BotCommand(GameCommand):
    name: str = "bot"
    bot_type: str = "cheap"

    def execute(self, args: List, client: ClientConnection):
        bot_name = args[0]
        client_queue: queue.Queue[dict] = queue.Queue()
        client_sender = LocalSender(client_queue)
        client_receiver = LocalReceiver(client_queue)

        bot_queue: queue.Queue[dict] = queue.Queue()

        bot_sender = LocalParsingSender(bot_queue)

        bot_client = ClientConnection(bot_name, client_sender)
        bot = BotClient(bot_name, bot_sender, client_receiver, self.bot_type)

        bot_client.msg_queue = bot_queue
        self.game.player_clients.append(bot_client)
        asyncio.create_task(bot.start())
        print(self.game.player_clients)
