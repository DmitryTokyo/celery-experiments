# Change these values before an experiment, then restart the workers.
BROKER = "redis"
RESULT_BACKEND = "redis://redis:6379/2"

CELERY_ACKS_LATE = True
CELERY_REJECT_ON_WORKER_LOST = False
VISIBILITY_TIMEOUT = 30
PREFETCH_MULTIPLIER = 1
SOFT_TIME_LIMIT = None
TIME_LIMIT = None

WRITE_ONCE_REDIS_URL = "redis://redis:6379/1"
WRITE_ONCE_POST_SETNX_DELAY = 0

BROKER_URLS = {
    "redis": "redis://redis:6379/0",
    "rabbit": "amqp://guest:guest@rabbitmq:5672//",
}

if BROKER not in BROKER_URLS:
    raise ValueError(f"BROKER must be one of {', '.join(BROKER_URLS)}")

BROKER_URL = BROKER_URLS[BROKER]
