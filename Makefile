init:
	@python -m venv .venv

install-deps:
	@python -m pip install -r requirements.txt

install-deps-test:
	@python -m pip install -r requirements.txt -r requirements-test.txt

test:
	@python -m pytest tests

check:
	@python -m mypy travelfootprint --ignore-missing-imports

format:
	@python -m black .

run:
	@python -m django runserver

deploy: format check test
	@gcloud app deploy

.PHONY: install-deps install-deps-test test check format run
