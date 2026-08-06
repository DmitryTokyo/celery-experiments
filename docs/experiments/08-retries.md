# 8. Retries, backoff и jitter

## Что проверяем

Celery повторяет ожидаемую ошибку с растущей задержкой и случайным jitter, затем прекращает
попытки после `max_retries`.

## Шаги

```bash
make up
make send ARGS='fail_task exp08 1.0 4'
docker compose logs -f worker1 worker2
```

Останови просмотр логов после финальной ошибки нажатием `Ctrl+C`.

## Ожидаем

События `attempt` и `retry_scheduled` повторяются. Поле `retries` растёт. Последнее событие —
`retries_exhausted`.

## Наблюдение

- Ожидал:
- Увидел:
