---
show_tiles_first: true
tiles:
  - caption: Default <sub id="fnref:1"><a class="footnote-ref" alt="to long image description" href="#fn:1">1</a></sub>
    img_src: ../../img/palettes/default.png
    img_alt: Default Demo Page
    link_href: ./default/
  - caption: Gruvbox Dark <sub id="fnref:2"><a class="footnote-ref" alt="to long image description" href="#fn:2">2</a></sub>
    img_src: ../../img/palettes/gruvbox_dark.png
    img_alt: Gruvbox Dark Demo Page
    link_href: ./gruvbox-dark/
  - caption: Dark <sub id="fnref:3"><a class="footnote-ref" alt="to long image description" href="#fn:3">3</a></sub>
    img_src: ../../img/palettes/dark.png
    img_alt: Dark Demo Page
    link_href: ./dark/    
  - caption: Pink <sub id="fnref:4"><a class="footnote-ref" alt="to long image description" href="#fn:4">4</a></sub>
    img_src: ../../img/palettes/pink.png
    img_alt: Pink Demo Page
    link_href: ./pink/        
  - caption: Sans <sub id="fnref:5"><a class="footnote-ref" alt="to long image description" href="#fn:5">5</a></sub>
    img_src: ../../img/palettes/sans.png
    img_alt: Sans Demo Page
    link_href: ./sans/    
  - caption: Sans Dark <sub id="fnref:6"><a class="footnote-ref" alt="to long image description" href="#fn:6">6</a></sub>
    img_src: ../../img/palettes/sans_dark.png
    img_alt: Sans Dark Demo Page
    link_href: ./sans-dark/            
---
# Theme Color Palettes
Terminal for MkDocs subports the following color palettes by default:

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

[^1]: demo site with a white background and light blue hyperlinks.
[^2]: demo site with a dark grey background, orange hyperlinks, and light yellow text.
[^3]: demo site with a black background, light blue hyperlinks, and white text.
[^4]: demo site with a white background and pink hyperlinks.
[^5]: demo site with a white background, light blue hyperlinks, and sans font.
[^6]: demo site with a black background, light blue hyperlinks, and white text in sans font.