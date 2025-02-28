--8<--
configuration/extensions/links.md
--8<--

# PyMdown Extensions

The [PyMdown Extensions] package is an excellent collection of extensions suited for advanced technical writing. Terminal for MkDocs lists this package as an explicit dependency so it's automatically installed with a supported version.

  [PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

# Suggested PyMdown Extensions

## Caret, Mark & Tilde

The [Caret], [Mark], and [Tilde] extensions add the ability to highlight text
and define subscript and superscript using a simple syntax. Enable them together
via `mkdocs.yml`:

```yaml
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

The [Snippets] extension adds the ability to embed content from arbitrary files into a document, including other documents or source files, by using a simple syntax. Enable it via `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.snippets
```

The configuration options of this extension are not specific to Terminal for
MkDocs, as they only impact the Markdown parsing stage. See the [Snippets 
documentation][Snippets] for more information.

  [Snippets]: https://facelessuser.github.io/pymdown-extensions/extensions/snippets/
  
See reference for usage:

- [Adding Snippets]

  [Adding Snippets]: ./snippets.md

## SuperFences

The [SuperFences] extension allows fenced blocks to be nested inside block quotes, lists, or other block elements.  Enable it via `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.superfences
```

This extension is incompatible with the Python Markdown extension `markdown.extensions.fenced_code`.

  [SuperFences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/

## Highlight and InlineHilite

The [Highlight] and [InlineHilite] extensions can be used to highlight code blocks.  If used with the [PyMdown SuperFences](#superfences) extension line numbers can be added as well.  Enable them via `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.highlight
  - pymdownx.inlinehilite
```

See reference for recommended configuration options:

- [Code Highlighting > PyMdown and Pygments](../code-highlighting/index.md#pymdown-and-pygments)

  [Highlight]: https://facelessuser.github.io/pymdown-extensions/extensions/highlight/
  [InlineHilite]: https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/

## Details

The [Details] extension can be used to create admonitions (sometimes called callouts). By default, Terminal for Mkdocs supports three categories. Enable them via `mkdocs.yml`:

/// info
This is an info block
///

/// warning
This is a warning
///

/// important
This is important
///

```yaml
markdown_extensions:
  - pymdownx.blocks.details:
      types:
        - name: info 
          class: terminal-alert
          title: Info
        - name: warning
          class: 'terminal-alert terminal-alert-error'
          title: Warning
        - name: important
          class: 'terminal-alert terminal-alert-primary'
          title: Important
```

* To use different categories, update the `name` attribute.
* To use a custom style, update the `class` attribute to the name of your custom CSS class (remember to load the custom CSS via the [extra_css MkDocs feature]).
  [Details]: https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/details/
  [extra_css MkDocs feature]: https://www.mkdocs.org/user-guide/configuration/#extra_css

# Credit

This documentation page is based on squidfunk's [Material for MkDocs Pymdown Extension](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/) documentation.
