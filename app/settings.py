import sys
from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        env_parse_none_str="none",
        extra="ignore",
    )

    broker: Literal["redis", "rabbit"]
    result_backend: str

    celery_acks_late: bool
    celery_reject_on_worker_lost: bool
    visibility_timeout: int
    prefetch_multiplier: int
    soft_time_limit: int | None
    time_limit: int | None

    write_once_redis_url: str
    write_once_post_setnx_delay: int

    @property
    def broker_url(self) -> str:
        return {
            "redis": "redis://redis:6379/0",
            "rabbit": "amqp://guest:guest@rabbitmq:5672//",
        }[self.broker]


settings = Settings()

logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    level="DEBUG",
    format=(
        "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    ),
)
