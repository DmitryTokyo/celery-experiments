# 12. Prefork, threads и GIL

## Что проверяем

Одинаковый объём CPU-bound Python-кода выполняется параллельно в нескольких процессах, но
потоки одного процесса конкурируют за GIL.

Задача делает фиксированное число Python-итераций. Это важно: при ограничении каждой задачи
фиксированным временем prefork и threads закончили бы партии примерно одновременно, а GIL
проявился бы только в разном числе выполненных итераций.

## Шаги

Prefork:

```bash
WORKER_POOL=prefork CONCURRENCY=4 docker compose up -d --build --force-recreate worker1 redis rabbitmq
docker compose stop worker2
date '+prefork started %T'
make send ARGS='burn_cpu prefork 20_000_000 --count 8'
make events WORKERS=worker1
```

После восьмого `after_burn` запиши время, нажми `Ctrl+C` и повтори с threads:

```bash
make purge
WORKER_POOL=threads CONCURRENCY=4 docker compose up -d --force-recreate worker1
date '+threads started %T'
make send ARGS='burn_cpu threads 20_000_000 --count 8'
make events WORKERS=worker1
```

После восьмого `after_burn` запиши время и нажми `Ctrl+C`.

## Ожидаем

При наличии хотя бы четырёх доступных CPU-ядер prefork завершает восемь одинаковых задач
заметно быстрее threads. Prefork распределяет задачи между процессами, а Python-код четырёх
потоков одного процесса не исполняется параллельно из-за GIL.

Сравни wall-clock время от `started` до восьмого `after_burn`. Абсолютное время зависит от CPU
и лимитов Docker. Если одна задача выполняется слишком быстро или слишком долго, одинаково
измени число итераций в обеих сериях.

## Наблюдение

- Ожидал:
- Увидел:
