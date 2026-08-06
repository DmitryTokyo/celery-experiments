import json
import os
import random
import socket
import time
from typing import Any

from billiard.exceptions import SoftTimeLimitExceeded
from celery import Task
from loguru import logger
from redis import Redis

from app import settings
from app.celery_app import celery_app


class RetryableExperimentError(RuntimeError):
    pass


def _exp_log(task: Task, task_id: str, event: str, **fields: Any) -> None:
    payload = {
        "delivery_info": dict(task.request.delivery_info or {}),
        "event": event,
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        "retries": task.request.retries,
        "task_id": task_id,
        **fields,
    }
    logger.debug(f"[EXP] {json.dumps(payload, sort_keys=True, separators=(',', ':'))}")


@celery_app.task(bind=True)
def sleep_task(self: Task, task_id: str, seconds: float) -> dict[str, Any]:
    _exp_log(self, task_id, "before_sleep", seconds=seconds)
    time.sleep(seconds)
    _exp_log(self, task_id, "after_sleep", seconds=seconds)
    return {"task_id": task_id, "slept": seconds}


@celery_app.task(
    bind=True,
    autoretry_for=(RetryableExperimentError,),
    max_retries=None,
    retry_backoff=True,
    retry_jitter=True,
)
def fail_task(
    self: Task,
    task_id: str,
    fail_probability: float,
    max_retries: int,
) -> dict[str, Any]:
    if not 0 <= fail_probability <= 1:
        raise ValueError("fail_probability must be between 0 and 1")
    if max_retries < 0:
        raise ValueError("max_retries must be non-negative")

    _exp_log(
        self,
        task_id,
        "attempt",
        fail_probability=fail_probability,
        max_retries=max_retries,
    )
    if random.random() < fail_probability:
        if self.request.retries >= max_retries:
            _exp_log(self, task_id, "retries_exhausted", max_retries=max_retries)
            raise RuntimeError(f"retries exhausted for {task_id}")
        _exp_log(self, task_id, "retry_scheduled", max_retries=max_retries)
        raise RetryableExperimentError(task_id)

    _exp_log(self, task_id, "success")
    return {"task_id": task_id, "retries": self.request.retries}


@celery_app.task(bind=True)
def burn_cpu(self: Task, task_id: str, seconds: float) -> dict[str, Any]:
    _exp_log(self, task_id, "before_burn", seconds=seconds)
    deadline = time.monotonic() + seconds
    iterations = 0
    accumulator = 1
    while time.monotonic() < deadline:
        accumulator = (accumulator * 1_664_525 + 1_013_904_223) & 0xFFFFFFFF
        iterations += 1
    _exp_log(
        self,
        task_id,
        "after_burn",
        accumulator=accumulator,
        iterations=iterations,
        seconds=seconds,
    )
    return {"iterations": iterations, "task_id": task_id}


@celery_app.task(bind=True)
def write_once(self: Task, key: str) -> dict[str, Any]:
    redis_client: Redis = Redis.from_url(settings.WRITE_ONCE_REDIS_URL, decode_responses=True)
    redis_key = f"celery-lab:write-once:{key}"
    created = bool(redis_client.set(redis_key, "1", nx=True))
    _exp_log(self, key, "setnx", created=created, key=redis_key)

    delay = settings.WRITE_ONCE_POST_SETNX_DELAY
    if delay > 0:
        time.sleep(delay)
    _exp_log(self, key, "write_once_complete", created=created, key=redis_key)
    return {"created": created, "key": key}


@celery_app.task(bind=True)
def soft_limit_task(self: Task, task_id: str, seconds: float) -> dict[str, Any]:
    _exp_log(self, task_id, "before_sleep", seconds=seconds)
    try:
        time.sleep(seconds)
    except SoftTimeLimitExceeded:
        _exp_log(self, task_id, "soft_limit", cleanup="успел прибраться")
        raise
    _exp_log(self, task_id, "after_sleep", seconds=seconds)
    return {"task_id": task_id, "slept": seconds}


@celery_app.task(bind=True)
def chain_step(self: Task, n: int) -> int:
    request_id = str(self.request.id or "unknown")
    _exp_log(self, request_id, "chain_step", n=n)
    return n + 1
