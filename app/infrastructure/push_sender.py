from models.notification_event import NotificationEvent
from infrastructure.base_sender import Sender


class PushSender(Sender):
    def __init__(self):
        # Здесь можно было бы передать API ключ для push-сервиса
        pass

    async def send(self, notification: NotificationEvent):
        # Заглушка отправки push-уведомления
        print(f"[PushSender] Sending push notification to user_id={notification.user_id}, body={notification.message}")
