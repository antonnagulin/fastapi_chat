from functools import lru_cache

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from application.api.common.websockets.managers import (
    BaseConnectionManager,
    ConnectionManager,
)
from domain.events.messages import NewChatCreatedEvent, NewMessageReceivedEvent
from infra.message_brokers.base import BaseMessageBroker
from infra.message_brokers.kafka import KafkaMessageBroker
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
from logic.events.messages import (
    NewChatCreatedEventHandler,
    NewMessageReceivedEventHandler,
)
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)


@lru_cache(1)
def init_container() -> Container:
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
            mongo_db_collection_name=config.mongodb_messages_collection,
        )
        
    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_url,
                group_id='chat',
                metadata_max_age_ms=30000,
            )
        )

    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton
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
    container.register(GetMessagesQueryHandler)
    
    container.register(
            BaseConnectionManager,
            instance=ConnectionManager(),
            scope=Scope.singleton
        )
        
    def init_mediator():
        mediator = Mediator()
        
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessagesRepository),
            chats_repository=container.resolve(BaseChatsRepository)
        )
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker)
        )
        new_message_received_handler = NewMessageReceivedEventHandler(
            broker_topic=config.new_message_received_topic,
            message_broker=container.resolve(BaseMessageBroker)
        )
        
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler]
        )
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        mediator.register_event(
            NewChatCreatedEvent, 
            [new_chat_created_event_handler]
        )
        mediator.register_event(
            NewMessageReceivedEvent, 
            [new_message_received_handler]
        )
 
        return mediator

    container.register(Mediator, init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
