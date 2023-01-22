[Back to Overview](index.md){class='btn btn-default'}  [to Python Markdown](python-markdown.md){class='btn btn-primary'}

# PyMdown Extensions

The [PyMdown Extensions]{target="_blank"} package is an excellent collection of
additional extensions perfectly suited for advanced technical writing. Terminal
for MkDocs lists this package as an explicit dependency so it's automatically
installed with a supported version.

  [PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

# Suggested PyMdown Extensions

## Caret, Mark & Tilde

The [Caret]{target="_blank"}, [Mark]{target="_blank"} and [Tilde]{target="_blank"} extensions add the ability to highlight text
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
  [Caret]: https://facelessuser.github.io/pymdown-extensions/extensions/caret/
  [Mark]: https://facelessuser.github.io/pymdown-extensions/extensions/mark/
  [Tilde]: https://facelessuser.github.io/pymdown-extensions/extensions/tilde/


## Snippets

The [Snippets]{target="_blank"} extension adds the ability to embed content from arbitrary files into a document, including other documents or source files, by using a simple syntax. Enable it via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - pymdownx.snippets
```

The configuration options of this extension are not specific to Terminal for
MkDocs, as they only impact the Markdown parsing stage. See the [Snippets 
documentation][Snippets]{target="_blank"} for more information.

  [Snippets]: https://facelessuser.github.io/pymdown-extensions/extensions/snippets/
  
See reference for usage:

- [Adding Snippets]

  [Adding Snippets]: ./snippets.md


# Credit

This documentation is based on squidfunk's Material for MkDocs [Pymdown Extension](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/){target="_blank"} documentation.
