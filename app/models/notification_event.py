from pydantic import BaseModel, Field
from typing import Optional, List  # Добавлен импорт List
from datetime import datetime

from config import settings


class NotificationEvent(BaseModel):
    user_id: int = Field(
        ...,
        description="ID пользователя, которому отправляется уведомление"
    )
    device_token: Optional[str] = Field(
        default_factory=lambda: None,
        description="Токен устройства"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Текст уведомления, не может быть пустым"
    )
    subject: Optional[str] = Field(
        default_factory=lambda: None,
        description="Тема события"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(settings.TIME_ZONE),
        description="Время создания события"
    )
    notification_type: List[str] = Field(
        ...,
        description="Тип события (список типов)"
    )
