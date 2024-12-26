import os
import logging
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()


class Settings:
    RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost/')
    SMTP_USER = os.getenv('SMTP_USER', 'email@gmail.com')
    SMTP_HOST = os.getenv('SMPT_HOST', 'smtp.gmail.com')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'password')
    SMTP_PORT = os.getenv('SMTP_PORT', 587)
    SMS_API_KEY = os.getenv('SMS_API_KEY', 'your_sms_key')
    PUSH_API_KEY = os.getenv('PUSH_API_KEY', 'your_push_key')
    TIME_ZONE = ZoneInfo('Europe/Moscow')
    LOG_LEVEL = logging.DEBUG


settings = Settings()
