# Theme Components

The MkDocs Terminal theme layout consists of three major components.  The top navigation bar, the side navigation bar, and the page table of contents.  Each of these components can be hidden site-wide (see [Theme Features](./features.md)), however they are enabled by default.

<figure markdown>
![UI Components](../img/annotated/hideable_components.png){alt="top navigation menu and side navigation menu annotated.  Page table of contents appears below side navigation menu." .terminal-mkdocs-thin-border }
<figcaption markdown>*Top Nav*, *Side Nav*, and *Table of Contents* are enabled by default</figcaption>
</figure>

## Top Navigation Menu

The top navigation menu includes the `site_name` at the top left and root level pages at the top right.  Root level pages are pages which are not child pages and are not a section index:

<figure markdown>
```yaml
site_name: Terminal Theme Demo
nav:
    - Home: 'index.md'
    - Troubleshooting: 'help.md'
```
<figcaption markdown>*Home* and *Troubleshooting* appear in the top navigation menu</figcaption>
</figure>

## Side Navigation Menu

The navigation menu in the left sidebar includes the root level and second level pages as defined in the `nav` section of `mkdocs.yml`:

<figure markdown>
```yaml
nav:
    - Home: 'index.md'
    - Troubleshooting: 'help.md'
    - About: 
      - Index: 'about/index.md'
      - Contributing: 'about/contributing.md'
      - License: 'about/license.md'
      - Release Notes:
        - Index: 'about/release-notes/index.md'
        - v1: 'about/release-notes/version-1.md'
        - v2: 'about/release-notes/version-2.md'
```
<figcaption markdown>*Home*, *Troubleshooting*, *About*, *Contributing*, *License*, and *Release Notes* appear in the side navigation menu</figcaption>
</figure>

## Page Table of Contents

The table of contents (TOC) is located directly underneath the side navigation menu.  It includes links to the the top two sections in the current page's markdown.  See [TOC Example](../navigation/toc.md) for details.



