from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.mediator.base import Mediator
from punq import Container
from pytest import fixture

from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)


@fixture()
def message_repository(container: Container) -> BaseMessagesRepository:
    return container.resolve(BaseMessagesRepository)
