from typing import Dict, Type

from infrastructure.email_sender import EmailSender
from infrastructure.sms_sender import SMSSender
from infrastructure.push_sender import PushSender
from infrastructure.base_sender import Sender
from models.notification_event import NotificationEvent
from logger_helper import get_logger

logger = get_logger(__name__)


class NotificationService:
    """
    Сервис, который обрабатывает уведомления и отправляет их через разные каналы (SMS, Email, Push).
    """

    def __init__(self) -> None:
        """
        Инициализирует сервис, создавая словарь `senders`, сопоставляющий тип уведомления
        (в виде строки) с классом, реализующим отправку уведомления.
        """
        self.senders: Dict[str, Type[Sender]] = {
            'sms': SMSSender,
            'email': EmailSender,
            'push': PushSender,
        }

    async def handle_notification(self, event: NotificationEvent) -> None:
        """
        Обрабатывает уведомление `event`, проходится по списку типов уведомлений и
        вызывает соответствующего отправителя для каждого типа.

        Если тип уведомления не найден в `self.senders`, выводится предупреждение в лог.

        :param event: Объект `NotificationEvent`, содержащий информацию об уведомлении
                      (тип, текст, идентификатор пользователя и т.д.).
        :type event: NotificationEvent
        :return: None
        :rtype: None
        """
        for notification_type in event.notification_type:
            sender_class = self.senders.get(notification_type)
            # Проверяем, что класс существует и у него есть метод send
            if sender_class and callable(sender_class.send):
                try:
                    await sender_class().send(event)
                    logger.info(
                        f"Уведомление '{notification_type}' отправлено пользователю {event.user_id}."
                    )
                except Exception as e:
                    logger.error(
                        f"Ошибка при отправке '{notification_type}' пользователю {event.user_id}: {e}"
                    )
            else:
                logger.warning(f"Неизвестный тип уведомления: {notification_type}")
