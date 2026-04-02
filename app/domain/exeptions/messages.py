from dataclasses import dataclass

from .base import ApplicationException


@dataclass(eq=False)
class TitleToLongExeption(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Слишком длинный текст сообщения {self.text[:255]}..."


@dataclass(eq=False)
class EmptyTextExeption(ApplicationException):
    @property
    def message(self):
        return "Текст не может быть пустым"
