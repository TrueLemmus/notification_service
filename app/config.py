import os
import logging
from zoneinfo import ZoneInfo


class Settings:
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    EMAIL_API_KEY = os.getenv("EMAIL_API_KEY", "your_email_key")
    SMS_API_KEY = os.getenv("SMS_API_KEY", "your_sms_key")
    PUSH_API_KEY = os.getenv("PUSH_API_KEY", "your_push_key")
    TIME_ZONE = ZoneInfo("Europe/Moscow")
    LOG_LEVEL = logging.DEBUG


settings = Settings()
