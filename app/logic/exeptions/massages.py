from dataclasses import dataclass

from logic.exeptions.base import LogicExeption


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicExeption):
    title: str

    @property
    def massage(self):
        return f'Чат с таким низванием "{self.title}" уже существует.'
    
    
    