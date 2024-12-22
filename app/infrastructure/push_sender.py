import asyncio

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from models.notification_event import NotificationEvent
from infrastructure.base_sender import Sender
from logger_helper import get_logger

logger = get_logger(__name__)


class PushSender(Sender):
    def __init__(self, credential_path: str = "serviceAccountKey.json"):
        # Загружаем учетные данные и инициализируем приложение Firebase
        self.cred = credentials.Certificate(credential_path)

        # initialize_app нужно вызвать только один раз за все время жизни приложения.
        # Если у вас уже есть где-то вызов initialize_app, повторно делать это не нужно.
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(self.cred)

    def send_push(self, notification: NotificationEvent):
        """
        Отправка push-уведомления с помощью Firebase Admin.
        Предполагается, что NotificationEvent содержит:
          - notification.user_id (идентификатор пользователя, можно не использовать)
          - notification.message (текст уведомления)
          - notification.device_token (обязательный, токен FCM/Device)
        """

        # Создаём сообщение для отправки через FCM
        message = messaging.Message(
            token=notification.device_token,  # Токен, полученный в клиентском приложении
            notification=messaging.Notification(
                title="Уведомление",
                body=notification.message,
            ),
            # Дополнительно можно передавать data-поле, если нужно
            # data={
            #     "some_key": "some_value"
            # }
        )

        # Отправляем сообщение
        try:
            response = messaging.send(message)
            logger.info(f"[PushSender] Push notification отправлено успешно. FCM response: {response}")
        except Exception as e:
            logger.error(f"[PushSender] Ошибка при отправке push-уведомления: {e}")

    async def send(self, notification: NotificationEvent) -> None:
        await asyncio.to_thread(self.send_push, notification)
