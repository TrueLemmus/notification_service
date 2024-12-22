from abc import ABC, abstractmethod

from models.notification_event import NotificationEvent


class Sender(ABC):
    """
    Абстрактный класс, который задаёт интерфейс для отправки уведомлений.
    """

    @abstractmethod
    async def send(self, notification: NotificationEvent) -> None:
        """
        Отправляет уведомление на основе переданного объекта NotificationEvent.

        :param notification: Уведомление, содержащее данные о сообщении, пользователе и т.д.
        :type notification: NotificationEvent
        :return: None
        :rtype: None
        """
        pass
