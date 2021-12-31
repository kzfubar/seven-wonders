import json

from networking.messaging.messageTypes import *
from networking.messaging.messageUtil import *


class MessageSender:
    def __init__(self, sock):
        self.sock = sock

    def _send(self, msg: dict):
        self.sock.sendall(json.dumps(msg).encode(UTF8) + SEP)

    def send_message(self, message: str):
        msg = {
            MSG_TYPE: MESSAGE,
            "data": str(message)
        }
        self._send(msg)

    def send_command(self, message: str):
        msg = {
            MSG_TYPE: COMMAND,
            "data": str(message)
        }
        self._send(msg)

    def send_logon(self, player_name: str, wonder_name: str):
        msg = {
            MSG_TYPE: LOGON,
            "playerName": player_name,
            "wonderName": wonder_name
        }
        self._send(msg)

    def send_error(self, error_msg: str, error_code: int):
        msg = {
            MSG_TYPE: ERROR,
            "errorMsg": error_msg,
            "errorCode": error_code,
        }
        self._send(msg)
