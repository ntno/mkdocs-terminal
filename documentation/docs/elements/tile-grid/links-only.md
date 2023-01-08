---
show_tiles_first: false
tiles:
  - caption: Example of tile without image
    title: 'open Picsum API for id 167'
    alt: 'link to Picsum API for id 167'
    url: https://picsum.photos/id/167/info
---
--8<--
elements/tile-grid/links.md
--8<--

# Link Only Tiles 
The tiles on this page only have the `caption`, `url`, `alt`, and `title` attributes set.  They do not have the `img_alt`, `img_url`, or `img_title` attributes.  They are rendered as a captioned link instead of a linked image.

```markdown
---
show_tiles_first: false
tiles:
  - caption: Example of tile without image
    title: 'open Picsum API for id 167'
    alt: 'link to Picsum API for id 167'
    url: https://picsum.photos/id/167/info
---
```


