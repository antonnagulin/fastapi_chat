from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewMassageReceivedEvent(BaseEvent):
    massage_text: str
    massage_oid: str
    chat_oid: str


@dataclass
class NewChatCreated(BaseEvent):
    chat_oid: str
    chat_title: str