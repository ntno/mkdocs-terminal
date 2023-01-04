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

serve-mkdocs: clean build-mkdocs
	mkdocs serve -v --dev-addr=0.0.0.0:5000

clean:
	rm -rf site/

update-tag:
	git tag -d demo && git push origin :refs/tags/demo
	git tag demo && git push origin demo