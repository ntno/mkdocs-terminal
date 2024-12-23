# mkdocs-terminal with PyMdown and Pygments

This example site uses the [Pygments] library and [PyMdown Extensions] to hilight code blocks as they are rendered to HTML during the MkDocs build process.

Please review the Pygments docs for more information on supported programming languages and available styles:

- [Pygments Supported Languages] 
- [Pygments Builtin Styles]

[Pygments]: https://pygments.org/
[PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/
[Pygments Supported Languages]: https://pygments.org/languages/
[Pygments Builtin Styles]: https://pygments.org/styles/

## Set Up
### Install Pygments and PyMdown

Install Pygments (minimum version 2.12) and PyMdown Extensions:

```text
mkdocs
mkdocs-terminal~=4.0

# Python Markdown Extensions
pygments>=2.12
pymdown-extensions
```

### Enable PyMdown Extensions

Enable the pymdownx extensions according to the PyMdown documentation:

- [PyMdown Highlight]
- [PyMdown InlineHilite]

[PyMdown Highlight]: https://facelessuser.github.io/pymdown-extensions/extensions/highlight/
[PyMdown InlineHilite]: https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/

**Note:** for the configuration used in this example site, `pymdownx.superfences` must be enabled.

`mkdocs.yml` excerpt:

```yaml
markdown_extensions:
  - pymdownx.superfences         # required extension
  - pymdownx.highlight:
      use_pygments: true         # use pygments library    
      pygments_style: monokai    # use 'monokai' style
      noclasses: true            # update HTML style attr
  - pymdownx.inlinehilite        # style inline code

theme:
  name: terminal
  palette: dark
```
