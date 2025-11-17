from abc import ABC, abstractmethod
from typing import Any

from networking.messaging.messageTypes import COMMAND, ERROR, EVENT, LOGON, MESSAGE
from networking.messaging.messageUtil import DATA, EVENT_TYPE, MSG_TYPE


class MessageSender(ABC):
    @abstractmethod
    def _send(self, msg: Any) -> None:
        pass

    def send_message(self, message: str) -> None:
        msg = {MSG_TYPE: MESSAGE, DATA: str(message)}
        self._send(msg)

    def send_event(self, event_type: str, event_data: dict) -> None:
        msg = {MSG_TYPE: EVENT, EVENT_TYPE: event_type, DATA: event_data}
        self._send(msg)

    def send_command(self, message: str) -> None:
        msg = {MSG_TYPE: COMMAND, DATA: str(message)}
        self._send(msg)

    def send_logon(self, player_name: str) -> None:
        msg = {MSG_TYPE: LOGON, DATA: player_name}
        self._send(msg)

    def send_error(self, error_msg: str, error_code: int) -> None:
        msg = {MSG_TYPE: ERROR, DATA: error_msg, "errorCode": error_code}
        self._send(msg)


class EmptySender(MessageSender):
    def _send(self, msg: Any) -> None:
        pass


EMPTY_SENDER = EmptySender()
