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

# note the single quotes and \` to escape a backtick
highlightjs_string='Language highlighting can be enabled with \`highlight.js\` by adding a [supported programming language](https://highlightjs.readthedocs.io/en/latest/supported-languages.html) name directly after the first <code>\`\`\`</code> grouping in a Markdown code block'
pymdownx_string='Language highlighting can be enabled with \`pymdownx\` by adding a [supported programming language](https://pygments.org/languages/) name directly after the first <code>\`\`\`</code> grouping in a Markdown code block'

update-code-highlight-example: check-site check-method-regex
	cp -r template-code-markdown-docs/docs/ $(site)/docs/
	find $(site)/docs/ -type f -print0 | xargs -0 sed -i '' "s#HIGHLIGHTING_METHOD_PLACEHOLDER#$(method-regex)#g"

update-all-highlight-examples: 
	$(MAKE) update-code-highlight-example site=pymdown-pygments method-regex=$(pymdownx_string)
	$(MAKE) update-code-highlight-example site=highlightjs method-regex=$(highlightjs_string)
	$(MAKE) update-code-highlight-example site=highlightjs-dark method-regex=$(highlightjs_string)

check-method-regex:
ifndef site
	$(error method-regex is not set)
endif

check-site:
ifndef site
	$(error site is not set)
endif