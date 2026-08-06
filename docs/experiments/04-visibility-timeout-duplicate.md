# 4. `visibility_timeout` короче задачи

## Что проверяем

Долгая неподтверждённая задача может вернуться в Redis раньше завершения и выполняться
параллельно вторым воркером.

## Настройки

```python
CELERY_ACKS_LATE = True
VISIBILITY_TIMEOUT = 10
```

## Шаги

```bash
CONCURRENCY=2 make up
make send ARGS='sleep_task exp04 35'
sleep 45
docker compose logs --tail=200 worker1 worker2
```

## Ожидаем

В логах возможны два `before_sleep` с одним `task_id`, но разными PID или hostname.
Момент восстановления зависит от цикла опроса Redis.

## Наблюдение

- Ожидал:
- Увидел:
