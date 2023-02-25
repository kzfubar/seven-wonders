import asyncio
from asyncio import StreamWriter
from typing import Dict, Optional

from networking.Config import Config
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import MESSAGE, COMMAND, LOGON
from networking.messaging.messageUtil import MSG_TYPE, DATA
from networking.server.ClientConnection import ClientConnection
from networking.server.Room import Room
from util.constants import KNOWN_IP


class AsyncServer:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.room_by_client: Dict[ClientConnection, Optional[Room]] = {}

        self.config = Config()
        self.known_ip = self.config.get(KNOWN_IP)
        self.host = self.config.get("host_ip")
        self.port = self.config.get("server_port")

        print("Server created")

    def _get_room(self, client: ClientConnection) -> Optional[Room]:
        return self.room_by_client.get(client)

    def _verify_ip(self, ip: str) -> bool:
        return ip in self.known_ip

    def add_ip(self, ip: str):
        self.config.add(KNOWN_IP, ip)

    # todo better handle if room already created
    def create_room(self, room_name: str) -> Room:
        while room_name in self.rooms:
            room_name += "*"
        room = Room(room_name)
        self.rooms[room_name] = room
        return room

    async def _close_connection(self, addr, writer: StreamWriter) -> None:
        print(f"Closing connection {addr}")
        writer.close()
        await writer.wait_closed()

    def get_room(self, room_name: str) -> Optional[Room]:
        return self.rooms[room_name]

    def _handle_message(self, msg: Dict, client: ClientConnection):
        print(f"{client.name} received message: {msg}")
        clean_data = msg["data"].strip("\n")
        client.msg_queue.put(clean_data)

    async def _handle_command(self, msg, client: ClientConnection):
        print(f"Received command from {client.name}: {msg}")
        args = msg["data"].split()
        cmd = args[0]
        if cmd == "start":
            room = self._get_room(client)
            if room is not None:
                await room.start_game()  # todo handle not enough players gracefully
                print("game started")
        elif cmd == "room":
            room_name = args[1]
            if room_name not in self.rooms:
                self.create_room(room_name)
            room = self.get_room(room_name)
            room.join(client)
            self.room_by_client[client] = room

    async def handle(self, reader, writer: StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"Received Connection from {addr}")
        ip = addr[0]
        if not self._verify_ip(ip):
            user_input = input(f"accept new ip connection {ip} (y/n) ").lower()
            if user_input == "y":
                self.add_ip(ip)
            if user_input == "n":
                print(f"Connection {addr} not accepted, closing!")
                return
        else:
            print("connection recognized!")

        receiver = MessageReceiver(reader)
        sender = MessageSender(writer)
        logon = await receiver.get_message()

        connection_open = True
        if not logon[MSG_TYPE] == LOGON:
            sender.send_error("Logon expected", -1)
            await self._close_connection(addr, writer)
            connection_open = False

        print(f"Received logon: {logon}")
        player_name = logon[DATA]
        client = ClientConnection(player_name, addr, sender)
        client.send_message(f"{player_name} logged on")

        while connection_open:
            msg = await receiver.get_message()
            print(f"Received {msg!r} from {addr!r}")
            if msg == '':
                await self._close_connection(addr, writer)
                connection_open = False
            if msg[MSG_TYPE] == MESSAGE:
                self._handle_message(msg, client)
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
