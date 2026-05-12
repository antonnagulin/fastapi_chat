from functools import lru_cache

from aiojobs import Scheduler
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from domain.events.messages import (
    ChatDeletedEvent,
    ListenerAddedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from httpx import AsyncClient
from infra.integrations.notifications.clients.base import BaseNotificationClient
from infra.integrations.notifications.clients.telegram import TelegramNotificationClient
from infra.message_brokers.base import BaseMessageBroker
from infra.message_brokers.kafka import KafkaMessageBroker
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessagesRepository,
)
from infra.websockets.managers import (
    BaseConnectionManager,
    ConnectionManager,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from settings.config import Config

from logic.commands.messages import (
    AddTelegramListenerCommand,
    AddTelegramListenerCommandHandler,
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
    DeleteChatCommand,
    DeleteChatCommandHandler,
)
from logic.events.messages import (
    ChatDeletedEventHandler,
    ListenerAddedEventHandler,
    NewChatCreatedEventHandler,
    NewChatCreatedFromBrokerEvent,
    NewChatCreatedFromBrokerEventHandler,
    NewMessageReceivedEventHandler,
    NewMessageReceivedFromBrokerEvent,
    NewMessageReceivedFromBrokerEventHandler,
    SendTelegramOnNewChatCreatedHandler,
    SendTelegramOnNewMessageHandler,
)
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.messages import (
    GetAllChatsQuery,
    GetAllChatsQueryHandler,
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

    def create_notification_client() -> BaseNotificationClient:
        return TelegramNotificationClient(
            bot_token=config.telegram_bot_token,
            chat_id=config.chat_id,
            http_client=AsyncClient(),
        )
    
    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton
    )
    
    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton
    )

    container.register(
        BaseNotificationClient,
        factory=create_notification_client,
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

    container.register(DeleteChatCommandHandler)
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    container.register(AddTelegramListenerCommandHandler)
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)
    container.register(GetAllChatsQueryHandler)
    

        
    def init_mediator():
        mediator = Mediator()
        #commands
        
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessagesRepository),
            chats_repository=container.resolve(BaseChatsRepository)
        )
        delete_chat_handler = DeleteChatCommandHandler(
            _mediator=mediator,
            chats_repository=container.resolve(BaseChatsRepository)
        )
        add_telegram_listener_command = AddTelegramListenerCommandHandler(
            _mediator=mediator,
            chats_repository = container.resolve(BaseChatsRepository)
        )
        
        #events
        listener_added_event_handler = ListenerAddedEventHandler(
            broker_topic=config.new_listener_added_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager)
        )
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager)
        )
        new_message_received_event_handler = NewMessageReceivedEventHandler(
            broker_topic=config.new_message_received_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager)
        )
        chat_deleted_event_handler = ChatDeletedEventHandler(
            broker_topic=config.chat_deleted_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager)
        )
        new_message_received_from_broker_event_handler = NewMessageReceivedFromBrokerEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
            broker_topic=config.new_message_received_topic,
        )
        new_chat_created_from_broker_event_handler = NewChatCreatedFromBrokerEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
            broker_topic=config.new_chats_event_topic,
        )
        new_chat_telegram_handler = SendTelegramOnNewChatCreatedHandler(
            notification_client=container.resolve(BaseNotificationClient)
        )
        new_message_telegram_handler = SendTelegramOnNewMessageHandler(
            notification_client=container.resolve(BaseNotificationClient)
        )
        #commands
        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            DeleteChatCommand,
            [delete_chat_handler]
        )
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler]
        )
        mediator.register_command(
            AddTelegramListenerCommand,
            [add_telegram_listener_command]
        )
        
        #queryes
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )
        mediator.register_query(
            GetAllChatsQuery,
            container.resolve(GetAllChatsQueryHandler)
        )
        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )
        
        #events
        mediator.register_event(
            ListenerAddedEvent,
            [listener_added_event_handler]
        )
        mediator.register_event(
            NewChatCreatedEvent, 
            [new_chat_created_event_handler]
        )
        mediator.register_event(
            NewMessageReceivedEvent, 
            [new_message_received_event_handler]
        )
        mediator.register_event(
            ChatDeletedEvent,
            [chat_deleted_event_handler]
        )
        mediator.register_event(
            NewMessageReceivedFromBrokerEvent,
            [
                new_message_received_from_broker_event_handler,
                new_message_telegram_handler
            ],
        )
        mediator.register_event(
            NewChatCreatedFromBrokerEvent,
            [
                new_chat_created_from_broker_event_handler,
                new_chat_telegram_handler
            ],
        )
 
        return mediator

    container.register(Mediator, init_mediator)
    container.register(EventMediator, factory=init_mediator)
    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container
