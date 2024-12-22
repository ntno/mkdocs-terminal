# Grid Reference
Terminal for MkDocs Tile Grid can be further customized using the following configuration options.  These options should be specified in the markdown page's metadata in the same way that `tiles` are specified:

```markdown
---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    ...
---

# Page Content as usual
```


## Configuration Options


`show_tiles_first`

:   Defaults to `false`.  If `true`, tiles will be added to the final page above the main page content.  If `false` (or unspecified), tiles will be added to the final page below the main content.  
    Ignored if `show_tiles_inline` is `true`.

`show_tiles_inline`

:   Defaults to `false`.  If `true`, tiles will be rendered on the final page using the [Tile Grid Pluglet] (if enabled).

`grid_id`

:   ID to add to the grid's HTML for advanced styling.  
    See [Override Styling] for example.

`grid_css`

:   CSS class to add to the grid's HTML for advanced styling.  
    See [Override Styling] for example.


[Override Styling]: examples/override-styling.md
[Tile Grid Pluglet]: pluglet.md


## Default Tile Placement

See [Example Page]

### Markdown
```markdown
--8<--
tile-grid/examples/example-page.md
--8<--
```


## Tiles First

See [Tiles First Example]

### Markdown
```markdown
--8<--
tile-grid/examples/images-only.md
--8<--

<!-- no closing ``` code block because the snippet page ends in markdown code block -->


[Example Page]: examples/example-page.md
[Tiles First Example]: examples/images-only.md