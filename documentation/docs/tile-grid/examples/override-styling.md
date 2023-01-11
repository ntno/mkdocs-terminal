---
show_tiles_first: true
grid_id: "grid_123"
grid_css: "example_solid_border"
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    div_css: "example_dashed_border"
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    div_css: "example_dashed_border"
  - caption: '@Guillaume'
    img_src: ../../../img/picsum/120_small.jpg
    img_width: "250"
    div_css: "example_dashed_border"
---

<style> 
    .example_solid_border {
      border: solid !important;
      border-width: thin !important;
    }

    .example_dashed_border { 
        border: dashed !important;
        border-width: thin !important;
    }

    #grid_123 {
        grid-gap: .5em !important;
        grid-template-columns: 100px 100px 250px !important;
        padding: 30px;
    }
</style>

# Tile Grid Style Overrides

Tile Grid can be further customized by setting the `grid_id` and `grid_css` attributes in the markdown page's metadata (see [Overview] for details).  

`grid_id` sets the HTML ID on the div containing the tile grid.  

`grid_css` is added to the div's CSS classes.  


[Overview]: ../..#1-add-tiles-to-page-metadata

## Extra CSS
To demonstrate how the tile grid's style can be overriden, the following `<style>` HTML is included in this page's markdown:

- `example_solid_border`: sets the border to a solid line  
- `example_dashed_border`: sets the border to a dashed line  
- `#grid_123`: sets the gile grid's column widths explicitly  


```css
<style> 
    .example_solid_border {
      border: solid !important;
      border-width: thin !important;
    }

    .example_dashed_border { 
        border: dashed !important;
        border-width: thin !important;
    }

    #grid_123 {
        grid-gap: .5em !important;
        grid-template-columns: 100px 100px 250px !important;
        padding: 30px;
    }
</style>
```

## Grid Markdown
Note that the metadata on this page includes `grid_id: "grid_123"` and `grid_css: "example_solid_border"`.  These settings override the tile grid's original styling to the custom styling defined on this page (see [above](#extra-css)).

```markdown
---
show_tiles_first: true
grid_id: "grid_123"
grid_css: "example_solid_border"
tiles:
  - caption: '@petradr'
    img_src: ../../../img/picsum/167_200x200.jpeg
    div_css: "example_dashed_border"
  - caption: 'Marcin Czerwinski'
    img_src: ../../../img/picsum/127_200x200.jpeg
    div_css: "example_dashed_border"
  - caption: '@Guillaume'
    img_src: ../../../img/picsum/120_small.jpg
    img_width: "250"
    div_css: "example_dashed_border"
---
```