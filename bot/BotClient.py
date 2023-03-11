import asyncio
import random

from networking.Config import Config
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import MESSAGE, EVENT
from networking.messaging.messageUtil import MSG_TYPE, EVENT_TYPE, DATA


class BotClient:
    sender: MessageSender

    def __init__(self):
        print("Client created")
        self.player_state = {'hand': []}
        self.receiver = None
        self.config = Config()

        self.host = self.config.get("server_ip")
        self.port = self.config.get("server_port")

    async def start(self, player_name: str):
        print(f"Connecting to {self.host}:{self.port}")
        reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
        self.receiver = MessageReceiver(reader)
        self.sender = MessageSender(writer)
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
        if data_type == "room":
            if len(data["clients"]) == 3:
                self.sender.send_command("start")
        elif data_type == "hand":
            self.player_state["hand"] = data["hand"]
            print(self.player_state)
        elif data_type == "wonder_selection":
            self.sender.send_message(random.choice(data["options"]))
        elif data_type == "input":
            self.sender.send_message(random.choice(data["options"]) + str(random.randrange(0, len(self.player_state["hand"]))))
        elif data_type == "payment":
            self.sender.send_message(random.choice(data["options"]))

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

