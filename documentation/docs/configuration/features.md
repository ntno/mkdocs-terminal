# Theme Features

```yaml
theme:
  name: terminal
  features:
    - navigation.side.hide
    - navigation.side.indexes
    - navigation.side.prev_next
    - navigation.side.toc.hide
    - navigation.top.hide
    - navigation.top.cursor_animation.hide
    - navigation.top.search_button.hide
    - revision.date
    - revision.history
    - style.links.underline.hide
```

## navigation.side.hide  
Hides the side navigation menu and page table of contents on all site pages.

## navigation.side.indexes  
Enables section links in the side navigation menu.  
Ignored if `navigation.side.hide` is set.  
See [Section Indexes](../navigation/section-indexes.md) for details.  

## navigation.side.toc.hide  
Hides page table of contents on all site pages.  
Ignored if `navigation.side.hide` is set.  
See [Page Table of Contents](../configuration/index.md#page-table-of-contents) for more info. 

## navigation.top.hide  
Hides top navigation menu on all site pages.  
See [Top Navigation Menu](../configuration/index.md#top-navigation-menu) for more info.  

## navigation.top.cursor_animation.hide  
Hides the blinking cursor animation in the top navigation menu.  
Ignored if `navigation.top.hide` is set.  

## navigation.top.search_button.hide
Hides the search button in the top navigation menu.  
Ignored if `navigation.top.hide` is set.  

## revision.date
Enables the "Page last updated..." text at the bottom of each site page.  Requires [git-revision-date plugin setup].

## revision.history
Enables the "See revision history..." text at the bottom of each site page.  Requires [git-revision-date plugin setup] and additional [git-revision-date configuration].

## style.links.underline.hide
Hides the underline styling on links.  The underline text decoration on links is added to make links identifiable without color vision.  If you choose to hide this styling you should consider adding an alternate [non-color link indicator].    

[git-revision-date plugin setup]: ../plugins/git-revision/
[git-revision-date configuration]: ../plugins/git-revision/#advanced-configuration
[non-color link indicator]: https://www.w3.org/WAI/WCAG21/Techniques/general/G182.html
<hr>

# Page Features

To hide certain Terminal for MkDocs components on a per-page basis, add a [YAML Style Meta-Data] section to the very top of your Markdown page. Inside this metadata section, add the attribute `hide` which is a list of page-specific feature names.

Pay special attention to the indentation. There should be two spaces before the `-` marking the start of a component name: 

```markdown
---
hide:
    - revision_date
    - revision_history
    - side_toc
    - top_nav
---
```

[YAML Style Meta-Data]: https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data

## hide: revision_date
Hides the "Page last updated" text at the bottom of the page.  
Ignored if `revision.date` Theme Feature is not enabled.  
Ignored if `git-revision-date` plugin is not enabled.  

## hide: revision_history
Hides the "See revision history..." text at the bottom of the page.  
Ignored if `revision.history` Theme Feature is not enabled.  
Ignored if `git-revision-date` plugin is not enabled.  

## hide: side_toc
Hides the table of contents in the side panel on the page.

## hide: top_nav
Hides the top navigation menu on the page.  