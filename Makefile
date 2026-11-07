# AI Toolkit v2 Development Makefile

SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: test-wizard verify clean audit help

test-wizard:
	python3 bin/wizard/init_profile.py --preset enterprise_clean_bloc --target-dir .
	./bin/check-profile .
	rm -f project_profile.yaml

verify:
	bash setup/verify-setup.sh

help:
	@echo "AI Toolkit v2 Development Commands:"
	@echo "  make test-wizard  - Test profile wizard against presets"
	@echo "  make verify       - Run integrity checks across rules and templates"
