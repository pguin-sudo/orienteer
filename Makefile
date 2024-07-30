# git
.PHONY: update
update:
	git fetch
	git pull


# modules
.PHONY: orienteer
orienteer:
	poetry run py -m orienteer

.PHONY: api
api:
	poetry run py -m orienteer.api

.PHONY: bot
bot:
	poetry run py -m orienteer.bot

.PHONY: checker
checker:
	poetry run py -m orienteer.checker


# compose
.PHONY: redis
redis:
	poetry run docker-compose up redis
