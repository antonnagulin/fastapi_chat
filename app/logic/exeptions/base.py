from dataclasses import dataclass

from domain.exeptions.base import ApplicationException


@dataclass(eq=False)
class LogicExeption(ApplicationException):

    @property
    def message(self):
        return "В обработке запроса возникла ошибка"
