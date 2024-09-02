-include .env

export

PROJECT_NAME = nwcrawler
PACKAGE_NAME = nwcrawler

PWD := $(shell pwd)
JUPYTER_IMAGE := $(PROJECT_NAME)_jupyter:latest

DOCKER_IMG := $(PROJECT_NAME):latest
DOCKER_ENV := --env-file .env

DOCKER_RUN := docker run --rm -t

PYTEST := python -B -m pytest

build:
	docker build -f docker/Dockerfile -t $(DOCKER_IMG) .

scrape: build
ifdef last
	$(DOCKER_RUN) $(DOCKER_ENV)  -v $(PWD):/app -i $(DOCKER_IMG) nwcrawler articles scrape -l $(last)
else
	$(DOCKER_RUN) $(DOCKER_ENV) -v $(PWD):/app -i $(DOCKER_IMG) nwcrawler articles scrape
endif

shell: build
	$(DOCKER_RUN) $(DOCKER_ENV) -i --entrypoint=/bin/bash $(DOCKER_IMG)

clean:
	docker images -q $(PROJECT_NAME)* | xargs -I {} docker rmi -f {}

mypy: build
	$(DOCKER_RUN) $(DOCKER_IMG) mypy src tests

flake: build
	$(DOCKER_RUN) $(DOCKER_IMG) flake8 src tests

bandit: build
	$(DOCKER_RUN) $(DOCKER_IMG) bandit src tests

format:
	black src tests

lint: mypy flake bandit

check:
	$(DOCKER_RUN) $(DOCKER_IMG) $(PYTEST) tests/unit

build-jupyter:
	docker build -f docker/Dockerfile.jupyter -t $(JUPYTER_IMAGE) .

start-jupyter: build-jupyter
	docker run $(DOCKER_ENV) -p 8888:8888 -v $(PWD):/app $(JUPYTER_IMAGE)

.PHONY: all test clean