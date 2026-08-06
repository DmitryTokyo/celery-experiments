# 11. Два экземпляра Beat

## Что проверяем

Два независимых scheduler-процесса отправляют одну периодическую задачу дважды.

## Шаги

```bash
docker compose --profile beat up -d --build --scale beat=2 beat worker1 redis rabbitmq
sleep 25
docker compose --profile beat logs --tail=200 beat worker1
```

## Ожидаем

Примерно каждые 10 секунд worker получает два близких события `chain_step` вместо одного.

## Наблюдение

- Ожидал:
- Увидел:
