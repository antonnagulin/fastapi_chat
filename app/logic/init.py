from functools import lru_cache

from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.mongo import MongoDBChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from settings.config import Config


@lru_cache(1)
def init_cotainer():
    return _init_container()


def _init_container()-> Container:
    container = Container()
    
    container.register(CreateChatCommandHandler)
    container.register(Config, instance=Config(), scope=Scope.singleton)


    def init_mediator():
        mediator = Mediator()
        
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )
        return mediator

    def init_chat_mongo_db_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000
        )
        return MongoDBChatRepository(
            mongo_db_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongodb_chat_collection,
        )
        
    
    container.register(
        BaseChatRepository,
        factory=init_chat_mongo_db_repository,
        scope=Scope.singleton
    )
    container.register(Mediator, init_mediator)
    
    return container