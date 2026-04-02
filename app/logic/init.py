from functools import lru_cache

from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessagesRepository,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from settings.config import Config

from logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from logic.mediator import Mediator
from logic.queries.messages import GetChatDetailQuery, GetChatDetailQueryHandler


@lru_cache(1)
def init_cotainer():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def create_motor_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri, serverSelectionTimeoutMS=3000
        )

    container.register(
        AsyncIOMotorClient, factory=create_motor_client, scope=Scope.singleton
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongo_db_repository():
        return MongoDBChatRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    def init_messages_mongo_db_repository():
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )

    container.register(
        BaseChatsRepository,
        factory=init_chat_mongo_db_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        factory=init_messages_mongo_db_repository,
        scope=Scope.singleton,
    )

    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    container.register(GetChatDetailQueryHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        mediator.register_command(
            CreateMessageCommand, [container.resolve(CreateMessageCommandHandler)]
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )

        return mediator

    container.register(Mediator, init_mediator)

    return container
