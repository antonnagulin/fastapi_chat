
from dataclasses import dataclass

from logic.exeptions.base import LogicExeption


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicExeption):
    event_type: type

    @property
    def message(self):
        return f'Не удалось найти обработчик для события: {self.event_type}'
    
    
@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicExeption):
    command_type: type

    @property
    def massage(self):
        return f'Не удалось найти обработчик для команды: {self.command_type}'
    