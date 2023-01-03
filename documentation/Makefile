#########################################################
## run from machine or container with required software
## python, pip, GNU Make, etc.
#########################################################

install-mkdocs-requirements:
	pip install -r ./requirements.txt

build-mkdocs: clean-demo install-mkdocs-requirements
	mkdocs build

serve-mkdocs: clean install-mkdocs-requirements
	mkdocs serve -v --dev-addr=0.0.0.0:8080

clean:
	rm -rf site/

update-tag:
	git tag -d documentation && git push origin :refs/tags/documentation
	git tag documentation && git push origin documentation