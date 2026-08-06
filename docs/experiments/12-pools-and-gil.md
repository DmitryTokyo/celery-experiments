# 12. Prefork, threads и GIL

## Что проверяем

CPU-bound Python-код масштабируется процессами, но не потоками из-за GIL.

## Шаги

Prefork:

```bash
WORKER_POOL=prefork CONCURRENCY=4 docker compose up -d --build --force-recreate worker1 redis rabbitmq
docker compose stop worker2
make send ARGS='burn_cpu prefork 10 --count 8'
make events WORKERS=worker1
```

После завершения задач нажми `Ctrl+C` и повтори с threads:

```bash
make purge
WORKER_POOL=threads CONCURRENCY=4 docker compose up -d --force-recreate worker1
make send ARGS='burn_cpu threads 10 --count 8'
make events WORKERS=worker1
```

После завершения задач нажми `Ctrl+C`.

## Ожидаем

Prefork использует несколько CPU-ядер. Threads конкурируют за GIL и дают меньший выигрыш.
Сравни время между `before_burn` и завершением последней задачи.

## Наблюдение

- Ожидал:
- Увидел:
