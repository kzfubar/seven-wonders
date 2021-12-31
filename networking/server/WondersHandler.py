from __future__ import annotations

import socketserver

from game.ServerPlayer import ServerPlayer
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import LOGON, MESSAGE, COMMAND
from networking.messaging.messageUtil import MSG_TYPE
from networking.server import WondersServer
from util.util import get_wonder


class WondersHandler(socketserver.BaseRequestHandler):
    server: WondersServer.WondersServer
    player: ServerPlayer  # todo don't persist the player across games, create a new player
    receiver: MessageReceiver
    sender: MessageSender

    def _handle_logon(self, msg):
        print(f"Received logon: {msg}")
        player_name = msg['playerName']
        wonder_name = msg['wonderName']
        wonder = get_wonder(wonder_name)
        if wonder is None:
            self._error_response("Wonder not found!", 1)
            return  # todo kill the connection, or ask for a different wonder name if this happens
        self.player = ServerPlayer(player_name, wonder, self.request)
        self.server.players.append(self.player)

    def _handle_message(self, msg):
        print(f"{self.client_address} received message: {msg}")
        self.player.message_queue.put(msg['data'])

    def _handle_command(self, msg):
        print(f"{self.client_address} received command: {msg}")
        if msg['data'] == 'start':
            self.server.start_game()
            return

    def _error_response(self, error_msg: str, error_code: int):
        self.sender.send_error(error_msg=error_msg, error_code=error_code)

    def _verify_ip(self, ip: str) -> bool:
        return ip in self.server.known_ip

    def handle(self):
        print(f"Received Connection from {self.client_address}")
        ip = self.client_address[0]
        if not self._verify_ip(ip):
            user_input = input(f"accept new ip connection {ip} (y/n) ").lower()
            if user_input == 'y':
                self.server.add_ip(ip)
            if user_input == 'n':
                print(f"Connection {self.client_address} not accepted, closing!")
                return
        else:
            print("connection recognized!")
        self.receiver = MessageReceiver(self.request)
        self.sender = MessageSender(self.request)
        while True:
            msg = self.receiver.get_message()
            print(msg)
            if msg is None:
                break
            if msg[MSG_TYPE] == LOGON:
                self._handle_logon(msg)
            elif msg[MSG_TYPE] == MESSAGE:
                self._handle_message(msg)
            elif msg[MSG_TYPE] == COMMAND:
                self._handle_command(msg)
        print(f"{self.client_address} connection closed")
