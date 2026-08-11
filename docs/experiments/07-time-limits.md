# 7. Soft и hard time limits

## Что проверяем

Soft limit даёт задаче обработать исключение. Hard limit убивает процесс без cleanup.

## Настройки

### Отрабатываем SoftTimeLimitExceeded

```python
SOFT_TIME_LIMIT = 5
TIME_LIMIT = None
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

`soft_limit_task` ловит SoftTimeLimitExceeded, пишет `cleanup=managed to clean up in time`. 
`sleep_task` не ловит исключение, Celery пишет traceback.


### Отрабатываем Hard Limit

```python
SOFT_TIME_LIMIT = None
TIME_LIMIT = 5
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

Ни обработчик SoftTimeLimitExceeded, ни cleanup не выполняются.
Полные логи показывают `Hard time limit ... exceeded`

## Наблюдение

- Ожидал:
- Увидел:
