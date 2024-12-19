from abc import ABC, abstractmethod
from models.notification_event import NotificationEvent


class Sender(ABC):
    @abstractmethod
    async def send(self, notification: NotificationEvent):
        pass
