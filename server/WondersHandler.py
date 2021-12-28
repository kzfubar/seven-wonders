from __future__ import annotations

import json
import socketserver

from Player import Player
from server import WondersServer
from server.PlayerConnection import PlayerConnection
from util import get_wonder


class WondersHandler(socketserver.BaseRequestHandler):
    server: WondersServer.WondersServer
    player: Player

    def _handle_logon(self, msg):
        print(f"Received logon: {msg}")
        player_name = msg['playerName']
        wonder_name = msg['wonderName']
        wonder = get_wonder(wonder_name)
        if wonder is None:
            self._error_response("Wonder not found!", 1)
            return
        self.player = Player(player_name, wonder)
        self.server.connections.append(PlayerConnection(self.player, self.request))
        if len(self.server.connections) == 3:
            self.server.start_game()

    def _error_response(self, error_msg: str, error_code: int):
        msg = {
            "msgType": "error",
            "errorMsg": error_msg,
            "errorCode": error_code,
        }
        self.request.sendall(json.dumps(msg).encode('utf-8'))

    def handle(self):
        print(f"Received Connection from {self.client_address}")
        while True:
            data = self.request.recv(1024).strip()
            if data == b'':
                break
            msg = json.loads(data.decode('utf-8'))
            if msg["msgType"] == "logon":
                self._handle_logon(msg)
        print(f"{self.client_address} connection closed")
