# 9. Защита части задачи от повторного выполнения

## Что проверяем

После потери ACK брокер может запустить одну задачу повторно. Идемпотентный ключ через `SETNX`
позволяет выполнить защищённую часть логики только при первой доставке и пропустить её при
повторной.

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
docker compose exec -T redis redis-cli -n 1 del celery-lab:write-once:exp09
make send ARGS='write_once exp09'
sleep 2
make kill-worker
docker compose start worker1
make events WORKERS=worker1
```

После повторного `write_once_complete` нажми `Ctrl+C`.

## Ожидаем

При первой доставке `setnx` содержит `created=true`, затем появляется
`protected_logic_executed`. Worker погибает до ACK, поэтому брокер доставляет задачу повторно.

При повторной доставке `setnx` содержит `created=false`, затем появляется
`protected_logic_skipped`: защищённая часть не выполняется второй раз. Поле `redelivered`
меняется на `true`, а `retries` остаётся равным `0`, потому что это повторная доставка брокером,
а не Celery retry.

`SETNX` фиксирует право на выполнение, но не гарантирует завершение защищённой операции. Для
реального побочного эффекта нужна атомарная схема, транзакция или idempotency key внешнего
сервиса.

## Наблюдение

- Ожидал:
- Увидел:
