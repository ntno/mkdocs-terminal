--8<--
configuration/extensions/links.md
--8<--

# Python Markdown

Terminal for MkDocs is compatible with some of the [Python Markdown] extensions. The following is a list of all extensions which have been tested with this theme, linking to documentation which explain how they can be used.

  [Python Markdown]: https://python-markdown.github.io/extensions/

# Suggested Python Markdown Extensions

## Attribute Lists

The [Attribute Lists] extension helps to add HTML attributes and CSS classes to [almost every][Attribute Lists limitations] Markdown inline- and block-level element with a special syntax. Enable it via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - attr_list
```

No configuration options are available. See reference for usage:

- [Adding buttons]
- [Adding tooltips]
- [Adding link target]

  [Attribute Lists]: https://python-markdown.github.io/extensions/attr_list/
  [Attribute Lists limitations]: https://python-markdown.github.io/extensions/attr_list/#limitations
  [Adding buttons]: ../../elements/buttons.md#default
  [Adding tooltips]: ../../elements/tooltips.md#example
  [Adding link target]: ../../elements/links.md#enhanced-example

## Definition Lists

The [Definition Lists] extension adds the ability to add definition lists (more
commonly known as [description lists] – `dl` in HTML) via Markdown to a
document. Enable it via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - def_list
```

No configuration options are available. See reference for usage:

- [Using definition lists]

  [Definition Lists]: https://python-markdown.github.io/extensions/definition_lists/
  [description lists]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dl
  [Using definition lists]: ../../elements/definitions.md#example

## Footnotes

The [Footnotes] extension enables inline footnotes which are then
rendered below all Markdown content of a document. Enable it via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - footnotes
```

No configuration options are supported. See reference for usage:

- [Adding footnote markers]
- [Adding footnote content]

  [Footnotes]: https://python-markdown.github.io/extensions/footnotes/
  [Adding footnote markers]: ../../elements/footnotes.md#example-footnote-marker
  [Adding footnote content]: ../../elements/footnotes.md#example-footnote-content

## Markdown in HTML

The [Markdown in HTML] extension allows for writing Markdown inside of HTML, which is useful for wrapping Markdown content with custom elements. Enable it
via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - md_in_html
```

From the [Markdown in HTML] extension's docs:
> By default, Markdown ignores any content within a raw HTML block-level element. With the `md_in_html` extension enabled, the content of a raw HTML block-level element can be parsed as Markdown by including a `markdown` attribute on the opening tag. The `markdown` attribute will be stripped from the output, while all other attributes will be preserved.


No configuration options are available. See reference for usage:

- [Adding Grouped Buttons]
- [Adding Figures]

  [Markdown in HTML]: https://python-markdown.github.io/extensions/md_in_html/
  [Adding Grouped Buttons]: ../../elements/buttons.md#group
  [Adding Figures]: ../../elements/figure.md#example


## Table of Contents

The [Table of Contents] extension automatically generates a table of contents from a document which Terminal for MkDocs will render as part of the resulting page. It can be configured via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - toc:
      permalink: "#"
```

The following configuration options are supported:

`permalink`
:   
    **Default**: `false`

    This option adds an anchor link containing the paragraph symbol (if `true`) or another custom symbol at the end of each headline, exactly like on the page you're currently viewing.


`permalink_title`

:   **Default**: `Permanent link`

    This option sets the title of the anchor link which is shown on hover and read by screen readers.  For accessibility reasons, it might be beneficial to change it to a more discernable name, stating that the anchor links to the section itself.  Ex: `Anchor link to this section for reference`


`toc_depth`

:   **Default**: `6` 

    Defines the range of levels to be included in the table of contents. This may be useful for project documentation with deeply structured headings to decrease the length of the table of contents, or to remove the table of contents altogether.  See [Table of Contents Example] for further discussion.

`baselevel`

:   **Default**: `1` 

    Base level for headers.  See [Table of Contents Example] for further discussion.

`anchorlink`

:   **Default**: `false`
  
    Set to `true` to render all headers as links to themselves.

The other configuration options of this extension are not officially supported
by Terminal for MkDocs, which is why they may yield unexpected results. Use
them at your own risk.

See reference for usage:

- [Table of Contents Example]

  [Table of Contents]: https://python-markdown.github.io/extensions/toc/
  [Table of Contents Example]: ../../navigation/toc.md


## Tables

The [Tables] extension adds the ability to create tables in Markdown by using a simple syntax. Enable it via `mkdocs.yml` (albeit it should be enabled by
default):

``` yaml
markdown_extensions:
  - tables
```

No configuration options are available. See reference for usage:

- [Adding tables]


  [Tables]: https://python-markdown.github.io/extensions/tables/
  [Adding tables]: ../../elements/table.md#example


# Credit

This documentation page is based on squidfunk's Material for MkDocs [Python Markdown](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/) documentation.

