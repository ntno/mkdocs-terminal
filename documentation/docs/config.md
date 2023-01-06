## Theme Components

The MkDocs Terminal theme layout consists of three major components.  The top navigation bar, the side navigation bar, and the page table of contents.  Each of these components can be hidden site-wide, however they are enabled by default.

![Major UI Components](img/annotated/hideable_components.png){title="Major UI Components", "screenshot with hideable MkDocs Terminal components annotated"}


### Top Navigation Menu

This component includes the `site_name` at the top left and the top level pages as defined in the `nav` section of `mkdocs.yml` at the top right:

```yaml
site_name: Terminal Theme Demo
nav:
    - Home: 'index.md'
    - Troubleshooting: 'help.md'
```

### Side Navigation Menu

This component includes the first through second level pages as defined in the `nav` section of `mkdocs.yml` in the left sidebar:

```yaml
nav:
    - Home: 'index.md'
    - Troubleshooting: 'help.md'
    - About: 
      - Contributing: 'about/contributing.md'
      - License: 'about/license.md'
      - Release Notes:
        - v1: 'about/release-notes/version-1.md'
        - v2: 'about/release-notes/version-2.md'
```

### Page Table of Contents

The table of contents component is located directly underneath the side-nav component.  It includes links to the the top two sections in the current page's markdown.  See [TOC Example](./navigation/toc.md) for details.



# Theme Features

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

