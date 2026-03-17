from dataclasses import dataclass

from ..exeptions.massages import EmptyTextExeption, TitleToLongExeption
from .base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextExeption()

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextExeption()

        if len(self.value) > 255:
            raise TitleToLongExeption(self.value)

    def as_generic_type(self):
        return str(self.value)
