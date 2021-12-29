import json
from typing import Optional

from messaging.messageUtil import SEP, UTF8, BUFFER_SIZE


class MessageReceiver:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = b''

    def get_message(self) -> Optional[dict]:
        while SEP not in self.buffer:
            data = self.sock.recv(BUFFER_SIZE)
            if not data:  # socket closed
                return None
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(SEP)
        return json.loads(line.decode(UTF8))
