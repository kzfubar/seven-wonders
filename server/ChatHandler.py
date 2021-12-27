from __future__ import annotations

import socketserver
from server import ChatServer


class ChatHandler(socketserver.BaseRequestHandler):
    server: ChatServer.ChatServer

    def handle(self):
        print(f"Received Connection from {self.client_address}")
        self.server.connections[self.client_address] = self.request
        while True:
            # self.request is the TCP socket connected to the client
            data = self.request.recv(1024).strip()
            if data == b'':
                break
            print(f"{self.client_address} wrote: {data}")
            # just send back the same data, but upper-cased
            for k, v in self.server.connections.items():
                if k != self.client_address:
                    v.sendall(bytes(str(self.client_address[1]) + " says: ", encoding="utf8") + data.upper())
        print(f"{self.client_address} connection closed")
