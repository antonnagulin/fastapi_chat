from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationExeption(Exception):

    @property
    def massage(self):
        return "Произошла ошибка приложения"
