import socketserver

from server import EchoHandler


class EchoServer(socketserver.ThreadingTCPServer):
    HOST = "localhost"
    PORT = 9999
    name = "oyo"

    def __init__(self):
        super().__init__((self.HOST, self.PORT), EchoHandler.EchoHandler)
        print("EchoServer created")

    def get_tag(self) -> bytes:
        return bytes(f"{self.name} says: ", encoding='utf8')

    def start(self):
        try:
            print("EchoServer Started!")
            self.serve_forever()
        except KeyboardInterrupt:
            print("EchoServer Closed!")


if __name__ == "__main__":
    print("Starting EchoServer")
    EchoServer().start()