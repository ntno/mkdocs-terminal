#########################################################
## run from machine or container with required software
## python, pip, GNU Make, etc.
#########################################################

install-mkdocs-requirements:
	pip install -r ./requirements.txt

build-mkdocs: clean-demo install-mkdocs-requirements
	mkdocs build

serve-mkdocs: clean install-mkdocs-requirements
	mkdocs serve -v --dev-addr=0.0.0.0:5000

clean:
	rm -rf site/

update-tag:
	git tag -d demo && git push origin :refs/tags/demo
	git tag demo && git push origin demo