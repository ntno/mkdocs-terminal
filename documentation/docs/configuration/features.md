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
    - revision.date
    - revision.source
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
enables the "Page last updated REVISION_DATE" text at the bottom of the page (assuming `revision_date` is available in the page's metadata[^revision_date_available])

### revision.source
enables the "See revision history on [GitHub]({{page.edit_url}})" text at the bottom of the page.  

MkDocs requires you to configure `repo_url`[^repo_url] and `edit_uri_template`[^edit_uri_template] to generate an accurate `page.edit_url`[^edit_url].  Terminal for MkDocs uses `page.edit_url` to create a page-specific link to the markdown page so make sure to validate that the generated link works as expected.  You may need to tweak your project settings if your `docs/` folder is not at the root of your repository.

This feature requires that the `page.edit_url`[^edit_url] attribute is set on the MkDocs page object.  


[^revision_date_available]: to automatically add `revision_date` metadata, enable the [Git Revision Date Plugin]
[^repo_url]: See `project.repo_url` on MkDocs: [mkdocs.configuration.repo_url]{target="_blank"}
[^edit_uri_template]: See `project.edit_uri_template` on MkDocs: [mkdocs.configuration.edit_uri_template]{target="_blank"}
[^edit_url]: See `page.edit_url` on MkDocs: [mkdocs.structure.pages.Page.edit_url]{target="_blank"}

[^project_information]: See project information config on MkDocs: [mkdocs.configuration.project-information]{target="_blank"}

[Git Revision Date Plugin]: plugins/git-revision.md
[mkdocs.structure.pages.Page.edit_url]: https://www.mkdocs.org/dev-guide/themes/#mkdocs.structure.pages.Page.edit_url
[mkdocs.configuration.project-information]: https://www.mkdocs.org/user-guide/configuration/#project-information
[mkdocs.configuration.repo_url]: https://www.mkdocs.org/user-guide/configuration/#repo_url
[mkdocs.configuration.edit_uri_template]: https://www.mkdocs.org/user-guide/configuration/#edit_uri_template

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

