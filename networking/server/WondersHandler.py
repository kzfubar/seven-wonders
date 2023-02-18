from __future__ import annotations

import socketserver
from typing import Optional

from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import LOGON, MESSAGE, COMMAND
from networking.messaging.messageUtil import MSG_TYPE
from networking.server import WondersServer
from networking.server.Client import Client
from networking.server.Room import Room


class WondersHandler(socketserver.BaseRequestHandler):
    server: WondersServer.WondersServer
    client: Client
    receiver: MessageReceiver
    sender: MessageSender

    def _get_room(self) -> Optional[Room]:
        return self.server.clients.get(self.client.name)

    def _handle_logon(self, msg):
        print(f"Received logon: {msg}")
        player_name = msg["playerName"]
        self.client = Client(player_name, self.request)

    def _handle_message(self, msg):
        print(f"{self.client_address} {self.client.name} received message: {msg}")
        self.client.msg_queue.put(msg["data"])

    def _handle_command(self, msg):
        print(f"{self.client_address} received command: {msg}")
        args = msg["data"].split()
        cmd = args[0]
        if cmd == "start":
            room = self._get_room()
            print(self.server.clients)
            if room is not None:
                room.start_game()  # todo handle not enough players gracefully
        elif cmd == "room":
            room_name = args[1]
            if room_name not in self.server.rooms:
                self.server.create_room(room_name)
            room = self.server.get_room(room_name)
            room.join(self.client)
            self.server.clients[self.client.name] = room

    def _error_response(self, error_msg: str, error_code: int):
        self.sender.send_error(error_msg=error_msg, error_code=error_code)

    def _verify_ip(self, ip: str) -> bool:
        return ip in self.server.known_ip

    def handle(self):
        print(f"Received Connection from {self.client_address}")
        ip = self.client_address[0]
        if not self._verify_ip(ip):
            user_input = input(f"accept new ip connection {ip} (y/n) ").lower()
            if user_input == "y":
                self.server.add_ip(ip)
            if user_input == "n":
                print(f"Connection {self.client_address} not accepted, closing!")
                return
        else:
            print("connection recognized!")
        self.receiver = MessageReceiver(self.request)
        self.sender = MessageSender(self.request)
        while True:
            msg = self.receiver.get_message()
            if msg is None:
                break
            if msg[MSG_TYPE] == LOGON:
                self._handle_logon(msg)
            elif msg[MSG_TYPE] == MESSAGE:
                self._handle_message(msg)
            elif msg[MSG_TYPE] == COMMAND:
                self._handle_command(msg)
        print(f"{self.client_address} connection closed")
