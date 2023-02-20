import json
from asyncio import StreamReader
from typing import Optional

from networking.messaging.messageUtil import SEP, UTF8, BUFFER_SIZE


class MessageReceiver:
    def __init__(self, reader: StreamReader):
        self.reader = reader
        self.buffer = b""

    def is_empty(self):
        return self.reader.at_eof()

    async def get_message(self) -> Optional[dict]:
        while SEP not in self.buffer:
            data = await self.reader.read(BUFFER_SIZE)
            if not data:  # socket closed
                return None
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(SEP)
        return json.loads(line.decode(UTF8))
