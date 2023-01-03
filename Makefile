################################################
## run from machine with docker installed
## requires GNU Make
################################################

ubuntu: 
	docker compose run --rm ubuntu 

build: 
	docker compose run --entrypoint "/bin/bash" ubuntu -c "make build-theme"

serve-demo:
	docker compose run --entrypoint "/bin/bash" --service-ports local_development_server -c "make serve-mkdocs-demo"

open-local-demo:
	open http://0.0.0.0:5000/

open-demo:
	open https://ntno.github.io/mkdocs-terminal-theme



#########################################################
## run from machine or container with required software
## python, pip, GNU Make, etc.
#########################################################

install-build-requirements:
	pip install --upgrade build

build-pip-dist:
	python -m build

build-theme: clean install-build-requirements build-pip-dist

clean-dist:
	rm -rf mkdocs_terminal.egg-info/
	rm -rf dist/

clean: clean-demo clean-dist

install-mkdocs-demo-requirements:
	cd demo && \
	pip install -r ./requirements.txt

build-mkdocs-demo: clean install-mkdocs-demo-requirements
	cd demo && \
	mkdocs build

serve-mkdocs-demo: clean install-mkdocs-demo-requirements
	cd demo && \
	mkdocs serve -v --dev-addr=0.0.0.0:5000

clean-demo:
	cd demo && \
	rm -rf site/