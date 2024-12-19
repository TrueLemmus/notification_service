from infrastructure.base_sender import Sender
from models.notification_event import NotificationEvent


class SMSSender(Sender):
    def __init__(self):
        # Здесь можно было бы передать токен SMS провайдера
        pass

    async def send(self, notification: NotificationEvent):
        # Заглушка отправки SMS
        print(f"[SMSSender] Sending SMS to user_id={notification.user_id}, body={notification.message}")
