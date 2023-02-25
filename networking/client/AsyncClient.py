import asyncio
import sys

from networking.Config import Config
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import MESSAGE, EVENT
from networking.messaging.messageUtil import MSG_TYPE


class AsyncClient:
    def __init__(self):
        print("Client created")

        self.receiver = None
        self.sender = None
        self.config = Config()

        self.host = self.config.get("server_ip")
        self.port = self.config.get("server_port")

    async def start(self, player_name=None):
        print(f"Connecting to {self.host}:{self.port}")
        reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
        self.receiver = MessageReceiver(reader)
        self.sender = MessageSender(writer)
        login = asyncio.create_task(self._do_logon(player_name))
        recv = asyncio.create_task(self._recv())
        take_input = asyncio.create_task(self._receive_input())

        try:
            await login
            await recv
            await take_input
        except KeyboardInterrupt:
            self._close()

    def _close(self):
        print("\nShutting down!")
        # TODO close reader and writer

    async def _do_logon(self, player_name):
        if player_name is None:
            player_name = await self.ainput("player name: ")
        self.sender.send_logon(player_name=player_name)

    def _handle_message(self, msg: dict):
        print(msg["data"])

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
                    if msg[MSG_TYPE] == MESSAGE:  # todo handle error message from the server
                        self._handle_message(msg)
                    elif msg[MSG_TYPE] == EVENT:
                        continue
                    else:
                        print(msg)
        except OSError:
            print("\nClosing recv thread")

    async def _receive_input(self):
        while True:
            message = await self.ainput()
            if message == "":
                return
            if message[0] == "/":
                self.sender.send_command(message[1:])
            else:
                self.sender.send_message(message)

    async def ainput(self, string: str = "") -> str:
        await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s + ' '))
        return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)
