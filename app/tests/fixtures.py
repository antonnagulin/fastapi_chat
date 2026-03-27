from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.memory import MemoryChatRepository
from logic.init import _init_container
from punq import Container, Scope


def init_dummy_container() -> Container:
    container = _init_container()
    
    container.register(
        BaseChatRepository,
        MemoryChatRepository,
        scope=Scope.singleton
    )
    return container