from dataclasses import dataclass, field

from domain.entities.messages import Chat

from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository


@dataclass
class MemoryChatRepository(BaseChatsRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat
                    for chat in self._saved_chats
                    if chat.title.as_generic_type() == title  # noqa: E501
                )
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            chat = next(chat for chat in self._saved_chats if chat.oid == oid)
        except StopIteration:
            return None

        return chat



# @dataclass
# class MemoryMessagesRepository(BaseMessagesRepository):

#     async def add_message(self, chat_oid: str, message: Message) -> None:
#         ...


#     async def get_messages(
#         self,
#         chat_oid: str,
#         filters: GetMessagesFilters
#     ) -> tuple[Iterable[Message], int]:
#         ...