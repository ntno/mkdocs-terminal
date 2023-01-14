# Template Blocks

In some situations you may want to include your own Jinja2 page templates.  Terminal for MkDocs supports overriding or extending the blocks listed in [Reference](blocks.md#overridable-blocks).  

This is an advanced MkDocs feature.  For an extended discussion, see the [official MkDocs guide]{target="_blank"}.


[official MkDocs guide]: https://www.mkdocs.org/user-guide/customizing-your-theme/#using-the-theme-custom_dir

## Example Scenario
Let's say you want to add a banner above each page's markdown content.  You still want to be able to show a [Tile Grid] at the top of the page, but you want the banner to appear above the grid if one is defined.
[Tile Grid]: ../tile-grid/index.md


## 1. Add Overrides Folder
Create the following directory structure and add your banner snippet to `banner.html`:

```directory
.
├─ docs/
│  └─ index.md         # Markdown file(s)
├─ overrides/
│  ├─ partials/ 
│  │  ├─ banner.html   # your new snippet
│  │  ├─ main.html     # partial for overriding main theme
│  │  └─ page.html     # partial for extending page content
├─ requirements.txt    # requirements file
└─ mkdocs.yml          # MkDocs config
```


## 2. Add Theme Custom Directory
Configure MkDocs to look at the new `./overrides` folder
```yaml
theme:
  name: terminal
  custom_dir: overrides
```


## 3. Add Extended Partial 
You can add a custom banner above each page's content by adding the following theme extension:

**file name**: page.html  
**file location**: ./overrides/partials/page.html  

```jinja2
{% extends "partials/page-base.html" %}
{%- block before_markdown_content %}
{% include "partials/banner.html" %}
{{ super() }}
{%- endblock %}
```

Calling `super()` will include any Terminal for MkDocs features which are inserted before the main content (like the [Tile Grid] when `show_tiles_first` is set to `true`).
<hr>

# Overridable Blocks

`analytics`

:   Empty block to add analytics integration


`extrahead`

:   Empty block to add custom meta tags


`footer`

:   Contains MkDocs / Terminal for MkDocs credits


`htmltitle`

:   Wraps the `<title>` tag


`before_markdown_content`

:   Section before main markdown content


`markdown_content`

:   Content from page's markdown definition


`after_markdown_content`

:   Section after main markdown content (contains [Tile Grid] by default if `tiles` is set)


`revision`

:   Section after the `after_markdown_content` block containing information about when the markdown page was last updated.  See the [Git Revision plugin] for details.

[Git Revision plugin]: ../plugins/git-revision
<br>

# Override Locations

| Block Name              | Add to `./overrides/partials/` | Extend From `mkdocs-terminal` |
| ----------------------- | ------------------------------ | ----------------------------- |
| analytics               | main.html                      | partials/base.html            |
| extrahead               | main.html                      | partials/base.html            |
| footer                  | main.html                      | partials/base.html            |
| htmltitle               | main.html                      | partials/base.html            |
| before_markdown_content | page.html                      | partials/page-base.html       |
| markdown_content        | page.html                      | partials/page-base.html       |
| after_markdown_content  | page.html                      | partials/page-base.html       |
| revision                | page.html                      | partials/page-base.html       |