SHELL   := /bin/bash
PYTHON  ?= python3
MKDOCS  ?= mkdocs
PORT    ?= 8080

.PHONY: help install data build serve clean distclean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	$(PYTHON) -m pip install -r requirements.txt

data:  ## Collect every server's released version and tools, and fetch install.sh
	$(PYTHON) scripts/collect_servers.py
	curl -fsSL https://raw.githubusercontent.com/qso-graph/qso-graph-config/main/install.sh -o docs/install.sh

build:  ## Build the static site into site/
	$(MKDOCS) build

serve:  ## Start the dev server on PORT (default 8080)
	$(MKDOCS) serve --dev-addr localhost:$(PORT)

clean:  ## Remove build artifacts
	rm -rf site/

distclean: clean  ## Remove build artifacts and Python caches
	rm -rf __pycache__ .cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
