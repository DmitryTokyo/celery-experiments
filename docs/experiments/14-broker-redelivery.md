# 14. Redis и RabbitMQ после гибели воркера

## Что проверяем

Redis возвращает неподтверждённую задачу после `visibility_timeout`. RabbitMQ возвращает её
после закрытия соединения погибшего consumer.

## Настройки

```python
CELERY_ACKS_LATE = True
VISIBILITY_TIMEOUT = 20
```

## Шаги

1. Установи `BROKER = "redis"`, запусти один worker, отправь минутную задачу и убей worker:

   ```bash
   make up
   docker compose stop worker2
   make send ARGS='sleep_task redis 60'
   sleep 3
   date '+redis killed %s'
   make kill-worker
   docker compose start worker1
   make events WORKERS=worker1
   ```

   После `after_sleep` нажми `Ctrl+C` и запиши время возврата задачи.

2. Установи `BROKER = "rabbit"`, пересоздай worker и повтори:

   ```bash
   docker compose up -d --force-recreate worker1
   make send ARGS='sleep_task rabbit 60'
   sleep 3
   date '+rabbit killed %s'
   make kill-worker
   docker compose start worker1
   make events WORKERS=worker1
   ```

   После `after_sleep` нажми `Ctrl+C` и сравни время с Redis.

## Ожидаем

RabbitMQ обычно возвращает задачу быстрее после потери соединения. Redis ждёт истечения
`visibility_timeout` и очередного цикла восстановления.

## Наблюдение

- Ожидал:
- Увидел:
