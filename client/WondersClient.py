import socket
import threading

from messaging.MessageReceiver import MessageReceiver
from messaging.MessageSender import MessageSender
from messaging.messageTypes import MESSAGE
from messaging.messageUtil import MSG_TYPE


class WondersClient:
    HOST = "localhost"
    PORT = 9999

    def __init__(self):
        # create a TCP socket
        print("WondersClient created")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver = MessageReceiver(self.sock)
        self.sender = MessageSender(self.sock)

    def start(self, player_name=None, wonder_name=None):
        # connect to server
        print(f"WondersClient connecting to {self.HOST}:{self.PORT}")
        self.sock.connect((self.HOST, self.PORT))
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
                if msg[MSG_TYPE] == MESSAGE:
                    self._handle_message(msg)
        except OSError:
            print("\nClosing recv thread")

    def _receive_input(self):
        message = input()
        self.sender.send_message(message)
