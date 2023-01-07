[Back to Overview](index.md){class='btn btn-default'}  [to Python Markdown](python-markdown.md){class='btn btn-primary'}

**PyMdown Extensions**

The [PyMdown Extensions]{target="_blank"} package is an excellent collection of
additional extensions perfectly suited for advanced technical writing. Terminal
for MkDocs lists this package as an explicit dependency so it's automatically
installed with a supported version.

  [PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

## Supported extensions

### Caret, Mark & Tilde

The [Caret], [Mark] and [Tilde] extensions add the ability to highlight text
and define subscript and superscript using a simple syntax. Enable them together
via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - pymdownx.caret
  - pymdownx.mark
  - pymdownx.tilde
```

The configuration options of this extension are not specific to Terminal for
MkDocs, as they only impact the Markdown parsing stage. 

See reference for usage:

- [Adding Superscript Styling]
- [Adding Subscript Styling]
- [Adding Strikethrough Styling]
- [Adding Marks]

  [Adding Marks]: ../../../elements/typography/#marks
  [Adding Superscript Styling]: ../../../elements/typography/#superscript
  [Adding Subscript Styling]: ../../../elements/typography/#subscript
  [Adding Strikethrough Styling]: ../../../elements/typography/#strikethrough