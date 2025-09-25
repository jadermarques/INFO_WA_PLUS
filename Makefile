VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
STREAMLIT=$(VENV)/bin/streamlit
APP=src/app

.PHONY: venv install install-core setup gui cli test fmt lint db-init backup

venv:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate

install: venv
	$(PIP) install -r requirements.txt

install-core: venv
	$(PIP) install -r requirements-core.txt

setup: venv
	$(PIP) install -r requirements.txt
	@[ -f .env ] || cp .env.example .env

fmt:
	ruff format $(APP) || true

lint:
	ruff check $(APP) || true

cli:
	$(PY) -m src.app.interfaces.cli.app --help

gui:
	$(STREAMLIT) run src/app/interfaces/web/app.py

test:
	$(PY) -m pytest -q

backup:
	$(PY) -m src.app.interfaces.cli.app backup

db-init:
	$(PY) -m src.app.interfaces.cli.app db-init
