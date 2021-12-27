import socket


class EchoClient:
    HOST = "localhost"
    PORT = 9999

    def __init__(self):
        # create a TCP socket
        print("EchoClient created")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # connect to server
        print(f"EchoClient connecting to {self.HOST}:{self.PORT}")
        self.sock.connect((self.HOST, self.PORT))
        try:
            while True:
                self._receive_input()
        except KeyboardInterrupt:
            self._close()

    def _close(self):
        # shut down
        print("\nEchoClient shutting down!")
        self.sock.close()

    def _receive_input(self):
        data = input("input: ")
        self.sock.sendall(bytes(data, encoding='utf8'))

        # receive data back from the server
        received = str(self.sock.recv(1024))
        print(f"received: {received}")


if __name__ == "__main__":
    print("Launching EchoClient...")
    EchoClient().start()




