---
show_tiles_first: true
grid_id: "grid_123"
grid_css: "example_dashed_border"
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    alt_text: 'close up of fallen leaves.'
    tile_css: 'override_tile'
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    alt_text: 'close up of green moss on a log.'
    tile_css: 'override_tile'
  - caption: '@Guillaume'
    img_src: ../../../img/picsum/120_small.jpg
    alt_text: 'milky way with a rustic picket fence in the foreground'
    tile_css: 'override_tile'
---

<style> 
    .example_dashed_border { 
        border: dashed;
        border-width: thin;
    }
    .override_tile {
        width: 100px;
    }
    #grid_123 {
        grid-template-columns: calc(var(--page-width) / 3);
        grid-row-gap: 1em;
        justify-content: space-evenly;
        justify-items: center;
    }
</style>

# Tile Grid Style Overrides

The rendering of Terminal for MkDocs Tile Grid can be customized by setting the `grid_id` and `grid_css` attributes in the markdown page's metadata[^1].  

- `grid_id` sets the HTML ID on the div containing the tile grid.  

- `grid_css` is added to the div's CSS classes.  

[^1]: see [Overview] for more info on page metadata.
[Overview]: ../..#1-add-tiles-to-page-metadata

## Extra CSS
To demonstrate how the tile grid's style can be overriden, the following `<style>` HTML is included in this page's markdown:

- `.example_dashed_border`: sets the border to a dashed line
- `.override_tile`: sets image width to 100px  
- `#grid_123`: sets the tile grid's column widths explicitly  


```css
<style> 
    .example_dashed_border { 
        border: dashed;
        border-width: thin;
    }
    .override_tile {
        width: 100px;
    }
    #grid_123 {
        grid-template-columns: calc(var(--page-width) / 3);
        grid-row-gap: 1em;
        justify-content: space-evenly;
        justify-items: center;
    }
</style>
```

## Grid Markdown
Note that the metadata on this page includes `grid_id: "grid_123"` and `grid_css: "example_dashed_border"`.  These settings override the tile grid's original styling to the custom styling defined on this page (see previous section).

```markdown
---
show_tiles_first: true
grid_id: "grid_123"
grid_css: "example_dashed_border"
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    alt_text: 'close up of fallen leaves.'
    tile_css: 'override_tile'
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    alt_text: 'close up of green moss on a log.'
    tile_css: 'override_tile'
  - caption: '@Guillaume'
    img_src: ../../../img/picsum/120_small.jpg
    alt_text: 'milky way with a rustic picket fence in the foreground'
    tile_css: 'override_tile'
---
```