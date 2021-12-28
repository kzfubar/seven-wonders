import json
import socket


class WondersClient:
    HOST = "localhost"
    PORT = 9998

    def __init__(self):
        # create a TCP socket
        print("WondersClient created")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # connect to server
        print(f"WondersClient connecting to {self.HOST}:{self.PORT}")
        self.sock.connect((self.HOST, self.PORT))
        self._do_logon()
        try:
            while True:
                self._receive_input()
        except KeyboardInterrupt:
            self._close()

    def _close(self):
        # shut down
        print("\nWondersClient shutting down!")
        self.sock.close()

    def _do_logon(self):
        player_name = input("player name: ")
        wonder_name = input("wonder name: ")  # todo support random
        msg = {
            "msgType": "logon",
            "playerName": player_name,
            "wonderName": wonder_name
        }
        self.sock.sendall(json.dumps(msg).encode('utf-8'))

    def _receive_input(self):
        data = input("input: ")
        self.sock.sendall(bytes(data, encoding='utf8'))

        # receive data back from the server
        received = str(self.sock.recv(1024))
        print(f"received: {received}")

