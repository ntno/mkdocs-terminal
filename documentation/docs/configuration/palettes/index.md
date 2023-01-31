---
show_tiles_first: true
tiles:
  - caption: Default. <br>[fig. details](#default)
    img_src: ../../img/palettes/default.png
    img_alt: Default Demo Page
    link_href: ./default/
  - caption: Gruvbox Dark
    img_src: ../../img/palettes/gruvbox_dark.png
    img_alt: Gruvbox Dark Demo Page
    link_href: ./gruvbox-dark/
  - caption: Dark
    img_src: ../../img/palettes/dark.png
    img_alt: Dark Demo Page
    link_href: ./dark/    
  - caption: Pink
    img_src: ../../img/palettes/pink.png
    img_alt: Pink Demo Page
    link_href: ./pink/        
  - caption: Sans
    img_src: ../../img/palettes/sans.png
    img_alt: Sans Demo Page
    link_href: ./sans/    
  - caption: Sans Dark
    img_src: ../../img/palettes/sans_dark.png
    img_alt: Sans Dark Demo Page
    link_href: ./sans-dark/            
---
# Theme Color Palettes
Terminal for MkDocs supports the following color palettes by default:

  - [default](default.md)
  - [gruvbox_dark](gruvbox-dark.md)
  - [dark](dark.md)
  - [pink](pink.md)
  - [sans](sans.md)
  - [sans_dark](sans-dark.md)

To change the color palette to one of the built in color palettes, add the `palette` attribute to your theme configuration in `mkdocs.yml`:

```yaml
theme:
  name: terminal
  palette: pink
```

##### Image Descriptions
###### Default
demo site with a white background and light blue hyperlinks.

  <!-- img_desc: 'demo site with a dark grey background, orange hyperlinks, and light yellow text.'
  img_desc: 'demo site with a black background, light blue hyperlinks, and white text.'
  img_desc: 'demo site with a white background and pink hyperlinks.'
  img_desc: 'demo site with a white background, light blue hyperlinks, and sans font.'
  img_desc: 'demo site with a black background, light blue hyperlinks, and white text in sans font.' -->