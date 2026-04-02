from datetime import datetime

from domain.entities.messages import Chat, Message
from pydantic import BaseModel


class CreateChatInSchema(BaseModel):
    title: str


class CreateChatOutSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatOutSchema":
        return CreateChatOutSchema(oid=chat.oid, title=chat.title.as_generic_type())


class CreateMessageInSchema(BaseModel):
    text: str

class CreateMessageOutSchema(BaseModel):
    text: str
    oid: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageOutSchema':
        return cls(
            text=message.text.as_generic_type(),
            oid=message.oid,
            created_at=message.created_at,
        )
    
        