from dataclasses import dataclass
from typing import Generic

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository

from logic.exeptions.messages import ChatNotFoundExeption
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QT, QR]):
    chats_repository: BaseChatsRepository
    message_repository: BaseMessagesRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundExeption(chat_oid=query.chat_oid)

        return chat
