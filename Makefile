REGISTRY=ghcr.io/almazkun
IMAGE_NAME=django_telegram_bot
CONTAINER_NAME=django-telegram-bot
VERSION=latest
k=./

PIPENV=pipenv run python manage.py 

.PHONY: help

help:
	@echo "Usage: make <command>"
	@echo "Commands:"

	@echo "  lint        Run lint"
	@echo "  build       Build docker image"
	@echo "  push        Push docker image to registry"
	@echo "  run         Run docker container"
	@echo "  stop        Stop docker container"
	@echo "  restart     Restart docker container"
	@echo "  pull        Pull docker image from registry"
	@echo "  logs        Show docker container logs"
	@echo "  migrate     Run django migrate"
	@echo "  startdemo   Run django startdemo"
	@echo "  runserver   Run django runserver"

lint:
	@echo "Running lint..."
	pipenv run ruff check --fix -e .
	pipenv run black .
	pipenv run djlint . --reformat

build:
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .

push:
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

run:
	docker run \
		--rm \
		-ti \
		-d \
		-p 8000:8000 \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		$(REGISTRY)/$(IMAGE_NAME):$(VERSION)

stop:
	docker stop $(CONTAINER_NAME)

restart:
	docker restart $(CONTAINER_NAME)

pull:
	docker pull $(REGISTRY)/$(IMAGE_NAME):latest

logs:
	docker logs $(CONTAINER_NAME) -f

migrate:
	docker exec $(CONTAINER_NAME) python manage.py migrate

startdemo:
	docker exec $(CONTAINER_NAME) python manage.py startdemo

mng:
	pipenv run python manage.py $(cmd) $(args)

mng-migrate:
	@make mng cmd="migrate"

mng-startdemo:
	@make mng cmd="startdemo"

mng-runserver:
	@make mng cmd="runserver"

mng-test:
	@make mng cmd="test" args="$(k)"