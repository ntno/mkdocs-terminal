# MkDocs Terminal Theme

This site demonstrates the basic features of the `mkdocs-terminal` MkDocs theme.

## Hideable Components

### top-nav
This component includes the `site_name` at the top left and the top level pages as defined in the `nav` section of mkdocs.yml at the top right:

```mkdocs.yml
site_name: MkDocs Terminal Theme Demo
nav:
    - Home: 'index.md'
    - TOC Example: 'toc.md'
```

### side-nav
This component includes the first through third level pages as defined in the `nav` section of mkdocs.ylm in the left sidebar:

```mkdocs.yml
nav:
    - Home: 'index.md'
    - TOC Example: 'toc.md'
    - '':
      - About: 
        - Contributing: 'about/contributing.md'
      - 'User Guide':
        - Configuration: 'user-guide/configuration.md'
        - 'Custom Themes': 'user-guide/custom-themes.md'
        - Deployment: 'user-guide/deploying-your-docs.md'
```

### toc
The table of contents component is located directly underneath the side-nav component.  It includes links to the `h1` and `h2` level sections in the current page's markdown.  See [TOC Example](toc) for detailed example.

