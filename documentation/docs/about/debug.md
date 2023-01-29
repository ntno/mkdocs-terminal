---
show_tiles_inline: true
tiles:
  - caption: '*@petradr*'
    img_src: ../../img/picsum/167_200x200.jpeg
    img_title: 'to Picsum homepage'
    img_alt: 'close up image of fallen leaves'
    link_href: https://picsum.photos/ 
  - caption: 'Marcin **C**zerwinski'
    img_src: ../../img/picsum/127_200x200.jpeg
    img_title: 'to Picsum homepage'
    img_alt: 'close up image of green moss on a log'
    link_href: https://picsum.photos/ 
  - caption: "[Steve Richey](https://picsum.photos/)"
    img_src: ../../img/picsum/143_200x200.jpeg
    img_title: 'to Picsum homepage'
    img_alt: 'overhead image of fallen leaves'
    link_href: https://picsum.photos/
# {{ macros_info() }}    
---

# Debug Markdown Experiments

## incorrect usage
{{ tile_grid("sdf") }}

## correct usage
{{ tile_grid(page.meta) }}
