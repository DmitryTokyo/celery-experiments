# 7. Soft и hard time limits

## Что проверяем

Soft limit даёт задаче обработать исключение. Hard limit убивает процесс без cleanup.

## Настройки

```python
SOFT_TIME_LIMIT = 5
TIME_LIMIT = 8
```

## Шаги

```bash
make up
docker compose stop worker2
make send ARGS='soft_limit_task soft 20'
make send ARGS='sleep_task hard 20'
sleep 15
docker compose logs --tail=200 worker1
```

## Ожидаем

`soft_limit_task` пишет `cleanup=успел прибраться`. `sleep_task` завершается hard timeout
без такого лога.

## Наблюдение

- Ожидал:
- Увидел:
