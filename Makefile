# git
.PHONY: update
update:
	git fetch --all
	git stash
	git reset --hard origin/master
	git stash pop

.PHONY: poetry-venv
poetry-venv:
	poetry update

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