# Template Blocks

In some situations you may want to include your own Jinja2 page templates.  Terminal for MkDocs supports overriding or extending the blocks listed in [Overridable Blocks](blocks.md#overridable-blocks).  

This is an advanced MkDocs feature.  For an extended discussion, see the [official MkDocs guide].

[official MkDocs guide]: https://www.mkdocs.org/user-guide/customizing-your-theme/#overriding-template-blocks


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
│  │  └─ page.html     # partial for extending page content
│  └─ main.html        # partial for overriding main theme
├─ requirements.txt    # requirements file
└─ mkdocs.yml          # MkDocs config
```


## 2. Add Theme Custom Directory
Configure MkDocs to look at the new `./overrides` folder:

**file name**: mkdocs.yml  
**file location**: ./
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
{% raw %}
{% extends "partials/page-base.html" %}

{%- block before_markdown_content %}
{% include "partials/banner.html" %}
{{ super() }}
{%- endblock before_markdown_content %}
{% endraw %}
```

If you wanted to override higher level blocks[^block-levels] you would add them in `main.html`: 

[^block-levels]: See [Override Locations](blocks.md#override-locations) for details on where each block can be overriden from.

**file name**: main.html  
**file location**: ./overrides/main.html  

```jinja2
{% raw %}
{% extends "base.html" %}
{% endraw %}
```

Calling `super()` will include any Terminal for MkDocs features which are inside the original block definition.
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


`search`

:   Wraps the built-in Search Plugin CSS/JS support


`search_modal`

:   Wraps the built-in Search modal


`site_lang`

:   Wraps the HTML language attribute


`before_markdown_content`

:   Section before main markdown content


`markdown_content`

:   Content from page's markdown definition


`after_markdown_content`

:   Section after main markdown content (contains [Tile Grid] by default if `tiles` is set)


`revision`

:   Section after the `after_markdown_content` block containing information about when the markdown page was last updated.  See the [Git Revision Plugin] for details.

[Git Revision Plugin]: ../plugins/git-revision


# Override Locations

| Block Name              | Add to `./overrides/` | Extend From `mkdocs-terminal` |
| ----------------------- | --------------------- | ----------------------------- |
| analytics               | main.html             | base.html                     |
| extrahead               | main.html             | base.html                     |
| footer                  | main.html             | base.html                     |
| htmltitle               | main.html             | base.html                     |
| search                  | main.html             | base.html                     |
| search_modal            | main.html             | base.html                     |
| site_lang               | main.html             | base.html                     |
| before_markdown_content | partials/page.html    | partials/page-base.html       |
| markdown_content        | partials/page.html    | partials/page-base.html       |
| after_markdown_content  | partials/page.html    | partials/page-base.html       |
| revision                | partials/page.html    | partials/page-base.html       |