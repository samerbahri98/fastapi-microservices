UID := $(shell id -u)
GID := $(shell id -g)

default: dev

.PHONY: dev
dev: inventory-frontend/node_modules .cache/inventory .cache/payment
	sh -c "UID=$(UID) GID=$(GID) docker compose up -d"

inventory-frontend/node_modules:
	sh -c "docker run --user $(UID):$(UID) --rm --volume ./inventory-frontend:/app --workdir /app --entrypoint npm node:20-bullseye -- install"

.cache/%: %/requirements.txt
	mkdir -p $@
	sh -c "docker run --rm \
	--user $(UID):$(UID) \
	--volume $(PWD)/$@:/pip-cache:rw \
	--volume $(PWD)/$(dir $<):/app:ro \
	-e PIP_CACHE_DIR=/pip-cache \
	--workdir /app \
	--entrypoint /bin/bash \
	python:3.9-slim-bullseye \
	-- -c 'python3 -m pip install -r requirements.txt'"