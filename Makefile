SHELL := /bin/bash

build:
	rm -rf .venv
	python3.10 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
	mkdir -p data

run:
	errbot

daemon:
	errbot --daemon