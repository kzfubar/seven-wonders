import json
from asyncio import StreamWriter

from networking.messaging.messageTypes import COMMAND, ERROR, LOGON, MESSAGE
from networking.messaging.messageUtil import MSG_TYPE, SEP, UTF8


class MessageSender:
    def __init__(self, writer: StreamWriter):
        self.writer = writer

    def _send(self, msg: dict):
        self.writer.write(json.dumps(msg).encode(UTF8) + SEP)

    def send_message(self, message: str):
        msg = {MSG_TYPE: MESSAGE, "data": str(message)}
        self._send(msg)

    def send_command(self, message: str):
        msg = {MSG_TYPE: COMMAND, "data": str(message)}
        self._send(msg)

    def send_logon(self, player_name: str):
        msg = {MSG_TYPE: LOGON, "playerName": player_name}
        self._send(msg)

    def send_error(self, error_msg: str, error_code: int):
        msg = {MSG_TYPE: ERROR, "errorMsg": error_msg, "errorCode": error_code}
        self._send(msg)
