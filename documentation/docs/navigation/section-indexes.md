# Section Indexes

When the section index theme feature is enabled, documents can be directly attached to sections.  This is particularly useful for providing overview pages. 

## Example Scenario
Let's say you have a site with *Release Notes* and *About* documents.  The *Release Notes* documents are a subsection of the *About* section.  Both sections contain an overview page:

<figure markdown>
```directory
.
├─ docs/
│  ├─ about/
│  │  ├─ release-notes/
│  │  │  ├─ index.md          # Release Notes Overview
│  │  │  ├─ version-1.md
│  │  │  └─ version-2.md
│  │  ├─ index.md             # About Overview
│  │  ├─ license.md
│  │  └─ contributing.md
│  ├─ index.md                # Home
│  └─ help.md
├─ requirements.txt
└─ mkdocs.yml
```
<figcaption markdown>The *Release Notes* section is inside the *About* section.<br>Each section has an overview page.</figcaption>
</figure>

## With Section Indexes Feature
*About* and *Release Notes* are clickable in the side navigation.  The index page for the *About* section does not appear as a subpage of the *About* category:

![section index pages enabled](../img/about_page_with_section_indexes.png){alt="'Release Notes' is rendered as a clickable link in the side navigation" .terminal-mkdocs-thin-border}

## Without Section Indexes Feature
*About* and *Release Notes* are not clickable in the side navigation.  Instead, they are rendered as greyed out text.  The index page for the *About* section appears as a subpage of the *About* category:

![section index pages enabled](../img/about_page_without_section_indexes.png){alt="'Release Notes' is rendered as greyed out text in the side navigation" .terminal-mkdocs-thin-border}


## Setup
1. Add the `navigation.side.indexes` feature to the theme configuration in `mkdocs.yml`:

        
        theme:
          name: terminal
          features:
            - navigation.side.indexes
        

2. Add a page with the title 'Index' as a subpage in the `nav` config in `mkdocs.yml`:

      <figure markdown>


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

      <figcaption markdown>Use the page title 'Index' for section indexes.</figcaption>
      </figure>


