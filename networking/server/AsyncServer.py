import asyncio
from asyncio import StreamWriter
from typing import Dict, Optional, List

from networking.Config import Config
from networking.server.command.Command import Command
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import MESSAGE, COMMAND, LOGON
from networking.messaging.messageUtil import MSG_TYPE, DATA
from networking.server.ClientConnection import ClientConnection
from networking.server.GameServer import GameServer
from networking.server.command.RoomCommand import RoomCommand
from networking.server.command.StartCommand import StartCommand
from util.constants import KNOWN_IP


async def _close_connection(addr, writer: StreamWriter) -> None:
    print(f"Closing connection {addr}")
    writer.close()
    await writer.wait_closed()


def _handle_message(msg: Dict, client: ClientConnection):
    print(f"{client.name} received message: {msg}")
    clean_data = msg["data"].strip("\n")
    client.msg_queue.put(clean_data)


def _server_commands(server: GameServer) -> Dict[str, Command]:
    commands = [RoomCommand(server),
                StartCommand(server)]
    return {cmd.name: cmd for cmd in commands}


class AsyncServer:
    def __init__(self):
        self.game_server: GameServer = GameServer()
        self.commands: Dict[str, Command] = _server_commands(self.game_server)

        self.config = Config()
        self.known_ip = self.config.get(KNOWN_IP)
        self.host = self.config.get("host_ip")
        self.port = self.config.get("server_port")

        print("Server created")

    def _verify_ip(self, ip: str) -> bool:
        return ip in self.known_ip

    def add_ip(self, ip: str):
        self.config.add(KNOWN_IP, ip)

    async def _handle_command(self, msg: Optional[Dict], client: ClientConnection) -> None:
        print(f"Received command from {client.name}: {msg}")
        args: List = msg["data"].split()
        cmd = args.pop(0)

        if cmd in self.commands:
            self.commands[cmd].execute(args, client)
            return

        if not self.game_server.handle_command(cmd, args, client):
            client.send_message(f"Command [{cmd}] not found")

    async def handle(self, reader, writer: StreamWriter):
        addr = writer.get_extra_info('peername')
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
                await _close_connection(addr, writer)
                return
        else:
            print("connection recognized!")

        receiver = MessageReceiver(reader)
        sender = MessageSender(writer)
        logon = await receiver.get_message()

        connection_open = True
        if not logon[MSG_TYPE] == LOGON:
            sender.send_error("Logon expected", -1)
            await _close_connection(addr, writer)
            connection_open = False

        print(f"Received logon: {logon}")
        player_name = logon[DATA].strip('\n')
        client = ClientConnection(player_name, addr, sender)
        client.send_message(f"{player_name} logged on")

        while connection_open:
            msg = await receiver.get_message()
            print(f"Received {msg!r} from {addr!r}")
            if msg == '':
                await _close_connection(addr, writer)
                connection_open = False
            if msg[MSG_TYPE] == MESSAGE:
                _handle_message(msg, client)
            elif msg[MSG_TYPE] == COMMAND:
                asyncio.create_task(self._handle_command(msg, client))
            await writer.drain()
        print(f"{addr} connection closed")

    async def start(self):
        server = await asyncio.start_server(self.handle, self.host, 9999)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()
