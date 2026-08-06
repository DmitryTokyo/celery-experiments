# 13. Result backend

## Что проверяем

Backend хранит состояние и результат задачи. Без backend получить результат через `get()`
нельзя.

## Шаги

Сначала установи:

```python
RESULT_BACKEND = "redis://redis:6379/2"
```

Запусти и получи результат:

```bash
make up
docker compose exec -T worker1 python -c 'from app.tasks import chain_step; r=chain_step.delay(1); print(r.get(timeout=10))'
```

Затем установи `RESULT_BACKEND = "disabled"`, пересоздай worker и проверь тип backend:

```bash
docker compose up -d --force-recreate worker1
docker compose exec -T worker1 python -c 'from app.tasks import chain_step; print(type(chain_step.delay(1).backend).__name__)'
```

## Ожидаем

С Redis первая команда печатает `2`. Без backend возвращается отключённый backend, результат
не сохраняется.

## Наблюдение

- Ожидал:
- Увидел:
