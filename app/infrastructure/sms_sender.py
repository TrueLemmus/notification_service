from infrastructure.base_sender import Sender
from models.notification_event import NotificationEvent
from logger_helper import get_logger

logger = get_logger(__name__)


class SMSSender(Sender):
    def __init__(self):
        # Здесь можно было бы передать токен SMS провайдера
        pass

    async def send(self, notification: NotificationEvent):
        # Заглушка отправки SMS
        logger.info(f"[SMSSender] Sending SMS to user_id={notification.user_id}, body={notification.message}")
