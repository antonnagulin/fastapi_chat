from dataclasses import dataclass
from typing import ClassVar

from domain.events.messages import (
    ChatDeletedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from infra.integrations.notifications.clients.base import BaseNotificationClient
from infra.integrations.notifications.dots import Notification
from infra.message_brokers.converters import convert_event_to_broker_message

from logic.events.base import EventHandler, IntegrationEvent


@dataclass
class NewChatCreatedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = 'New Chat Created From Broker Received'

    chat_title: str
    chat_oid: str

@dataclass
class NewMessageReceivedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = 'New Message From Broker Received'

    message_text: str
    message_oid: str
    chat_oid: str
    
    
@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent)-> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )
        
    
@dataclass
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )
        
@dataclass
class NewMessageReceivedFromBrokerEventHandler(
    EventHandler[NewMessageReceivedFromBrokerEvent, None]
):
    async def handle(self, event: NewMessageReceivedFromBrokerEvent)-> None:
        await self.connection_manager.send_all(
            key=event.chat_oid,
            bytes_=convert_event_to_broker_message(event=event)
        )
        
@dataclass
class NewChatCreatedFromBrokerEventHandler(
    EventHandler[NewChatCreatedFromBrokerEvent, None]
):
    async def handle(self, event: NewChatCreatedFromBrokerEvent)-> None:
        await self.connection_manager.send_all(
            key="profile",
            bytes_=convert_event_to_broker_message(event=event)
        )


@dataclass(kw_only=True)
class SendTelegramOnNewChatCreatedHandler(
    EventHandler[NewChatCreatedFromBrokerEvent, None]
):
    notification_client: BaseNotificationClient

    async def handle(self, event: NewChatCreatedFromBrokerEvent) -> None:
        await self.notification_client.send(
            Notification(
                title="🆕 Новый чат",
                text=f"Название: {event.chat_title}\nID: {event.chat_oid}",
            )
        )
        
@dataclass(kw_only=True)
class SendTelegramOnNewMessageHandler(
    EventHandler[NewMessageReceivedFromBrokerEvent, None]
):
    notification_client: BaseNotificationClient

    async def handle(self, event: NewMessageReceivedFromBrokerEvent) -> None:
        await self.notification_client.send(
            Notification(
                title="💬 Новое сообщение",
                text=f"{event.message_text}\n(chat: {event.chat_oid})",
            )
        )
        
@dataclass
class ChatDeletedEventHandler(EventHandler[ChatDeletedEvent, None]):
    async def handle(self, event: ChatDeletedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )

        await self.connection_manager.disconnect_all(event.chat_oid)