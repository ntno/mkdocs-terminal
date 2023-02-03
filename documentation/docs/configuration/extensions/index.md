--8<--
configuration/extensions/links.md
--8<--

# Extensions

Markdown is a very small language with a kind-of reference implementation called
[John Gruber's Markdown]. Python Markdown and PyMdown Extensions are two packages that enhance the Markdown writing experience, adding useful syntax extensions for technical writing.

[John Gruber's Markdown]: https://daringfireball.net/projects/markdown/

## Suggested Extensions

The following extensions have been confirmed to work with Terminal for MkDocs and are recommended:

<div markdown>

- [Attribute Lists]
- [Caret, Mark, & Tilde]
- [Definition Lists]
- [Footnotes]
- [Markdown in HTML]
- [Snippets]
- [Table of Contents]
- [Tables]
  
</div>


  [Attribute Lists]: python-markdown.md#attribute-lists
  [Caret, Mark, & Tilde]: pymdown-extensions.md#caret-mark-tilde
  [Definition Lists]: python-markdown.md#definition-lists
  [Footnotes]: python-markdown.md#footnotes
  [Markdown in HTML]: python-markdown.md#markdown-in-html
  [Snippets]: pymdown-extensions.md#snippets
  [Table of Contents]: python-markdown.md#table-of-contents
  [Tables]: python-markdown.md#tables


# Configuration

Extensions are enabled in the MkDocs configuration file.  See below for two example configurations to bootstrap your documentation project.

## Minimal Config

The minimal configuration is a good starting point for when you're using MkDocs for the first time.  You can explore the suggested extensions and gradually add extensions as needed:

``` yaml
markdown_extensions:
  # Python Markdown  
  - attr_list
  - md_in_html
  - meta
  - toc:
      permalink: "#"
```

## Recommended Config

The recommended configuration enables all Markdown-related features of Terminal for MkDocs
and is great for experienced users bootstrapping a new documentation project:

``` yaml
markdown_extensions:
  # Python Markdown  
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - meta
  - toc:
      permalink: "#"
      permalink_title: Anchor link to this section for reference

  # PyMdown Extensions
  - pymdownx.caret
  - pymdownx.mark
  - pymdownx.tilde
  - pymdownx.snippets:
      base_path: 
        - docs
```

# Credit
This documentation page is based on squidfunk's [Material for MkDocs Extensions](https://squidfunk.github.io/mkdocs-material/setup/extensions/) documentation.
