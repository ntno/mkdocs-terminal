---
show_tiles_first: true
tiles:
  - caption: <a id="fnref:1" class="footnote-ref" title="to image description" alt="to long image description" href="#fn:1">Default</a>
    img_src: ../../img/palettes/default.png
    tooltip: to Default Demo Page 
    alt_text: Default Demo Page
    link_href: ./default/
  - caption: <a id="fnref:2" class="footnote-ref" title="to image description" alt="to long image description" href="#fn:2">Gruvbox Dark</a>
    img_src: ../../img/palettes/gruvbox_dark.png
    tooltip: to Gruvbox Dark Demo Page
    alt_text: Gruvbox Dark Demo Page
    link_href: ./gruvbox-dark/
  - caption: <a id="fnref:3" class="footnote-ref" title="to image description" alt="to long image description" href="#fn:3">Dark</a>
    img_src: ../../img/palettes/dark.png
    tooltip: to Dark Demo Page 
    alt_text: Dark Demo Page
    link_href: ./dark/    
  - caption: <a id="fnref:4" class="footnote-ref" title="to image description" alt="to long image description" href="#fn:4">Pink</a>
    img_src: ../../img/palettes/pink.png
    tooltip: to Pink Demo Page
    alt_text: Pink Demo Page
    link_href: ./pink/        
  - caption: <a id="fnref:5" class="footnote-ref" title="to image description" alt="to long image description" href="#fn:5">Sans</a>
    img_src: ../../img/palettes/sans.png
    tooltip: to Sans Demo Page
    alt_text: Sans Demo Page
    link_href: ./sans/    
  - caption: <a id="fnref:6" class="footnote-ref" title="to image description" alt="to long image description" href="#fn:6">Sans Dark</a>
    img_src: ../../img/palettes/sans_dark.png
    tooltip: to Sans Dark Demo Page 
    alt_text: Sans Dark Demo Page
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

[^1]: demo site with a white background and light blue hyperlinks.
[^2]: demo site with a dark grey background, orange hyperlinks, and light yellow text.
[^3]: demo site with a black background, light blue hyperlinks, and white text.
[^4]: demo site with a white background and pink hyperlinks.
[^5]: demo site with a white background, light blue hyperlinks, and sans font.
[^6]: demo site with a black background, light blue hyperlinks, and white text in sans font.