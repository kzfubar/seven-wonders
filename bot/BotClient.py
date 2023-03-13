import asyncio

from bot.GamePlayer import GamePlayer
from bot.CheapPlayer import SequentialPlayer
from networking.Config import Config
from networking.messaging.MessageReceiver import MessageReceiver, EMPTY_RECEIVER
from networking.messaging.RemoteReceiver import RemoteReceiver
from networking.messaging.MessageSender import MessageSender, EMPTY_SENDER
from networking.messaging.RemoteSender import RemoteSender
from networking.messaging.messageTypes import MESSAGE, EVENT
from networking.messaging.messageUtil import MSG_TYPE, DATA, EVENT_TYPE, ROOM, GAME


class BotClient:
    def __init__(self):
        self.sender: MessageSender = EMPTY_SENDER
        self.receiver: MessageReceiver = EMPTY_RECEIVER

        self._game_player: GamePlayer = SequentialPlayer()

        self.config = Config()

        self.host = self.config.get("server_ip")
        self.port = self.config.get("server_port")
        print("Client created")

    async def start(self, player_name: str):
        print(f"Connecting to {self.host}:{self.port}")
        reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
        self.receiver = RemoteReceiver(reader)
        self.sender = RemoteSender(writer)
        login = asyncio.create_task(self._do_logon(player_name))
        recv = asyncio.create_task(self._recv())

        try:
            await login
            await recv
        except KeyboardInterrupt:
            self._close()

    def _close(self):
        print("\nShutting down!")
        # TODO close reader and writer

    async def _do_logon(self, player_name):
        self.sender.send_logon(player_name=player_name)
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
                        print("Received unknown msg" + msg)
        except OSError:
            print("\nClosing recv thread")
