# Эксперименты с Celery

Каждый документ проверяет одну гипотезу. Команды выполняются из корня проекта.

Перед новым экспериментом:

```bash
make down
```

Верни изменённые значения в `app/settings.py` после завершения опыта.

Учебные события без служебного шума Celery:

```bash
make events                 # оба воркера
make events WORKERS=worker1 # только worker1
```

Остановить просмотр: `Ctrl+C`.

1. [Позднее подтверждение и повторная доставка](01-acks-late-redelivery.md)
2. [Раннее подтверждение и потеря задачи](02-acks-early-task-loss.md)
3. [Потеря дочернего процесса воркера](03-reject-on-worker-lost.md)
4. [Короткий visibility timeout](04-visibility-timeout-duplicate.md)
5. [Prefetch и голодание воркеров](05-prefetch-starvation.md)
6. [Раздельные очереди](06-separate-queues.md)
7. [Soft и hard time limits](07-time-limits.md)
8. [Retries, backoff и jitter](08-retries.md)
9. [Повторная доставка и счётчик retries](09-redelivery-vs-retry.md)
10. [Новая сигнатура и старый воркер](10-task-signature-change.md)
11. [Два экземпляра Beat](11-multiple-beat.md)
12. [Prefork, threads и GIL](12-pools-and-gil.md)
13. [Result backend](13-result-backend.md)
14. [Redis и RabbitMQ после гибели воркера](14-broker-redelivery.md)
