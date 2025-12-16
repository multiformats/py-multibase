.PHONY: clean-pyc clean-build docs clean help pr
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "Available commands:"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test artifacts"
	@echo "clean - run clean-build, clean-pyc, and clean-test"
	@echo "setup - install development requirements"
	@echo "fix - fix formatting & linting issues with ruff"
	@echo "lint - run pre-commit hooks on all files"
	@echo "typecheck - run mypy type checking"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - run tests with coverage report"
	@echo "docs-ci - generate docs for CI"
	@echo "docs - generate docs and open in browser"
	@echo "servedocs - serve docs with live reload"
	@echo "dist - build package and show contents"
	@echo "pr - run clean, lint, and test (everything needed before creating a PR)"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -fr .mypy_cache
	rm -fr .ruff_cache
	rm -f .coverage
	rm -fr htmlcov/

setup:
	pip install -e ".[dev]"

lint:
	pre-commit run --all-files

fix:
	python -m ruff check --fix

typecheck:
	pre-commit run mypy-local --all-files

test:
	python -m pytest tests

coverage:
	coverage run --source multibase -m pytest tests
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs-ci:
	rm -f docs/multibase.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ multibase
	$(MAKE) -C docs clean
	mkdir -p docs/_static
	$(MAKE) -C docs html SPHINXOPTS="-W"

docs: docs-ci
	$(BROWSER) docs/_build/html/index.html

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

dist: clean
	python -m build
	ls -l dist

pr: clean fix lint typecheck test
	@echo "PR preparation complete! All checks passed."

# docs helpers

validate-newsfragments:
	python ./newsfragments/validate_files.py
	towncrier build --draft --version preview

build-docs:
	sphinx-apidoc -o docs/ . "*conftest*" tests/
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(MAKE) -C docs doctest

# release commands

package-test: clean
	python -m build
	python scripts/release/test_package.py

notes: check-bump validate-newsfragments
	# Let UPCOMING_VERSION be the version that is used for the current bump
	$(eval UPCOMING_VERSION=$(shell bump-my-version bump --dry-run $(bump) -v | awk -F"'" '/New version will be / {print $$2}'))
	# Now generate the release notes to have them included in the release commit
	towncrier build --yes --version $(UPCOMING_VERSION)
	# Before we bump the version, make sure that the towncrier-generated docs will build
	make build-docs
	git commit -m "Compile release notes for v$(UPCOMING_VERSION)"

release: check-bump check-git clean
	# verify that notes command ran correctly
	./newsfragments/validate_files.py is-empty
	CURRENT_SIGN_SETTING=$(git config commit.gpgSign)
	git config commit.gpgSign true
	bump-my-version bump $(bump)
	python -m build
	git config commit.gpgSign "$(CURRENT_SIGN_SETTING)"
	git push upstream && git push upstream --tags
	twine upload dist/*

# release helpers

check-bump:
ifndef bump
	$(error bump must be set, typically: major, minor, patch, or devnum)
endif

check-git:
	# require that upstream is configured for multiformats/py-multibase
	@if ! git remote -v | grep "upstream[[:space:]]git@github.com:multiformats/py-multibase.git (push)\|upstream[[:space:]]https://github.com/multiformats/py-multibase (push)"; then \
		echo "Error: You must have a remote named 'upstream' that points to 'py-multibase'"; \
		exit 1; \
	fi
