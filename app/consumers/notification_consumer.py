import json
from typing import Any, Dict

from aio_pika import connect, Connection, Channel, Queue
from config import settings
from models.notification_event import NotificationEvent
from services.notification_service import NotificationService
from logger_helper import get_logger

logger = get_logger(__name__)


async def handle_incoming_message(raw_message: str) -> None:
    """
    Обрабатывает входящее сообщение, проверяет его валидность с помощью Pydantic 
    и вызывает соответствующую бизнес-логику для отправки уведомлений.

    :param raw_message: Строка в формате JSON, полученная из очереди.
    :type raw_message: str
    :return: None
    :rtype: None
    """
    # Разбор входящей строки в словарь
    data: Dict[str, Any] = json.loads(raw_message)

    # Валидация данных с помощью Pydantic
    try:
        event: NotificationEvent = NotificationEvent(**data)
    except Exception as e:
        # Если валидация не прошла - логируем ошибку или отправляем в DLQ
        logger.error(f"Ошибка валидации входящего сообщения: {e}")
        return

    # Если модель успешно создана, можно работать с данными
    logger.info("Валидация пройдена:")
    logger.info(f"Пользователь ID: {event.user_id}, сообщение: {event.message}, время: {event.created_at}")

    # Создаем NotificationService
    notification_service: NotificationService = NotificationService()

    # Обрабатываем уведомление
    await notification_service.handle_notification(event)


async def consume() -> None:
    """
    Подключается к очереди RabbitMQ, ожидает входящие сообщения 
    и передаёт их на обработку в handle_incoming_message.

    :return: None
    :rtype: None
    """
    # Устанавливаем соединение с RabbitMQ
    connection: Connection = await connect(settings.RABBITMQ_URL)

    # Создаём канал
    channel: Channel = await connection.channel()

    # Объявляем очередь
    queue: Queue = await channel.declare_queue("notifications", durable=True)
    logger.info(" [*] Waiting for messages...")

    # Считываем сообщения из очереди
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                raw: str = message.body.decode()
                logger.info("Received message:", raw)
                await handle_incoming_message(raw)
