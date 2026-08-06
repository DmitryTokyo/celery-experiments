# 3. `reject_on_worker_lost`

## Что проверяем

Celery возвращает задачу в очередь при гибели дочернего процесса prefork, когда включён
`task_reject_on_worker_lost`.

## Настройки

```python
CELERY_ACKS_LATE = True
CELERY_REJECT_ON_WORKER_LOST = True
```

## Шаги

```bash
WORKER_POOL=prefork CONCURRENCY=2 docker compose up -d --build --force-recreate worker1 redis
docker compose stop worker2
make send ARGS='sleep_task exp03 60'
sleep 3
docker compose exec -T worker1 python -c 'import os,pathlib; ps=list(pathlib.Path("/proc").glob("[0-9]*")); p=next(x for x in ps if b"worker" in (x/"cmdline").read_bytes().split(b"\0") and any(a.endswith(b"/celery") for a in (x/"cmdline").read_bytes().split(b"\0"))); children=(p/"task"/p.name/"children").read_text().split(); os.kill(int(children[0]), 9)'
sleep 5
make events WORKERS=worker1
```

После повторного `before_sleep` нажми `Ctrl+C`.

## Ожидаем

Основной worker остаётся жив. Задача назначается новому дочернему процессу повторно.

## Наблюдение

- Ожидал:
- Увидел:
