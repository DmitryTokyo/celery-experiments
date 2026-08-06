# 9. Повторная доставка не увеличивает `retries`

## Что проверяем

Повторная доставка брокером и Celery retry — разные механизмы. `SETNX` показывает повторное
выполнение побочного эффекта.

## Настройки

```python
CELERY_ACKS_LATE = True
VISIBILITY_TIMEOUT = 15
WRITE_ONCE_POST_SETNX_DELAY = 15
```

## Шаги

```bash
make up
docker compose stop worker2
make send ARGS='write_once exp09'
sleep 2
make kill-worker
docker compose start worker1
make events WORKERS=worker1
```

После повторного `write_once_complete` нажми `Ctrl+C`.

## Ожидаем

Первый `setnx` содержит `created=true`, повторный — `created=false`. В обоих выполнениях
`retries=0`.

## Наблюдение

- Ожидал:
- Увидел:
