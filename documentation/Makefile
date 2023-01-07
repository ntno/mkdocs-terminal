#########################################################
## run from machine or container with required software
## python, pip, GNU Make, etc.
#########################################################
upgrade-pip:
	python3 -m pip install --upgrade pip

install-mkdocs-requirements: upgrade-pip
	pip install -r ./requirements.txt

build-mkdocs: clean install-mkdocs-requirements
	mkdocs build -v

serve-mkdocs: build-mkdocs
	mkdocs serve -v --dev-addr=0.0.0.0:8080 -f local.yml

clean:
	rm -rf site/

update-tag:
	git tag -d documentation && git push origin :refs/tags/documentation
	git tag documentation && git push origin documentation