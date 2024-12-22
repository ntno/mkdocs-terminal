# mkdocs-terminal with pymdownx highlight and pygments

TODO - explain what pymdownx Markdown extension and pygments library do

- https://pygments.org/languages/
- https://pygments.org/styles/

## Set Up
### Install TODO

TODO

### Enable TODO

TODO


`mkdocs.yml` excerpt:

```yaml
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.highlight:
      use_pygments: true
      pygments_style: default
      noclasses: true

theme:
  name: terminal
```
