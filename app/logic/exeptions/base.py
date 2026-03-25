

from dataclasses import dataclass

from domain.exeptions.base import ApplicationExeption


@dataclass(eq=False)
class LogicExeption(ApplicationExeption):
    
    @property
    def massage(self):
        return 'В обработке запроса возникла ошибка'
    
    