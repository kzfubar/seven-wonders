import asyncio
from asyncio import StreamWriter, StreamReader
from typing import Dict, Optional, List

from networking.Config import Config
from networking.messaging.RemoteReceiver import RemoteReceiver
from networking.messaging.RemoteSender import RemoteSender
from networking.messaging.messageTypes import MESSAGE, COMMAND, LOGON
from networking.messaging.messageUtil import MSG_TYPE, DATA
from networking.server.ClientConnection import ClientConnection
from networking.server.GameServer import GameServer
from networking.server.command.Command import Command
from networking.server.command.LeaveCommand import LeaveCommand
from networking.server.command.RoomCommand import RoomCommand
from networking.server.command.StartCommand import StartCommand
from util.constants import KNOWN_IP


async def _close_connection(writer: StreamWriter) -> None:
    writer.close()
    await writer.wait_closed()


def _handle_message(msg: Dict, client: ClientConnection):
    clean_data = msg["data"].strip("\n")
    if clean_data:
        client.msg_queue.put(clean_data)


def _server_commands(server: GameServer) -> Dict[str, Command]:
    commands = [RoomCommand(server), StartCommand(server), LeaveCommand(server)]
    return {cmd.name: cmd for cmd in commands}


class AsyncServer:
    def __init__(self):
        self._game_server: GameServer = GameServer()
        self.commands: Dict[str, Command] = _server_commands(self._game_server)

        self.config = Config()
        self.known_ip = self.config.get(KNOWN_IP)
        self.host = self.config.get("host_ip")
        self.port = self.config.get("server_port")

        print("Server created")

    def _verify_ip(self, ip: str) -> bool:
        return ip in self.known_ip

    def add_ip(self, ip: str):
        self.config.add(KNOWN_IP, ip)

    async def _handle_command(
            self, msg: Optional[Dict], client: ClientConnection
    ) -> None:
        args: List = msg["data"].split()
        cmd = args.pop(0)

        if cmd in self.commands:
            self.commands[cmd].execute(args, client)
            return

        if not self.game_server.handle_command(cmd, args, client):
            client.send_message(f"Command [{cmd}] not found")

    async def _handle_connection(self, addr, writer: StreamWriter):
        print(f"Received Connection from {addr}")
        ip = addr[0]
        if not self._verify_ip(ip):
            # todo make this not hang the server?
            user_input = input(f"accept new ip connection {ip} (y/n) ").lower()
            if user_input == "y":
                self.add_ip(ip)
                print(f"Connection {addr} accepted")
            if user_input == "n":
                print(f"Connection {addr} not accepted, closing connection")
                await _close_connection(writer)
                return
        else:
            print("connection recognized!")

    async def _handle_kernel(self, addr, reader: StreamReader, writer: StreamWriter):
        receiver = RemoteReceiver(reader)
        sender = RemoteSender(writer)
        logon = await receiver.get_message()

        if not logon[MSG_TYPE] == LOGON:
            sender.send_error("Logon expected", -1)
            await _close_connection(writer)
            return

        print(f"Received logon: {logon}")
        player_name = logon[DATA].strip("\n")
        client = ClientConnection(player_name, sender)
        client.send_message(f"{player_name} logged on")

        while True:
            msg = await receiver.get_message()
            print(f"Received {msg} from {client.name}")
            if msg is None or msg == "":
                await _close_connection(writer)
                self._game_server.cleanup(client)
                print(f"{player_name} :: {addr} connection closed")
                return
            elif msg[MSG_TYPE] == MESSAGE:
                _handle_message(msg, client)
            elif msg[MSG_TYPE] == COMMAND:
                asyncio.create_task(self._handle_command(msg, client))
            await writer.drain()

    async def _handle(self, reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info("peername")
        await self._handle_connection(addr, writer)
        try:
            await self._handle_kernel(addr, reader, writer)
        except ConnectionResetError:
            print("Connection reset")

    async def start(self):
        server = await asyncio.start_server(self._handle, self.host, 9999)
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs}")
        async with server:
            await server.serve_forever()
