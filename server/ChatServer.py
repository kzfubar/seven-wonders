import socketserver
from socket import SocketType
from typing import Dict, Any

from server import ChatHandler


class ChatServer(socketserver.ThreadingTCPServer):
    HOST = "localhost"
    PORT = 9998
    connections: Dict[Any, SocketType] = {}

    def __init__(self):
        super().__init__((self.HOST, self.PORT), ChatHandler.ChatHandler)
        print("ChatServer created")

    def start(self):
        try:
            print("ChatServer Started!")
            self.serve_forever()
        except KeyboardInterrupt:
            print("ChatServer Closed!")
            # todo close the server even if there are still clients
            # todo oh my.. printing to terminal wipes out the text
            # todo we'd need a gui or something to fix this... probably not urgent tho


if __name__ == "__main__":
    print("Starting ChatServer")
    ChatServer().start()
