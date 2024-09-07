# git
.PHONY: update
update:
	git fetch --all
	git stash
	git reset --hard origin/master
	poetry update
	git stash pop


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

.PHONY: tests
tests:
	poetry run py -m tests