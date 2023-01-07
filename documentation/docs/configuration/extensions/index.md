[to Python Markdown](python-markdown.md){class='btn btn-primary'}  [to PyMdown Extensions](py-mdown-extensions.md){class='btn btn-primary'}

**Extensions**

Markdown is a very small language with a kind-of reference implementation called
[John Gruber's Markdown]{target="_blank"}. [Python Markdown]{target="_blank"} and [PyMdown Extensions]{target="_blank"} are two packages that enhance the Markdown writing experience, adding useful syntax extensions for technical writing.

  [John Gruber's Markdown]: https://daringfireball.net/projects/markdown/
  [Python Markdown]: https://python-markdown.github.io/extensions/
  [PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

## Supported Extensions

The following extensions are all supported by Terminal for MkDocs and therefore 
strongly recommended. Click on each extension to learn about its purpose and
configuration:

<!-- - [Abbreviations]
- [Admonition]
- [Arithmatex] -->
<!-- - [BetterEm]
- [Caret, Mark & Tilde]
- [Critic] -->
<!-- - [Details]
- [Emoji] -->
<!-- - [Highlight]
- [Keys] -->
<!-- - [SmartSymbols]
- [Snippets]
- [SuperFences]
- [Tabbed] -->
<!-- - [Tasklist] -->


<div markdown>

- [Attribute Lists]
- [Caret, Mark, & Tilde]
- [Definition Lists]
- [Footnotes]
- [Markdown in HTML]
- [Table of Contents]
- [Tables]
  
</div>


  [Attribute Lists]: python-markdown.md#attribute-lists
  [Caret, Mark, & Tilde]: py-mdown-extensions.md#caret-mark-tilde
  [Definition Lists]: python-markdown.md#definition-lists
  [Footnotes]: python-markdown.md#footnotes
  [Markdown in HTML]: python-markdown.md#markdown-in-html
  [Table of Contents]: python-markdown.md#table-of-contents
  [Tables]: python-markdown.md#tables


**Configuration**

Extensions are configured as part of `mkdocs.yml` – the MkDocs configuration
file. The following sections contain two example configurations to bootstrap
your documentation project.

### Minimal Config

This configuration is a good starting point for when you're using Terminal for 
MkDocs for the first time. The best idea is to explore the [supported extensions](#supported-extensions) and gradually add what you want to use:

``` yaml
markdown_extensions:
  # Python Markdown  
  - attr_list
  - md_in_html
  - meta
  - toc:
      permalink: "#"
```

### Recommended Config

This configuration enables all Markdown-related features of Terminal for MkDocs
and is great for experienced users bootstrapping a new documentation project:

``` yaml
markdown_extensions:
  # Python Markdown  
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - meta
  - tables
  - toc:
      permalink: "#"
      permalink_title: Anchor link to this section for reference

  # PyMdown Extensions
  - pymdownx.caret
  - pymdownx.mark
  - pymdownx.tilde
```

# Credit
This documentation is based on squidfunk's Material for MkDocs [Extensions](https://squidfunk.github.io/mkdocs-material/setup/extensions/) documentation.
