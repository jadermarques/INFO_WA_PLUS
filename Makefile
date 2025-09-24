PY=python3
PIP=pip3
APP=src/app

.PHONY: venv install install-core setup gui cli test fmt lint db-init backup

venv:
	python3 -m venv .venv
	. .venv/bin/activate

install:
	$(PIP) install -r requirements.txt

install-core:
	$(PIP) install -r requirements-core.txt

setup:
	bash scripts/dev-setup.sh --gui

fmt:
	ruff format $(APP) || true

lint:
	ruff check $(APP) || true

cli:
	$(PY) -m src.app.interfaces.cli.app --help

gui:
	streamlit run src/app/interfaces/web/app.py

test:
	$(PY) -m pytest -q

backup:
	$(PY) -m src.app.interfaces.cli.app backup

db-init:
	$(PY) -m src.app.interfaces.cli.app db-init
