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

serve-demo:
	docker compose run --entrypoint "/bin/bash" --service-ports local_demo_server -c "make serve-mkdocs"

serve-docs:
	docker compose run --entrypoint "/bin/bash" --service-ports local_documentation_server -c "make serve-mkdocs"



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

update-demo-tag:
	git tag -d demo && git push origin :refs/tags/demo
	git tag demo && git push origin demo