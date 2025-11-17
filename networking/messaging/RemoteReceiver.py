import json
from asyncio import StreamReader

from networking.messaging.MessageReceiver import MessageReceiver
from networking.messaging.messageUtil import BUFFER_SIZE, SEP, UTF8


class RemoteReceiver(MessageReceiver):
    def __init__(self, reader: StreamReader) -> None:
        self.reader = reader
        self.buffer = b""

    def is_empty(self) -> bool:
        return self.reader.at_eof()

    async def get_message(self) -> dict[str, str]:
        while SEP not in self.buffer:
            data = await self.reader.read(BUFFER_SIZE)
            if not data:  # socket closed
                raise ConnectionResetError
            self.buffer += data
        line, _sep, self.buffer = self.buffer.partition(SEP)
        return json.loads(line.decode(UTF8))
