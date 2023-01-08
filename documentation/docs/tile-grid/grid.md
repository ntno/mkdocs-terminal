# Grid Reference
Terminal for MkDocs [Tile Grid](index.md){title="to Tile Grid overview"} can be further customized using the following configuration options.  These options should be specified in the markdown page's metadata in the same way that `tiles` are specified:

```
---
show_tiles_first: true
tiles:
  - caption: '@petradr'
    ...
---

# Page Content as usual
```

<br>

## Configuration Options


`show_tiles_first`

:   Defaults to `false`.  If `true`, tiles will be added to the final page above the main page content.  If `false` (or unspecified), tiles will be added to the final page below the main content.

<br>

## Default Tile Placement

See [Example Page]{target="_blank", title="open default grid example in new tab"}

**Markdown**:
```markdown
--8<--
tile-grid/examples/example-page.md
--8<--
```

<br>

## Tiles First

See [Tiles First example]{target="_blank", title="open tiles first example in new tab"}

**Markdown**:
```markdown
--8<--
tile-grid/examples/images-only.md
--8<--

<!-- no closing ``` because the snippet page ends in markdown -->


[Example Page]: examples/example-page.md
[Tiles First example]: examples/images-only.md