SHELL := /bin/bash
PYTHON ?= python3
PORT ?= 8080

.PHONY: help install docs data build serve clean distclean publish-spec
help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'
install:  ## Install site dependencies (Node 24 or later)
	npm ci
docs:  ## Fetch released product documentation
	$(PYTHON) scripts/fetch_docs.py
data:  ## Collect released server versions and tools
	$(PYTHON) scripts/collect_servers.py
build:  ## Build the static site
	npm run build
serve:  ## Start the development server
	npm run dev -- --host localhost --port $(PORT)
publish-spec:  ## Tag the spec's main as VERSION=vX.Y.Z [NOTES="..."] and publish it here now
	@VERSION="$(VERSION)" NOTES="$(NOTES)" scripts/publish_spec.sh
clean:  ## Remove build artifacts
	rm -rf dist/ .astro/
distclean: clean  ## Remove build artifacts and caches
	rm -rf __pycache__ .cache node_modules
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
