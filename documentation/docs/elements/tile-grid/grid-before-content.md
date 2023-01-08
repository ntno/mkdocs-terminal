---
show_tiles_first: true
tiles:
  - caption: Wide Image
    img_src: https://picsum.photos/seed/abcd/1000/600
    img_title: Wide Image Tooltip
    img_alt: 'a random wide image'
    link_href: https://picsum.photos/
  - caption: Square Image
    img_src: https://picsum.photos/seed/efg/200
    img_title: Square Image Tooltip
    img_alt: 'a random square image'
    link_href: https://picsum.photos/
  - caption: Squat Image
    img_src: https://picsum.photos/seed/hij/1000/800
    img_title: Squat Image Tooltip
    img_alt: 'a random Squat image'
    link_href: https://picsum.photos/
  - caption: Tall Image
    img_src: https://picsum.photos/seed/klmn/500/900
    img_title: Tall Image Tooltip
    img_alt: 'a random tall image'
    link_href: https://picsum.photos/    
  - caption: Long Image
    img_src: https://picsum.photos/seed/opq/1000/350
    img_title: Long Image Tooltip
    img_alt: 'a random image'
    link_href: https://picsum.photos/
  - caption: Another Square Image
    img_src: https://picsum.photos/seed/rst/300
    img_title: Another Square Image Tooltip
    img_alt: 'a random square image'
    link_href: https://picsum.photos/                
---
<br>
--8<--
elements/tile-grid/links.md
--8<--

# Tile Grid
Terminal for MkDocs enables you to quickly create a grid of linked tiles.  Each tile can contain an image (with optional caption, title, and alt text) and 


## Markdown

```markdown
---
show_tiles_first: true
tiles:
  - caption: Wide Image
    img_src: https://picsum.photos/1000/600?random=1
    img_title: Wide Image Tooltip
    img_alt: 'a random wide image'
    link_href: https://picsum.photos/
  - caption: Square Image
    img_src: https://picsum.photos/200?random=2
    img_title: Square Image Tooltip
    img_alt: 'a random square image'
    link_href: https://picsum.photos/
  - caption: Squat Image
    img_src: https://picsum.photos/1000/800?random=4
    img_title: Squat Image Tooltip
    img_alt: 'a random Squat image'
    link_href: https://picsum.photos/
  - caption: Tall Image
    img_src: https://picsum.photos/600/1000?random=3
    img_title: Tall Image Tooltip
    img_alt: 'a random tall image'
    link_href: https://picsum.photos/    
  - caption: Long Image
    img_src: https://picsum.photos/1000/350?random=5
    img_title: Long Image Tooltip
    img_alt: 'a random image'
    link_href: https://picsum.photos/
  - caption: Another Square Image
    img_src: https://picsum.photos/200?random=6
    img_title: Another Square Image Tooltip
    img_alt: 'a random square image'
    link_href: https://picsum.photos/                
---
```