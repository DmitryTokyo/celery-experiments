# Celery experiments

A hands-on lab for reproducible experiments with Celery, Redis, and RabbitMQ.

[Русская версия](README.ru.md)

## Getting started

```bash
cp .env.example .env
uv sync
make up
```

Redis is the default broker. Flower is available at <http://localhost:5555>.
RabbitMQ Management is available at
<http://localhost:15672>.

Verify the setup:

```bash
make send ARGS='sleep_task smoke 2'
make events
```

Stop the services:

```bash
make down
```

## Configuration

Settings for manual experiments live in `.env`. After changing them, restart the
workers with `make restart`.

## Experiments

The lab contains 14 experiments covering acknowledgements and redelivery, worker
failures, visibility timeouts, prefetching, queues, time limits, retries, task signature
changes, Celery Beat, execution pools and the GIL, result backends, and broker behavior.

Detailed experiment guides are currently available in Russian:
[docs/experiments](docs/experiments/README.md).

## Useful commands

```bash
make logs
make events
make restart
make kill-worker
make purge
```

`make events` shows only the lab's `[EXP]` events. Press `Ctrl+C` to stop watching.

## Code checks

```bash
uv run ruff check .
uv run ruff format --check .
```

## License

This project is available under the [MIT License](LICENSE).
