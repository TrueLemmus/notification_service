from typing import Dict
import logging

from infrastructure.email_sender import EmailSender
from infrastructure.sms_sender import SMSSender
from infrastructure.push_sender import PushSender
from infrastructure.base_sender import Sender
from models.notification_event import NotificationEvent


class NotificationService:
    def __init__(self):

        self.senders: Dict[str, Sender] = {
            'sms': SMSSender,
            'email': EmailSender,
            'push': PushSender,
        }

    async def handle_notification(self, event: NotificationEvent):
        for notification_type in event.notification_type:
            sender = self.senders.get(notification_type)
            if sender and callable(sender.send):
                try:
                    await sender().send(event)
                    logging.info(f"Уведомление '{notification_type}' отправлено пользователю {event.user_id}.")
                except Exception as e:
                    logging.error(f"Ошибка при отправке '{notification_type}' пользователю {event.user_id}: {e}")
            else:
                logging.warning(f"Неизвестный тип уведомления: {notification_type}")
