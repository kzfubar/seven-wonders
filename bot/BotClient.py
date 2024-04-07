import asyncio

from bot.CheapPlayer import CheapPlayer
from bot.BasePlayer import BasePlayer
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import MESSAGE, EVENT
from networking.messaging.messageUtil import MSG_TYPE, DATA, EVENT_TYPE, ROOM, GAME


class BotClient:
    def __init__(
        self, player_name: str, sender: MessageSender, receiver: MessageReceiver
    ):
        self.player_name: str = player_name
        self.sender: MessageSender = sender
        self.receiver: MessageReceiver = receiver

        self._game_player: BasePlayer = CheapPlayer()
        print("Client created")

    async def start(self):
        recv = asyncio.create_task(self._recv())
        try:
            await recv
        except KeyboardInterrupt:
            self._close()

    def _close(self):
        print("\nShutting down!")

    async def logon(self):
        self.sender.send_logon(player_name=self.player_name)
        self.sender.send_command("room r")

    def _handle_message(self, msg: dict):
        print(msg["data"])  # Print output msg

    def _handle_event(self, event: dict):
        event_type = event[EVENT_TYPE]
        data = event[DATA]
        data_type = data["type"]
        if event_type == ROOM:
            if data_type == "room":
                if len(data["clients"]) == 3:
                    self.sender.send_command("start")
        elif event_type == GAME:
            response = self._game_player.handle_event(event)
            if response is not None:
                self.sender.send_message(response)

    async def _recv(self):
        # receive data back from the server
        try:
            while True:
                if self.receiver.is_empty():
                    await asyncio.sleep(1)
                else:
                    msg = await self.receiver.get_message()
                    if msg is None:
                        print()
                        break
                    if (
                        msg[MSG_TYPE] == MESSAGE
                    ):  # todo handle error message from the server
                        self._handle_message(msg)
                    elif msg[MSG_TYPE] == EVENT:
                        print(msg)
                        self._handle_event(msg)
                    else:
                        print("Received unknown msg" + str(msg))
        except OSError:
            print("\nClosing recv thread")
