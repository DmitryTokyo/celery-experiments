COMPOSE := docker compose

.PHONY: up down restart logs events send kill-worker purge redis-watch redis-unacked

WORKERS ?= worker1 worker2

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) --profile beat down --remove-orphans

restart:
	$(COMPOSE) restart worker1 worker2 flower

logs:
	$(COMPOSE) logs -f worker1 worker2 flower

events:
	$(COMPOSE) logs -f $(WORKERS) | grep '\[EXP\]'

send:
	$(COMPOSE) exec -T worker1 python -m app.send $(ARGS)

kill-worker:
	$(COMPOSE) kill -s SIGKILL worker1

purge:
	$(COMPOSE) exec -T worker1 celery -A app.celery_app:celery_app purge

redis-watch:
	watch -n 0.5 '$(COMPOSE) exec -T redis redis-cli -n 0 eval "return {redis.call(\"llen\",\"default\"), redis.call(\"llen\",\"short\"), redis.call(\"llen\",\"long\"), redis.call(\"hlen\",\"unacked\")}" 0'

redis-unacked:
	@echo "unacked:"
	@$(COMPOSE) exec -T redis redis-cli -n 0 hgetall unacked
	@echo "unacked_index:"
	@$(COMPOSE) exec -T redis redis-cli -n 0 zrange unacked_index 0 -1 withscores
