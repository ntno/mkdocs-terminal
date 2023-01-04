# MkDocs Terminal Theme

This site demonstrates the basic features of the `mkdocs-terminal` MkDocs theme.

## Features

```yaml
theme:
  name: terminal
  features:
    - toc.hide
    - navigation.side.hide
    - navigation.side.indexes
    - navigation.top.hide
    - navigation.top.cursor_animation.hide
```
**toc.hide**  
hides table of contents on all site pages

**navigation.side.hide**  
hides side navigation on all site pages

**navigation.side.indexes**  
enables section links in side nav.  ignored if `navigation.side.hide` is set.

**navigation.top.hide**  
hides top navigation on all site pages

**navigation.top.cursor_animation.hide**  
hides the blinking cursor animation in the top nav.  ignored if `navigation.top.hide` is set.

## Hideable Components
In order to hide components on a per-page basis, you need the meta markdown extension
```mkdocs.yml
markdown_extensions:
  - meta
```
### top-nav
This component includes the `site_name` at the top left and the top level pages as defined in the `nav` section of mkdocs.yml at the top right:

```yaml
site_name: MkDocs Terminal Theme Demo
nav:
    - Home: 'index.md'
    - TOC Example: 'toc.md'
```

### side-nav
This component includes the first through second level pages as defined in the `nav` section of mkdocs.ylm in the left sidebar:

```yaml
nav:
    - Home: 'index.md'
    - TOC Example: 'toc.md'
    - About: 
      - Contributing: 'about/contributing.md'
    - 'User Guide':
      - Configuration: 'user-guide/configuration.md'
      - 'Custom Themes': 'user-guide/custom-themes.md'
      - Deployment: 'user-guide/deploying-your-docs.md'
```

### toc
The table of contents component is located directly underneath the side-nav component.  It includes links to the `h1` and `h2` level sections in the current page's markdown.  See [TOC Example](toc) for detailed example.

