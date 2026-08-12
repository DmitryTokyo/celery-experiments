# 13. Result backend

## Что проверяем

Result backend хранит состояние и возвращённое значение задачи. С Redis клиент видит переход
к `SUCCESS` и получает значение через `get()`. Без result backend получить состояние и
значение через `AsyncResult` нельзя.

## Шаги

Сначала установи в `.env`:

```dotenv
RESULT_BACKEND=redis://redis:6379/2
```

Запусти задачу, получи результат и проверь финальное состояние:

```bash
make up
docker compose exec -T worker1 python -c 'from app.tasks import chain_step; r=chain_step.delay(1); print("result:", r.get(timeout=10)); print("state:", r.state)'
```

Затем установи в `.env` `RESULT_BACKEND=disabled`, пересоздай worker и отдельно попробуй
прочитать состояние и результат:

```bash
docker compose up -d --force-recreate worker1
docker compose exec -T worker1 python -c 'from app.tasks import chain_step; r=chain_step.delay(1); print("backend:", type(r.backend).__name__); print("state:", r.state)'
docker compose exec -T worker1 python -c 'from app.tasks import chain_step; print(chain_step.delay(1).get(timeout=10))'
```

## Ожидаем

С Redis команда печатает `result: 2` и `state: SUCCESS`. Без backend задача всё равно
отправляется и выполняется. Первая проверка печатает `backend: DisabledBackend`, затем чтение
`state` завершается ошибкой. Вторая проверка завершается `NotImplementedError` при вызове
`get()`: результат и состояние задачи не были сохранены.

## Наблюдение

- Ожидал:
- Увидел:
