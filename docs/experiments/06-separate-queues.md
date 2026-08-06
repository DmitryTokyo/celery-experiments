# 6. Раздельные очереди

## Что проверяем

Длинные задачи в очереди `long` не задерживают короткие задачи из очереди `short`.

## Шаги

Для этого опыта воркерам нужны разные значения `QUEUES`, поэтому используем одноразовые
environment overrides:

```bash
QUEUES=long docker compose up -d --build --force-recreate worker1 redis rabbitmq
QUEUES=short docker compose up -d --build --force-recreate worker2
make send ARGS='sleep_task long 60 --count 2 --queue long'
make send ARGS='sleep_task short 1 --count 10 --queue short'
make events
```

Когда оба воркера начнут выполнять свои очереди, нажми `Ctrl+C`.

## Ожидаем

`worker1` выполняет только `long`, `worker2` — только `short`. Короткие задачи не ждут.

## Наблюдение

- Ожидал:
- Увидел:
