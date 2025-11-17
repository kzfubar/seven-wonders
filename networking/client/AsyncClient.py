import asyncio
import sys

from networking.Config import Config
from networking.messaging.messageTypes import EVENT, MESSAGE
from networking.messaging.messageUtil import MSG_TYPE
from networking.messaging.RemoteReceiver import RemoteReceiver
from networking.messaging.RemoteSender import RemoteSender


class AsyncClient:
    def __init__(self) -> None:
        print("Client created")

        self.receiver: RemoteReceiver | None = None
        self.sender: RemoteSender | None = None
        self.config = Config()

        self.host = self.config.get("server_ip")
        self.port = self.config.get("server_port")

    async def start(self, player_name: str | None = None) -> None:
        print(f"Connecting to {self.host}:{self.port}")
        reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
        self.receiver = RemoteReceiver(reader)
        self.sender = RemoteSender(writer)
        login = asyncio.create_task(self._do_logon(player_name))
        recv = asyncio.create_task(self._recv())
        take_input = asyncio.create_task(self._receive_input())

        try:
            await login
            await recv
            await take_input
        except KeyboardInterrupt:
            self._close()

    def _close(self) -> None:
        print("\nShutting down!")
        # TODO close reader and writer

    async def _do_logon(self, player_name: str | None) -> None:
        if self.sender is None:
            raise Exception("Sender is None")
        if player_name is None:
            player_name = await self.ainput("player name: ")
        self.sender.send_logon(player_name=player_name)

    def _handle_message(self, msg: dict) -> None:
        print(msg["data"])  # Print output msg

    async def _recv(self) -> None:
        # receive data back from the server
        if self.receiver is None:
            return
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
                        continue
                    else:
                        print(f"Received unknown msg {msg}")
        except OSError:
            print("\nClosing recv thread")

    async def _receive_input(self) -> None:
        if self.sender is None:
            raise Exception("Sender is None")
        while True:
            message = await self.ainput()
            if not message:
                return
            if message[0] == "/":
                self.sender.send_command(message[1:])
            else:
                self.sender.send_message(message)

    async def ainput(self, string: str = "") -> str:
        await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s)
        )
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
