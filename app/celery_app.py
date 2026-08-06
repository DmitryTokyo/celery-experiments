import sys

from celery import Celery
from loguru import logger

from app import settings

logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    level="DEBUG",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

celery_app = Celery(
    "celery_lab",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
    include=["app.tasks"],
)
celery_app.conf.update(
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
    broker_transport_options={"visibility_timeout": settings.VISIBILITY_TIMEOUT},
    result_accept_content=["json"],
    result_expires=3600,
    task_acks_late=settings.CELERY_ACKS_LATE,
    task_default_queue="default",
    task_reject_on_worker_lost=settings.CELERY_REJECT_ON_WORKER_LOST,
    task_serializer="json",
    task_soft_time_limit=settings.SOFT_TIME_LIMIT,
    task_time_limit=settings.TIME_LIMIT,
    task_track_started=True,
    timezone="UTC",
    worker_prefetch_multiplier=settings.PREFETCH_MULTIPLIER,
    worker_send_task_events=True,
    task_send_sent_event=True,
    beat_schedule={
        "experiment-chain-step": {
            "task": "app.tasks.chain_step",
            "schedule": 10.0,
            "args": (1,),
            "options": {"queue": "default"},
        }
    },
)
