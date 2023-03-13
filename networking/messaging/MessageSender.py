from abc import ABC, abstractmethod
from typing import Dict


class MessageSender(ABC):
    @abstractmethod
    def send_message(self, message: str):
        pass

    @abstractmethod
    def send_event(self, event_type: str, event_data: Dict):
        pass

    @abstractmethod
    def send_command(self, message: str):
        pass

    @abstractmethod
    def send_logon(self, player_name: str):
        pass

    @abstractmethod
    def send_error(self, error_msg: str, error_code: int):
        pass


class EmptySender(MessageSender):
    def send_message(self, message: str):
        pass

    def send_event(self, event_type: str, event_data: Dict):
        pass

    def send_command(self, message: str):
        pass

    def send_logon(self, player_name: str):
        pass

    def send_error(self, error_msg: str, error_code: int):
        pass


EMPTY_SENDER = EmptySender()
