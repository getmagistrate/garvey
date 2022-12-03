SHELL := /bin/bash

build:
	rm -rf .venv
	python3.8 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
	mkdir -p data