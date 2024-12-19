from models.notification_event import NotificationEvent
from infrastructure.base_sender import Sender


class EmailSender(Sender):
    def __init__(self):
        # Здесь можно было бы передать API ключ или настройки SMTP
        pass

    async def send(self, notification: NotificationEvent):
        # Заглушка отправки email
        print(f'[EmailSender] Sending email to user_id={notification.user_id},'
              f'subject={notification.subject}, body={notification.message}')
