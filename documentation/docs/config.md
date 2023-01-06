# Theme Configuration

## Hideable Components

### Top Navigation Menu

This component includes the `site_name` at the top left and the top level pages as defined in the `nav` section of mkdocs.yml at the top right:

```yaml
site_name: MkDocs Terminal Theme Demo
nav:
    - Home: 'index.md'
    - TOC Example: 'toc.md'
```

### Side Navigation Menu

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

### Page Table of Contents

The table of contents component is located directly underneath the side-nav component.  It includes links to the `h1` and `h2` level sections in the current page's markdown.  See [TOC Example](./navigation/toc.md) for detailed example.



# Features

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
## Details

### toc.hide  
hides table of contents on all site pages

### navigation.side.hide  
hides side navigation on all site pages

### navigation.side.indexes  
enables section links in side nav.  ignored if `navigation.side.hide` is set.

### navigation.top.hide  
hides top navigation on all site pages

### navigation.top.cursor_animation.hide  
hides the blinking cursor animation in the top nav.  ignored if `navigation.top.hide` is set.

#### wow another one