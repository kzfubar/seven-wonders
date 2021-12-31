import socket
import threading

from networking.Config import Config
from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.MessageSender import MessageSender
from networking.messaging.messageTypes import MESSAGE
from networking.messaging.messageUtil import MSG_TYPE


class WondersClient:
    def __init__(self):
        # create a TCP socket
        print("WondersClient created")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver = MessageReceiver(self.sock)
        self.sender = MessageSender(self.sock)
        self.config = Config()

        self.host = self.config.get("server_ip")
        self.port = self.config.get("server_port")

    def start(self, player_name=None, wonder_name=None):
        # connect to server
        print(f"WondersClient connecting to {self.host}:{self.port}")
        self.sock.connect((self.host, self.port))
        threading.Thread(target=self._recv).start()
        self._do_logon(player_name, wonder_name)
        try:
            while True:
                self._receive_input()
        except KeyboardInterrupt:
            self._close()

    def _close(self):
        # shut down
        print("\nWondersClient shutting down!")
        self.sock.close()

    def _do_logon(self, player_name, wonder_name):
        if player_name is None:
            player_name = input("player name: ")
        if wonder_name is None:
            wonder_name = input("wonder name: ")  # todo support random
        self.sender.send_logon(player_name=player_name, wonder_name=wonder_name)

    def _handle_message(self, msg: dict):
        print(msg['data'])

    def _recv(self):
        # receive data back from the server
        try:
            while True:
                msg = self.receiver.get_message()
                if msg is None:
                    break
                if msg[MSG_TYPE] == MESSAGE:  # todo handle error message from the server
                    self._handle_message(msg)
        except OSError:
            print("\nClosing recv thread")

    def _receive_input(self):
        message = input()
        if message == '':
            return
        if message[0] == '/':
            self.sender.send_command(message[1:])
        self.sender.send_message(message)
