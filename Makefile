SHELL := /bin/bash

build:
	docker build -t wapp .

up:
	docker compose up --detach

down:
	docker compose down

logs:
	docker compose logs -f --tails=200
