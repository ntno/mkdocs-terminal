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
    - revision.date
    - revision.history
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

### revision.date
enables the "Page last updated..." text at the bottom of the page.  requires [git-revision-date plugin setup].

### revision.history
enables the "See revision history..." text at the bottom of the page.  requires [git-revision-date plugin setup].


[git-revision-date plugin setup]: plugins/git-revision


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

### hide: revision_date
hides the "Page last updated" text at the bottom of the page.  ignored if `revision.date` Theme Feature is not enabled.  ignored if `git-revision-date` plugin is not enabled.  

### hide: revision_history
hides the "See revision history..." text at the bottom of the page.  ignored if `revision.history` Theme Feature is not enabled.  ignored if `git-revision-date` plugin is not enabled.  