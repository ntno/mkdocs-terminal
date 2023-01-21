version=$(shell cat package.json | jq .version -r)

ifeq ($(USE_SUDO),1)
   SUDO_FLAG = sudo
endif

.PHONY: check-version-match clean

################################################
## run from machine with docker installed
## requires GNU Make
################################################

ubuntu: 
	docker compose run --rm ubuntu 

build: 
	docker compose run --entrypoint "/bin/bash" ubuntu -c "make build-theme"

remove-orphans: 
	docker compose down --remove-orphans

serve: check-site
	docker compose run --entrypoint "/bin/bash" --service-ports local_examples_server -c "make serve site=$(site)"

serve-docs: 
	docker compose run --entrypoint "/bin/bash" --service-ports local_documentation_server -c "make serve-mkdocs"

serve-local-theme: 
	docker compose run --entrypoint "/bin/bash" --service-ports local_theme_server -c "make build-local-theme-and-serve"


#########################################################
## run from machine or container with required software
## python, pip, GNU Make, etc.
#########################################################

install-build-requirements:
	pip install --upgrade build

build-pip-dist:
	python -m build --outdir ./dist

build-theme: clean install-build-requirements build-pip-dist

check-dist:
	tar tf dist/*.tar.gz
	unzip -l dist/*.whl

clean-dist:
	rm -rf dist/

clean-node:
	rm -rf node_modules/

clean: clean-dist clean-node

install-test-prereqs:
	$(SUDO_FLAG) apt-get update && $(SUDO_FLAG) apt install -y tidy

install-test-requirements:	
	pip install -r requirements.test.txt

install-tox:
	python -m pip install -U tox

tox: install-tox install-test-prereqs
	python -m tox -e py 
	python -m tox -e pytest-linux

check-version-match:
	cat terminal/theme_version.html | grep -s --silent $(version)\"\>\$$ -o 

install-from-dist: build-theme
	pip uninstall mkdocs-terminal
	pip install dist/*.tar.gz

build-local-theme-and-serve: install-from-dist
	cd documentation && \
	$(MAKE) serve-local

#for developer use, assumes you have already installed prereqs
quick-tests:
	flake8 --ignore E501 terminal && \
	flake8 --ignore E501 tests && \
	pytest --color=yes --capture=no tests

#for developer use, assumes you have already installed prereqs
generate-test-coverage:
	pytest --cov=terminal --cov-branch --cov-report=html tests/
	rm -rf documentation/docs/about/coverage-report/.gitignore


check-site:
ifndef site
	$(error site is not set)
endif