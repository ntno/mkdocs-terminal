# Theme Features

```yaml
theme:
  name: terminal
  features:
    - navigation.side.indexes
    - navigation.top.search_button.hide
    - revision.date
    - revision.history
```

### navigation.side.indexes  
enables section links in side nav.  
ignored if `navigation.side.hide` is set.  
see [Section Indexes](../navigation/section-indexes.md) for details.  

### navigation.top.search_button.hide
hides the search button in the top nav.  
ignored if `navigation.top.hide` is set. 

### revision.date
enables the "Page last updated..." text at the bottom of the page.  requires [git-revision-date plugin setup].

### revision.history
enables the "See revision history..." text at the bottom of the page.  requires [git-revision-date plugin setup] and additional [git-revision-date configuration].


[git-revision-date plugin setup]: ../plugins/git-revision/
[git-revision-date configuration]: ../plugins/git-revision/#advanced-configuration

# Page Features

To hide certain [Terminal for MkDocs components] on a per-page basis, add a [YAML Style Meta-Data]{target="_blank"} section to the very top of your Markdown page. Inside this metadata section, add the attribute `hide` which is a list of page-specific feature names.

Pay special attention to the indentation. There should be two spaces before the `-` marking the start of a component name: 

```markdown
---
hide:
    - revision_date
    - revision_history
---
```

[YAML Style Meta-Data]: https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data
[Terminal for MkDocs components]: ../#theme-components

### hide: revision_date
hides the "Page last updated" text at the bottom of the page.  ignored if `revision.date` Theme Feature is not enabled.  ignored if `git-revision-date` plugin is not enabled.  

### hide: revision_history
hides the "See revision history..." text at the bottom of the page.  ignored if `revision.history` Theme Feature is not enabled.  ignored if `git-revision-date` plugin is not enabled.  