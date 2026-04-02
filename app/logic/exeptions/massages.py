from dataclasses import dataclass

from logic.exeptions.base import LogicExeption


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicExeption):
    title: str

    @property
    def massage(self):
        return f'Чат с таким низванием "{self.title}" уже существует.'

@dataclass(eq=False)
class ChatNotFoundExeption(LogicExeption):
    chat_oid: str

    @property
    def message(self):
        return f'Чат c OID {self.chat_oid} не найден'