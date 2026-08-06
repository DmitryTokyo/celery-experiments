# 2. `acks_late=False` и потеря задачи

## Что проверяем

При раннем подтверждении брокер считает задачу завершённой до фактического выполнения.

## Настройки

```python
CELERY_ACKS_LATE = False
```

## Шаги

```bash
make up
docker compose stop worker2
make send ARGS='sleep_task exp02 60'
sleep 3
make kill-worker
docker compose start worker1
sleep 10
docker compose logs --tail=100 worker1
```

## Ожидаем

После перезапуска второго `before_sleep` нет. Задача потеряна.

## Наблюдение

- Ожидал:
- Увидел:
