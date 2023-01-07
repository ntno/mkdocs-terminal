[Back to Overview](index.md){class='btn btn-default'}  [to PyMdown Extensions](py-mdown-extensions.md){class='btn btn-primary'}

**Python Markdown**

Terminal for MkDocs supports a few of the [Python Markdown]{target="_blank"} extensions. The following is a list of all supported extensions, linking to the relevant sections which explain how they can be used.

  [Python Markdown]: https://python-markdown.github.io/extensions/

## Supported extensions

### Attribute Lists

The [Attribute Lists]{target="_blank"} extension helps to add HTML attributes and CSS classes to [almost every][Attribute Lists limitations]{target="_blank"} Markdown inline- and block-level element with a special syntax. Enable it via `mkdocs.yml`:

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

### Definition Lists

The [Definition Lists]{target="_blank"} extension adds the ability to add definition lists (more
commonly known as [description lists]{target="_blank"} – `dl` in HTML) via Markdown to a
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

### Footnotes

The [Footnotes]{target="_blank"} extension enables inline footnotes which are then
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

### Markdown in HTML

The [Markdown in HTML]{target="_blank"} extension allows for writing Markdown inside of HTML, which is useful for wrapping Markdown content with custom elements. Enable it
via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - md_in_html
```

From the [Markdown in HTML]{target="_blank"} extension's docs:
> By default, Markdown ignores any content within a raw HTML block-level element. With the `md_in_html` extension enabled, the content of a raw HTML block-level element can be parsed as Markdown by including a `markdown` attribute on the opening tag. The `markdown` attribute will be stripped from the output, while all other attributes will be preserved.


No configuration options are available. See reference for usage:

- [Adding Grouped Buttons]
- [Adding Figures]

  [Markdown in HTML]: https://python-markdown.github.io/extensions/md_in_html/
  [Adding Grouped Buttons]: ../../elements/buttons.md#group
  [Adding Figures]: ../../elements/figure.md#example


### Table of Contents

The [Table of Contents]{target="_blank"} extension automatically generates a table of contents from a document, which Terminal for MkDocs will render as part of the resulting page. Enable it via `mkdocs.yml`:

``` yaml
markdown_extensions:
  - toc:
      permalink: true
```

The following configuration options are supported:

[`permalink`](#+toc.permalink){ #+toc.permalink }

:   :octicons-milestone-24: Default: `false` – This option adds an anchor link
    containing the paragraph symbol `¶` or another custom symbol at the end of
    each headline, exactly like on the page you're currently viewing, which
    Material for MkDocs will make appear on hover:

    === "¶"

        ``` yaml
        markdown_extensions:
          - toc:
              permalink: true
        ```

    === "⚓︎"

        ``` yaml
        markdown_extensions:
          - toc:
              permalink: ⚓︎
        ```

[`permalink_title`](#+toc.permalink_title){ #+toc.permalink_title }

:   :octicons-milestone-24: Default: `Permanent link` – This option sets the
    title of the anchor link which is shown on hover and read by screen readers.
    For accessibility reasons, it might be beneficial to change it to a more 
    discernable name, stating that the anchor links to the section itself:

    ``` yaml
    markdown_extensions:
      - toc:
          permalink_title: Anchor link to this section for reference
    ```

[`slugify`](#+toc.slugify){ #+toc.slugify }

:   :octicons-milestone-24: Default: `headerid.slugify` – This option allows for
    customization of the slug function. For some languages, the default may not
    produce good and readable identifiers – consider using another slug function
    like for example those from [Python Markdown Extensions][Slugs]:

    === "Unicode"

        ``` yaml
        markdown_extensions:
          - toc:
              slugify: !!python/object/apply:pymdownx.slugs.slugify
                kwds:
                  case: lower
        ```

    === "Unicode, case-sensitive"

        ``` yaml
        markdown_extensions:
          - toc:
              slugify: !!python/object/apply:pymdownx.slugs.slugify
        ```

[`toc_depth`](#+toc.toc_depth){ #+toc.toc_depth }

:   :octicons-milestone-24: Default: `6` – Define the range of levels to be
    included in the table of contents. This may be useful for project
    documentation with deeply structured headings to decrease the length of the
    table of contents, or to remove the table of contents altogether:

    === "Hide levels 4-6"

        ``` yaml
        markdown_extensions:
          - toc:
              toc_depth: 3
        ```

    === "Hide table of contents"

        ``` yaml
        markdown_extensions:
          - toc:
              toc_depth: 0
        ```

The other configuration options of this extension are not officially supported
by Material for MkDocs, which is why they may yield unexpected results. Use
them at your own risk.

  [Table of Contents]: https://python-markdown.github.io/extensions/toc/
  [Table of Contents support]: https://github.com/squidfunk/mkdocs-material/releases/tag/0.1.0
  [title support]: https://github.com/squidfunk/mkdocs-material/releases/tag/7.3.5
  [site language]: ../changing-the-language.md#site-language
  [Slugs]: https://facelessuser.github.io/pymdown-extensions/extras/slugs/

### Tables

[:octicons-tag-24: 0.1.0][Tables support] ·
[:octicons-workflow-24: Extension][Tables]

The [Tables] extension adds the ability to create tables in Markdown by using a 
simple syntax. Enable it via `mkdocs.yml` (albeit it should be enabled by
default):

``` yaml
markdown_extensions:
  - tables
```

No configuration options are available. See reference for usage:

- [Using data tables]
- [Column alignment]

  [Tables]: https://python-markdown.github.io/extensions/tables/
  [Tables support]: https://github.com/squidfunk/mkdocs-material/releases/tag/0.1.0
  [Using data tables]: ../../reference/data-tables.md#usage
  [Column alignment]: ../../reference/data-tables.md#column-alignment

## Superseded extensions

The following [Python Markdown] extensions are not (or might not be) supported 
anymore, and are therefore not recommended for use. Instead, the alternatives
should be considered.

### Fenced Code Blocks

[:octicons-tag-24: 0.1.0][Fenced Code Blocks support] ·
[:octicons-workflow-24: Extension][Fenced Code Blocks]

Superseded by [SuperFences]. This extension might still work, but the
[SuperFences] extension is superior in many ways, as it allows for arbitrary 
nesting, and is therefore recommended.

  [Fenced Code Blocks]: https://python-markdown.github.io/extensions/fenced_code_blocks/
  [Fenced Code Blocks support]: https://github.com/squidfunk/mkdocs-material/releases/tag/0.1.0
  [SuperFences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/

### CodeHilite

[:octicons-tag-24: 0.1.0 ... 5.5.14][CodeHilite support] ·
[:octicons-workflow-24: Extension][CodeHilite]

Superseded by [Highlight]. Support for CodeHilite was dropped in
:octicons-tag-24: 6.0.0, as [Highlight] has a better integration with other 
essential extensions like [SuperFences] and [InlineHilite].

  [CodeHilite]: https://python-markdown.github.io/extensions/code_hilite/
  [CodeHilite support]: https://github.com/squidfunk/mkdocs-material/releases/tag/0.1.0
  [Highlight]: https://facelessuser.github.io/pymdown-extensions/extensions/highlight/
  [InlineHilite]: https://facelessuser.github.io/pymdown-extensions/extensions/inlinehilite/

# Credit
This documentation is based on squidfunk's Material for MkDocs [Python Markdown](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/) documentation.

