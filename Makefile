.DEFAULT_GOAL := test

test_clean:
	coverage erase
	touch check_file_exists.py

mypy:
	mypy

pylint:
	pylint --include-naming-hint=y run.py resume_app

pytest:
	coverage erase
	pytest
	coverage report -m --fail-under=100

black:
	black run.py resume_app tests

pip-audit:
	pip-audit --desc on

test: mypy pylint pytest black pip-audit
