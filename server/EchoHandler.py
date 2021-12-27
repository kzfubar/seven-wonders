from __future__ import annotations

import socketserver
from server import EchoServer


class EchoHandler(socketserver.BaseRequestHandler):
    server: EchoServer.EchoServer

    def handle(self):
        print(f"Received Connection from {self.client_address}")
        while True:
            # self.request is the TCP socket connected to the client
            data = self.request.recv(1024).strip()
            if data == b'':
                break
            print(f"{self.client_address} wrote: {data}")
            # just send back the same data, but upper-cased
            self.request.sendall(self.server.get_tag() + data.upper())
        print(f"{self.client_address} connection closed")
