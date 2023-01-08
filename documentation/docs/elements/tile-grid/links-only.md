---
show_tiles_first: false
tiles:
  - caption: Example of tile without image
    link_title: 'open Picsum API for id 167'
    link_alt: 'link to Picsum API for id 167'
    link_href: https://picsum.photos/id/167/info
---
--8<--
elements/tile-grid/links.md
--8<--

# Link Only Tiles 
The tiles on this page only have the `caption`, `link_href`, `link_alt`, and `link_title` attributes set.  They do not have the `img_alt`, `img_url`, or `img_title` attributes.  They are rendered as a captioned link instead of a linked image.

```markdown
---
show_tiles_first: false
tiles:
  - caption: Example of tile without image
    link_title: 'open Picsum API for id 167'
    link_alt: 'link to Picsum API for id 167'
    link_href: https://picsum.photos/id/167/info
---
```


