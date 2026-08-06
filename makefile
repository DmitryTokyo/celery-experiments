COMPOSE := docker compose

.PHONY: up down restart logs send kill-worker purge

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) --profile beat down --remove-orphans

restart:
	$(COMPOSE) restart worker1 worker2 flower

logs:
	$(COMPOSE) logs -f worker1 worker2 flower

send:
	$(COMPOSE) exec -T worker1 python -m app.send $(ARGS)

kill-worker:
	$(COMPOSE) kill -s SIGKILL worker1

purge:
	$(COMPOSE) exec -T worker1 celery -A app.celery_app:celery_app purge
