# Theme Features
mkdocs.yml:
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
hides table of contents on all site pages.  
see [Page Table of Contents](../configuration/index.md#page-table-of-contents) for more info.  

### navigation.side.hide  
hides side navigation on all site pages.  
see [Side Navigation Menu](../configuration/index.md#side-navigation-menu) for more info.  

### navigation.side.indexes  
enables section links in side nav.  
ignored if `navigation.side.hide` is set.  
see [Section Indexes](../navigation/section-indexes.md) for details.  

### navigation.top.hide  
hides top navigation on all site pages.  
see [Top Navigation Menu](../configuration/index.md#top-navigation-menu) for more info.  

### navigation.top.cursor_animation.hide  
hides the blinking cursor animation in the top nav.  
ignored if `navigation.top.hide` is set.  


# Page Features

To hide certain [Terminal for MkDocs components] on a per-page basis, add a [YAML Style Meta-Data]{target="_blank"} section to the very top of your Markdown page. Inside this metadata section, add the attribute `hide` which is a list of component names.

Pay special attention to the indentation. There should be two spaces before the `-` marking the start of a component name: 

```markdown
---
hide:
  - component_to_hide_on_this_page
---
```

[YAML Style Meta-Data]: https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data
[Terminal for MkDocs components]: ../#theme-components

### hide: git_revision_date
hides the "Page last updated" text at the bottom of the page.  ignored if `revision_date` for the page is not set.  see [Git Revision Date Plugin] for details.

[Git Revision Date Plugin]: plugins/git-revision.md