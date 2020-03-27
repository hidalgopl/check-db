install_deps:
	pip install -r requirements.txt
.PHONY: install_deps

setup_env:
	docker-compose up -d
.PHONY: setup_env

fetch_from_db:
	python checker.py
.PHONY: fetch_from_db

look_for_incosistent:
	python worker.py
.PHONY: look_for_incosistent