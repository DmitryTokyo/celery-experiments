# 14. Redis и RabbitMQ после гибели воркера

## Что проверяем

Redis возвращает неподтверждённую задачу после `visibility_timeout`. RabbitMQ возвращает её
после закрытия соединения погибшего consumer.

Измеряем задержку от гибели worker до повторного `before_sleep`. Длительность задачи меньше
`visibility_timeout`, чтобы успешная повторная попытка успела завершиться и эксперимент не
превратился в проверку параллельных дублей из эксперимента 4.

## Настройки

В `.env` установи:

```dotenv
CELERY_ACKS_LATE=true
VISIBILITY_TIMEOUT=20
```

## Шаги

1. Установи в `.env` `BROKER=redis`, запусти один worker, отправь задачу и убей worker:

   ```bash
   make up
   docker compose stop worker2
   make send ARGS='sleep_task redis 10'
   sleep 3
   date '+redis killed %T'
   make kill-worker
   docker compose start worker1
   make events WORKERS=worker1
   ```

   При втором `before_sleep` с `redelivered=true` запиши время. После `after_sleep` нажми
   `Ctrl+C`.

2. Установи в `.env` `BROKER=rabbit`, пересоздай worker и повтори:

   ```bash
   docker compose up -d --force-recreate worker1
   make send ARGS='sleep_task rabbit 10'
   sleep 3
   date '+rabbit killed %T'
   make kill-worker
   docker compose start worker1
   make events WORKERS=worker1
   ```

   При втором `before_sleep` с `redelivered=true` запиши время. После `after_sleep` нажми
   `Ctrl+C` и сравни задержку с Redis.

## Ожидаем

RabbitMQ обычно повторно доставляет задачу вскоре после обнаружения закрытого соединения.
Redis ждёт истечения `visibility_timeout` и очередного цикла восстановления. Timeout Redis
отсчитывается от первой доставки задачи, а не от момента гибели worker, поэтому при убийстве
через три секунды повторная доставка ожидается примерно через оставшиеся 17 секунд плюс
задержка цикла восстановления.

В обеих сериях повторный `before_sleep` содержит `redelivered=true`, а `retries` остаётся `0`:
это redelivery того же сообщения брокером, не Celery retry.

## Наблюдение

- Ожидал:
- Увидел:
