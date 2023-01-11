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
<hr>

# Tile Grid Style Overrides

To demonstrate how the tile grid's style can be overriden, the following `<style>` HTML is included in this page's markdown:

## Extra CSS
```
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