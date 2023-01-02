ubuntu: 
	docker compose run --rm ubuntu 

build: 
	docker compose run --entrypoint "/bin/bash" ubuntu -c "make build-theme"

install-build-requirements:
	pip install --upgrade build

build-pip-dist:
	python -m build

build-theme: clean-dist install-build-requirements build-pip-dist

clean-dist:
	rm -rf mkdocs_terminal.egg-info/
	rm -rf dist/