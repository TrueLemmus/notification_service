import json
from aio_pika import connect

from config import settings
from models.notification_event import NotificationEvent
from services.notification_service import NotificationService


async def handle_incoming_message(raw_message: str):
    # Разбор входящей строки в словарь
    data = json.loads(raw_message)

    # Валидация данных с помощью Pydantic
    try:
        event = NotificationEvent(**data)
    except Exception as e:
        # Если валидация не прошла - логируем ошибку или отправляем в DLQ
        print(f"Ошибка валидации входящего сообщения: {e}")
        return

    # Если модель успешно создана, можно работать с данными
    print("Валидация пройдена:")
    print(f"Пользователь ID: {event.user_id}, сообщение: {event.message}, время: {event.created_at}")

    # Далее - бизнес-логика обработки уведомления
    # Создаем NotificationService
    notification_service = NotificationService()

    # Обрабатываем уведомление
    await notification_service.handle_notification(event)


async def consume():
    connection = await connect(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)
    print(" [*] Waiting for messages...")
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                raw = message.body.decode()
                print("Received message:", raw)
                await handle_incoming_message(raw)
