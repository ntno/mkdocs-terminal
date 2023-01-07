---
show_tiles_first: true
tiles:
  - caption: Default
    img_src: ../../img/palettes/default.png
    img_title: Default
    img_alt: 'screenshot of demo site with the default color palette.  the site uses a white background with light blue hyperlinks.'
    url: ./default/
  - caption: Gruvbox Dark
    img_src: ../../img/palettes/gruvbox_dark.png
    img_title: Gruvbox Dark
    img_alt: 'screenshot of demo site with the gruvbox_dark color palette.  the site uses a dark grey background with orange hyperlinks and light yellow text.'
    url: ./gruvbox_dark/
  - caption: Dark
    img_src: ../../img/palettes/dark.png
    img_title: Dark
    img_alt: 'screenshot of demo site with the dark color palette.  the site uses a black background with light blue hyperlinks and white text.'
    url: ./dark/    
  - caption: Pink
    img_src: ../../img/palettes/pink.png
    img_title: Pink
    img_alt: 'screenshot of demo site with the pink color palette.  the site uses a white background with pink hyperlinks.'
    url: ./pink/        
  - caption: Sans
    img_src: ../../img/palettes/sans.png
    img_title: Sans
    img_alt: 'screenshot of demo site with the sans color palette.  the site uses a white background with light blue hyperlinks and sans font.'
    url: ./sans/    
  - caption: Sans Dark
    img_src: ../../img/palettes/sans_dark.png
    img_title: Sans Dark
    img_alt: 'screenshot of demo site with the sans_dark color palette.  the site uses a black background with light blue hyperlinks and white text in sans font.'
    url: ./sans_dark/            
---


# Theme Color Palettes
Terminal for MkDocs supports the following color palettes by default:

  - [default](default.md)
  - [gruvbox_dark](gruvbox_dark.md)
  - [dark](dark.md)
  - [pink](pink.md)
  - [sans](sans.md)
  - [sans_dark](sans_dark.md)

To change the color palette to one of the built in color palettes, add the `palette` attribute to your theme configuration in `mkdocs.yml`:

```yaml
theme:
  name: terminal
  palette: pink
```

