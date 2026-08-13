# Celery experiments

Учебный стенд для экспериментов с Celery, Redis и RabbitMQ.

[English version](readme.md)

## Запуск

```bash
cp .env.example .env
uv sync
make up
```

Redis используется как брокер по умолчанию. Flower доступен на
<http://localhost:5555>. RabbitMQ Management доступен на
<http://localhost:15672>.

Проверка:

```bash
make send ARGS='sleep_task smoke 2'
make events
```

Остановка:

```bash
make down
```

## Настройки

Значения для ручных экспериментов находятся в `.env`. После изменения
перезапусти воркеры командой `make restart`.

## Эксперименты

Список гипотез и пошаговые инструкции: [docs/experiments](docs/experiments/README.md).

## Полезные команды

```bash
make logs
make events
make restart
make kill-worker
make purge
```

`make events` показывает только учебные события `[EXP]`. Остановить просмотр: `Ctrl+C`.

## Проверки кода

```bash
uv run ruff check .
uv run ruff format --check .
```

## Лицензия

Проект распространяется по [лицензии MIT](LICENSE).
