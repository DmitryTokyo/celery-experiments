# 1. `acks_late=True` и повторная доставка

## Что проверяем

Задача подтверждается после выполнения. После `SIGKILL` неподтверждённая задача должна
вернуться из Redis в очередь.

## Настройки

В `app/settings.py` установи:

```python
CELERY_ACKS_LATE = True
VISIBILITY_TIMEOUT = 20
```

## Шаги

```bash
make up
docker compose stop worker2
make send ARGS='sleep_task exp01 60'
sleep 3
make kill-worker
docker compose start worker1
make events
```

Дождись `after_sleep` повторно доставленной задачи, затем нажми `Ctrl+C`.

## Ожидаем

Для одного `task_id=exp01` появятся:

1. `before_sleep` с `redelivered=false`;
2. `before_sleep` с `redelivered=true`;
3. `after_sleep` с `redelivered=true`.

Поле `retries` останется равным `0`: повторная доставка не является Celery retry.

## Наблюдение

- Ожидал:
- Увидел:
