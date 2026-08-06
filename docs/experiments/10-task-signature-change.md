# 10. Новая сигнатура и старый воркер

## Что проверяем

Работающий воркер продолжает использовать загруженную старую сигнатуру задачи после
изменения файла.

## Шаги

1. Запусти воркер со старой сигнатурой:

   ```bash
   make up
   docker compose stop worker2
   ```

2. Добавь третий аргумент `label` в сигнатуру `sleep_task` в `app/tasks.py`, но не
   перезапускай `worker1`.

3. Отправь сообщение новой формы:

   ```bash
   docker compose exec -T worker1 python -c 'from app.celery_app import celery_app; print(celery_app.send_task("app.tasks.sleep_task", args=["exp10", 2, "new"]).id)'
   sleep 5
   docker compose logs --tail=100 worker1
   ```

4. Пересоздай воркер и повтори отправку:

   ```bash
   docker compose up -d --force-recreate worker1
   docker compose exec -T worker1 python -c 'from app.celery_app import celery_app; print(celery_app.send_task("app.tasks.sleep_task", args=["exp10", 2, "new"]).id)'
   ```

## Ожидаем

Старый воркер падает на несовпадении аргументов. Новый воркер принимает новую сигнатуру.
После опыта верни исходную сигнатуру.

## Наблюдение

- Ожидал:
- Увидел:
