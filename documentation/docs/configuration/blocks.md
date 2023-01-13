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

:   Section after main markdown content (contains Tile Grid by default if `tiles` is set)




| Block Name              | Add Override In    | Extend From             |
| ----------------------- | ------------------ | ----------------------- |
| analytics               | partials/main.html | partials/base.html      |
| extrahead               | partials/main.html | partials/base.html      |
| footer                  | partials/main.html | partials/base.html      |
| htmltitle               | partials/main.html | partials/base.html      |
| before_markdown_content | partials/page.html | partials/page-base.html |
| markdown_content        | partials/page.html | partials/page-base.html |
| after_markdown_content  | partials/page.html | partials/page-base.html |