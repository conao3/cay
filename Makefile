## Makefile

all:

##################################################

.PHONY: all build test clean

all: build

##############################

build:

test:
	poetry run pytest

clean:

.PHONY: lint
lint:
	poetry run flake8 src test
	poetry run isort --check --diff .
	poetry run black --check .


.PHONY: format
format:
	poetry run autoflake -i --remove-all-unused-imports --remove-unused-variables -r .
	poetry run isort .
	poetry run black .
