from abc import ABC, abstractmethod
from typing import Dict

from networking.messaging.messageTypes import COMMAND, ERROR, LOGON, MESSAGE, EVENT
from networking.messaging.messageUtil import EVENT_TYPE, DATA
from networking.messaging.messageUtil import MSG_TYPE


class MessageSender(ABC):
    @abstractmethod
    def _send(self, msg):
        pass

    def send_message(self, message: str):
        msg = {MSG_TYPE: MESSAGE, DATA: str(message)}
        self._send(msg)

    def send_event(self, event_type: str, event_data: Dict):
        msg = {MSG_TYPE: EVENT, EVENT_TYPE: event_type, DATA: event_data}
        self._send(msg)

    def send_command(self, message: str):
        msg = {MSG_TYPE: COMMAND, DATA: str(message)}
        self._send(msg)

    def send_logon(self, player_name: str):
        msg = {MSG_TYPE: LOGON, DATA: player_name}
        self._send(msg)

    def send_error(self, error_msg: str, error_code: int):
        msg = {MSG_TYPE: ERROR, DATA: error_msg, "errorCode": error_code}
        self._send(msg)


class EmptySender(MessageSender):
    def _send(self, msg):
        pass


EMPTY_SENDER = EmptySender()
