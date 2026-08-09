from celery import Celery

from app.settings import settings

celery_app = Celery(
    "celery_lab",
    broker=settings.broker_url,
    backend=settings.result_backend,
    include=["app.tasks"],
)
celery_app.conf.update(
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
    broker_transport_options={"visibility_timeout": settings.visibility_timeout},
    result_accept_content=["json"],
    result_expires=3600,
    task_acks_late=settings.celery_acks_late,
    task_default_queue="default",
    task_reject_on_worker_lost=settings.celery_reject_on_worker_lost,
    task_serializer="json",
    task_soft_time_limit=settings.soft_time_limit,
    task_time_limit=settings.time_limit,
    task_track_started=True,
    timezone="UTC",
    worker_prefetch_multiplier=settings.prefetch_multiplier,
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
