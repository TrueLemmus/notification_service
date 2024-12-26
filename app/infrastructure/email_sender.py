import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from typing import Optional

from models.notification_event import NotificationEvent
from infrastructure.base_sender import Sender
from config import settings
from logger_helper import get_logger

logger = get_logger(__name__)


class EmailSender(Sender):
    """
    Класс для отправки email-уведомлений. Реализует интерфейс `Sender`.
    """

    def __init__(self) -> None:
        """
        Инициализирует класс EmailSender.

        Здесь можно было бы передать API ключ или настройки SMTP
        (например, через параметры конструктора).
        """
        pass

    @classmethod
    def send_email(cls, receiver: str, subject: Optional[str], message: str) -> None:
        """
        Отправляет письмо по указанному адресу посредством SMTP-сервера.

        :param receiver: Адрес электронной почты получателя.
        :type receiver: str
        :param subject: Тема письма (может быть None).
        :type subject: Optional[str]
        :param message: Текст письма.
        :type message: str
        :return: None
        :rtype: None
        """
        print(f"password = {settings.SMTP_PASSWORD} ")
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            email = MIMEMultipart()
            email["Subject"] = subject if subject else " "
            email["From"] = settings.SMTP_USER
            email["To"] = receiver

            server.sendmail(settings.SMTP_USER, receiver, message)

    @classmethod
    def get_user_email(cls, user_id: int) -> str:
        """
        Возвращает email-адрес пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Строка с адресом электронной почты пользователя.
        :rtype: str
        """
        # Логика получения email по user_id может быть расширена, например, взятием из БД
        return "example@gmail.com"

    async def send(self, notification: NotificationEvent) -> None:
        """
        Асинхронно отправляет email-уведомление, используя SMTP-сервер.

        :param notification: Объект NotificationEvent, содержащий информацию об уведомлении.
        :type notification: NotificationEvent
        :return: None
        :rtype: None
        """
        await asyncio.to_thread(
            self.send_email,
            self.get_user_email(notification.user_id),
            notification.subject,
            notification.message
        )
        logger.info(
            f"[EmailSender] Sending email to user_id={notification.user_id}, "
            f"subject={notification.subject}, body={notification.message}"
        )
