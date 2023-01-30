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
---

# Debug Markdown Experiments

## incorrect usage
{{ tile_grid("sdf") }}

## correct usage
{{ tile_grid(page.meta) }}

---

## bad render
<div class="terminal-mkdocs-tile-grid ">

    <div class="terminal-mkdocs-tile ">
        <figure>
            <a  href="https://picsum.photos/" > 
                    <img src="../../img/picsum/167_200x200.jpeg" alt="close up image of fallen leaves" title="to Picsum homepage" > 
            </a>
            <figcaption><p><em>@petradr</em></p></figcaption>

        </figure>
    </div>
    <div class="terminal-mkdocs-tile ">
        <figure>
            <a  href="https://picsum.photos/" > 
                    <img src="../../img/picsum/127_200x200.jpeg" alt="close up image of green moss on a log" title="to Picsum homepage" > 
            </a>
            <figcaption><p>Marcin <strong>C</strong>zerwinski</p></figcaption>

        </figure>
    </div>
    <div class="terminal-mkdocs-tile ">
        <figure>
            <a  href="https://picsum.photos/" > 
                    <img src="../../img/picsum/143_200x200.jpeg" alt="overhead image of fallen leaves" title="to Picsum homepage" > 
            </a>
            <figcaption><p><a href="https://picsum.photos/">Steve Richey</a></p></figcaption>

        </figure>
    </div>
</div>