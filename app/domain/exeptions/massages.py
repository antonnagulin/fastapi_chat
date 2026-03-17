from dataclasses import dataclass

from .base import ApplicationExeption


@dataclass(eq=False)
class TitleToLongExeption(ApplicationExeption):
    text: str

    @property
    def massage(self):
        return f"Слишком длинный текст сообщения {self.text[:255]}..."


@dataclass(eq=False)
class EmptyTextExeption(ApplicationExeption):
    @property
    def massage(self):
        return "Текст не может быть пустым"
