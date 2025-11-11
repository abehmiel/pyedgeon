.PHONY: help install test lint format clean build publish docs

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies with Poetry
	poetry install

install-all:  ## Install all dependencies including optional groups
	poetry install --with optimization,docs

test:  ## Run tests with pytest
	poetry run pytest

test-cov:  ## Run tests with coverage report
	poetry run pytest --cov=pyedgeon --cov-report=html --cov-report=term

lint:  ## Run linting checks (ruff + mypy)
	poetry run ruff check pyedgeon/
	poetry run mypy pyedgeon/

lint-fix:  ## Run linting checks and auto-fix issues
	poetry run ruff check --fix pyedgeon/

format:  ## Format code with black and isort
	poetry run black pyedgeon/
	poetry run isort pyedgeon/

format-check:  ## Check code formatting without making changes
	poetry run black --check pyedgeon/
	poetry run isort --check-only pyedgeon/

clean:  ## Clean build artifacts and caches
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

build:  ## Build distribution packages
	poetry build

publish:  ## Publish package to PyPI
	poetry publish

publish-test:  ## Publish package to TestPyPI
	poetry publish -r testpypi

docs:  ## Build documentation
	cd docs && poetry run make html

docs-serve:  ## Build and serve documentation locally
	cd docs && poetry run make html && python -m http.server --directory _build/html

pre-commit:  ## Install pre-commit hooks
	poetry run pre-commit install

pre-commit-run:  ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

update:  ## Update dependencies
	poetry update

lock:  ## Update poetry.lock without installing
	poetry lock --no-update

version-patch:  ## Bump patch version (0.3.1 -> 0.3.2)
	poetry version patch

version-minor:  ## Bump minor version (0.3.1 -> 0.4.0)
	poetry version minor

version-major:  ## Bump major version (0.3.1 -> 1.0.0)
	poetry version major

check:  ## Run all checks (format, lint, test)
	make format-check
	make lint
	make test

ci:  ## Run CI pipeline locally (format, lint, test with coverage)
	make format-check
	make lint
	make test-cov

example:  ## Run quick-start example script (use MESSAGE="text" ROTATIONS=6 OUTPUT="file.png" FONT_PATH="/path/to/font" to customize)
	poetry run python scripts/example.py $(if $(MESSAGE),"$(MESSAGE)","HELLO WORLD") $(if $(ROTATIONS),--rotations $(ROTATIONS),) $(if $(OUTPUT),--output "$(OUTPUT)",) $(if $(FONT_PATH),--font-path "$(FONT_PATH)",)
