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
CONCURRENCY=1 \
  docker compose up -d --build --force-recreate worker1 worker2 redis
docker compose stop worker2
make send ARGS='sleep_task exp04 60'
sleep 15
docker compose start worker2
make events
```

Задачу сначала получает единственный работающий worker. Через 15 секунд задача всё ещё
выполняется, но её `visibility_timeout` уже истёк. При старте `worker2` Redis transport
проверяет просроченные `unacked` и возвращает задачу в очередь.

Дождись двух `after_sleep`, затем нажми `Ctrl+C`.

## Ожидаем

Для одного `task_id=exp04` появляются:

1. `before_sleep` с `redelivered=false` от `worker1`;
2. `before_sleep` с `redelivered=true` от `worker2` до завершения первого выполнения;
3. два `after_sleep` от разных worker.

Поле `retries` остаётся равным `0`: это повторная доставка брокером, а не Celery retry.
`visibility_timeout` задаёт порог просрочки, но не точный момент повторной доставки.

## Наблюдение

- Ожидал:
- Увидел:
