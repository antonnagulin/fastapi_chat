from dataclasses import dataclass

from httpx import AsyncClient

from infra.integrations.notifications.clients.base import BaseNotificationClient
from infra.integrations.notifications.dots import Notification


@dataclass
class TelegramNotificationClient(BaseNotificationClient):
    bot_token: str
    chat_id: str
    http_client: AsyncClient

    async def _format_notification(self, notification: Notification) -> str:
        return f"{notification.title}\n{notification.text}"

    async def send(self, notification: Notification):
        text = await self._format_notification(notification)

        await self.http_client.post(
            url=f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            json={
                "chat_id": self.chat_id,
                "text": text,
            },
        )