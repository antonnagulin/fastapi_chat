from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar


@dataclass(frozen=True)
class BaseCommand(ABC): 
    ...


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR")


class CommandHandler(ABC, Generic[CT, CR]):

    @abstractmethod
    async def handle(self, command: CT) -> CR: ...
