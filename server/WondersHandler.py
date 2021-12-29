from __future__ import annotations

import socketserver
from socketserver import BaseServer
from typing import Any

from game.ServerPlayer import ServerPlayer
from messaging.MessageReceiver import MessageReceiver
from messaging.MessageSender import MessageSender
from messaging.messageTypes import LOGON
from messaging.messageUtil import MSG_TYPE
from server import WondersServer
from util.util import get_wonder


class WondersHandler(socketserver.BaseRequestHandler):
    server: WondersServer.WondersServer
    player: ServerPlayer
    receiver: MessageReceiver
    sender: MessageSender

    def _handle_logon(self, msg):
        print(f"Received logon: {msg}")
        player_name = msg['playerName']
        wonder_name = msg['wonderName']
        wonder = get_wonder(wonder_name)
        if wonder is None:
            self._error_response("Wonder not found!", 1)
            return
        self.player = ServerPlayer(player_name, wonder, self.request)
        self.server.players.append(self.player)
        if len(self.server.players) == 3:
            self.server.start_game()

    def _error_response(self, error_msg: str, error_code: int):
        self.sender.send_error(error_msg=error_msg, error_code=error_code)

    def handle(self):
        print(f"Received Connection from {self.client_address}")
        self.receiver = MessageReceiver(self.request)
        self.sender = MessageSender(self.request)
        while True:
            msg = self.receiver.get_message()
            if msg is None:
                break
            if msg[MSG_TYPE] == LOGON:
                self._handle_logon(msg)
        print(f"{self.client_address} connection closed")
