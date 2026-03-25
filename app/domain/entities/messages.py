from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.events.massages import NewChatCreated, NewMassageReceivedEvent
from domain.values.massages import Text, Title


@dataclass(eq=False)
class Massage(BaseEntity):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    text: Text


@dataclass(eq=False)
class Chat(BaseEntity):
    massage: set[Massage] = field(
        default_factory=set,
        kw_only=True,
    )
    title: Title
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def add_massage(self, massage: Massage):
        self.massage.add(massage)
        self.register_event(
            NewMassageReceivedEvent(
                massage_text=massage.text.as_generic_type(),
                massage_oid=massage.oid,
                chat_oid=self.oid,
            )
        )
        
    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreated(
            chat_title=new_chat.title.as_generic_type(),
            chat_oid=new_chat.oid
        ))
        return new_chat
    