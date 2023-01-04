
# Setup MkDocs project
See [Getting Started](https://www.mkdocs.org/getting-started/) for details.

## Install Theme
Install package with pip.  Add the `mkdocs-terminal` package to your requirements file.

```requirements.txt
mkdocs
mkdocs-terminal
```
Then run:  `pip install -r ./requirements.txt`

## Update MkDocs Configuration
Add `theme` configuration in `mkdocs.yml`
   
```mkdocs.yml
theme:
   name: terminal
   features:
      - navigation.top.terminal_prompt
```