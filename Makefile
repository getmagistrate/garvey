.PHONY: all build configure run

-include .env

SHELL := /bin/bash

all: build configure

build:
	rm -rf .venv
	python3.8 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
	mkdir -p data

configure:
	source .venv/bin/activate && echo "{'configs': {'Webserver': {'HOST': '0.0.0.0', 'PORT': ${WEBSERVER_HTTP_PORT}, 'SSL': {'certificate': '', 'enabled': False, 'host': '0.0.0.0', 'key': '', 'port': ${WEBSERVER_HTTPS_PORT}}}}}" | errbot --storage-set core

run:
	source .venv/bin/activate && errbot