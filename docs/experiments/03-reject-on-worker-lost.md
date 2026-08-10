# 3. `reject_on_worker_lost`

## Что проверяем

Celery возвращает задачу в очередь при гибели дочернего процесса prefork, когда включён
`task_reject_on_worker_lost`.

## Настройки

```python
CELERY_ACKS_LATE = True
CELERY_REJECT_ON_WORKER_LOST = True
VISIBILITY_TIMEOUT = 120
```

`VISIBILITY_TIMEOUT` должен быть больше времени выполнения задачи (60 секунд). Иначе
Redis может повторно доставить уже перезапущенную задачу до её завершения, смешав этот
сценарий с экспериментом 4.

## Шаги

```bash
WORKER_POOL=prefork CONCURRENCY=2 \
  docker compose up -d --build --force-recreate worker1 redis
docker compose stop worker2
make send ARGS='sleep_task exp03 60'
sleep 3
docker compose exec -T worker1 python -c 'import os,pathlib; ps=list(pathlib.Path("/proc").glob("[0-9]*")); p=next(x for x in ps if b"worker" in (x/"cmdline").read_bytes().split(b"\0") and any(a.endswith(b"/celery") for a in (x/"cmdline").read_bytes().split(b"\0"))); children=(p/"task"/p.name/"children").read_text().split(); os.kill(int(children[0]), 9)'
sleep 5
make events WORKERS=worker1
```

Дождись `after_sleep` повторно доставленной задачи, затем нажми `Ctrl+C`.

## Ожидаем

Основной worker остаётся жив. Для одного `task_id=exp03` появляются:

1. `before_sleep` с `redelivered=false` от первого дочернего процесса;
2. `before_sleep` с `redelivered=true` от нового дочернего процесса;
3. `after_sleep` с `redelivered=true` от нового дочернего процесса.

Поле `retries` остаётся равным `0`: это повторная доставка брокером, а не Celery retry.

## Наблюдение

- Ожидал:
- Увидел:
