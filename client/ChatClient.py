import socket
import threading


class ChatClient:
    HOST = "localhost"
    PORT = 9998

    def __init__(self):
        # create a TCP socket
        print("ChatClient created")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.started = True

    def start(self):
        # connect to server
        print(f"ChatClient connecting to {self.HOST}:{self.PORT}")
        self.sock.connect((self.HOST, self.PORT))
        threading.Thread(target=self._recv).start()

        try:
            print("begin typing: ")
            while True:
                self._receive_input()
        except KeyboardInterrupt:
            self.sock.shutdown(socket.SHUT_RDWR)
            self._close()

    def _close(self):
        # shut down
        print("\nChatClient shutting down!")
        self.sock.close()

    def _recv(self):
        # receive data back from the server
        try:
            while True:
                received = str(self.sock.recv(1024))
                print(f"{received}")
        except OSError:
            print("\nClosing recv thread")

    def _receive_input(self):
        data = input()
        self.sock.sendall(bytes(data, encoding='utf8'))


if __name__ == "__main__":
    print("Launching ChatClient...")
    ChatClient().start()
