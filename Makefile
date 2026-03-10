# Developer Makefile
.PHONY: venv install test

venv:
	python3 -m venv .venv
	.venv/bin/pip install -U pip setuptools wheel

install: venv
	.venv/bin/pip install -r requirements.txt || true

test: venv	PYTHONPATH=art-opp:. .venv/bin/pytest -q
