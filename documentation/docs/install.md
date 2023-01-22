# Installation

## 1. Setup MkDocs project
See [Getting Started](https://www.mkdocs.org/getting-started/){target="_blank"} for details.

## 2. Install Theme
Install the [mkdocs-terminal pip package](https://pypi.org/project/mkdocs-terminal/){target="_blank"}.  Add the package to your `requirements.txt` file:

```text
mkdocs
mkdocs-terminal
```
Then run:  `pip install -r ./requirements.txt`

## 3. Update MkDocs Configuration
Add the following `theme` configuration in `mkdocs.yml`:
   
```yaml
theme:
  name: terminal
```