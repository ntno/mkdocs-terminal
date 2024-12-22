# mkdocs-terminal with pymdownx and pygments

TODO - explain what pymdownx Markdown extension and pygments library do

- https://pygments.org/languages/
- https://pygments.org/styles/

## Set Up
### Install Required Extensions and Libraries

Install [Pygments] (at a minimum version 2.12) and [PyMdown Extensions]:

```text
mkdocs
mkdocs-terminal~=4.0

# Python Markdown Extensions
pygments>=2.12
pymdown-extensions
```
[Pygments]: https://pygments.org/
[PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

### Enable Extensions

Enable the pymdownx extensions according to the PyMdown documentation:

- [PyMdown Highlight]
- [PyMdown InlineHilite]

[PyMdown Highlight]: https://facelessuser.github.io/pymdown-extensions/extensions/highlight/
[PyMdown InlineHilite]: https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/

Note for the configuration used in this example, `pymdownx.superfences` must be enabled.

`mkdocs.yml` excerpt:

```yaml
markdown_extensions:
  - pymdownx.superfences         # required extension
  - pymdownx.highlight:
      use_pygments: true         # use pygments library    
      pygments_style: default    # use 'default' style
      noclasses: true            # update HTML style attr
  - pymdownx.inlinehilite        # style inline code

theme:
  name: terminal
```
