version=$(shell cat package.json | jq .version -r)


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

clean: clean-dist

install-tox-requirements:
	python -m pip install -U tox

tox: install-tox-requirements
	python -m tox -e py

check-version-match:
	cat terminal/theme_version.html | grep -s --silent $(version)\"\>\$$ -o 

check-site:
ifndef site
	$(error site is not set)
endif