import asyncio

import firebase_admin
from firebase_admin import credentials, messaging

from models.notification_event import NotificationEvent
from infrastructure.base_sender import Sender
from logger_helper import get_logger

logger = get_logger(__name__)


class PushSender(Sender):
    """
    Класс для отправки Push-уведомлений с помощью Firebase Admin SDK.
    """

    def __init__(self, credential_path: str = "serviceAccountKey.json") -> None:
        """
        Инициализирует Firebase-приложение, используя сервисный аккаунт 
        из указанного файла.

        :param credential_path: Путь к файлу с сервисным аккаунтом Firebase.
        :type credential_path: str
        """
        # Загружаем учетные данные и инициализируем приложение Firebase.
        self.cred = credentials.Certificate(credential_path)

        # initialize_app нужно вызвать только один раз за все время жизни приложения.
        # Если у вас уже есть где-то вызов initialize_app, повторно делать это не нужно.
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(self.cred)

    def send_push(self, notification: NotificationEvent) -> None:
        """
        Отправляет push-уведомление с помощью Firebase Admin SDK.

        Предполагается, что `notification` содержит:
          - notification.user_id (идентификатор пользователя, можно не использовать)
          - notification.message (текст уведомления)
          - notification.device_token (обязательный, токен FCM/Device)

        :param notification: Объект NotificationEvent, содержащий данные уведомления.
        :type notification: NotificationEvent
        :return: None
        :rtype: None
        """
        # Формируем сообщение для отправки через FCM
        message = messaging.Message(
            token=notification.device_token,  # Токен устройства из клиентского приложения
            notification=messaging.Notification(
                title="Уведомление",
                body=notification.message,
            ),
            # Дополнительно можно передавать data-поле, если нужно
            # data={"some_key": "some_value"}
        )

        # Отправляем сообщение
        try:
            response = messaging.send(message)
            logger.info(f"[PushSender] Push notification отправлено успешно. FCM response: {response}")
        except Exception as e:
            logger.error(f"[PushSender] Ошибка при отправке push-уведомления: {e}")

    async def send(self, notification: NotificationEvent) -> None:
        """
        Асинхронно отправляет push-уведомление, используя метод send_push в отдельном потоке.

        :param notification: Объект NotificationEvent, содержащий данные уведомления.
        :type notification: NotificationEvent
        :return: None
        :rtype: None
        """
        await asyncio.to_thread(self.send_push, notification)
