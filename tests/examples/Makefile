#########################################################
## run from machine or container with required software
## python, pip, GNU Make, etc.
#########################################################
upgrade-pip: check-site
	cd $(site) && \
	python3 -m pip install --upgrade pip

install-requirements: check-site upgrade-pip
	cd $(site) && \
	pip install -r ./requirements.txt

build: check-site clean install-requirements
	cd $(site) && \
	mkdocs build -v

serve: check-site clean build
	cd $(site) && \
	mkdocs serve -v --dev-addr=0.0.0.0:5000

clean: check-site
	cd $(site) && \
	rm -rf site/

update-tag: check-site
	git tag -d $(site) && git push origin :refs/tags/$(site)
	git tag $(site) && git push origin $(site)


check-site:
ifndef site
	$(error site is not set)
endif