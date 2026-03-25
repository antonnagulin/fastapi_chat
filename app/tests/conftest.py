from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic import init_mediator
from logic.mediator import Mediator
from pytest import fixture


@fixture(scope='function')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()

@fixture(scope='function')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)

    return mediator