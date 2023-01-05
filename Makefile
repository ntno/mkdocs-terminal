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

serve-demo: remove-orphans
	docker compose run --entrypoint "/bin/bash" --service-ports local_example_server -c "make serve site=demo"

serve-docs: remove-orphans
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

clean: clean-demo clean-dist
