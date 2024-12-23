---
show_tiles_first: true
tiles:
  - caption: <a id="fnref:1" class="footnote-ref" title="to image description" alt="to Default PyMdown + Pygments Bash example description." href="#fn:1">PyMdown + Pygments (Default)</a>
    img_src: ../../img/code-highlighting/default_terminal_default_pygments.png
    tooltip: to PyMdown + Pygments Demo Site
    alt_text: PyMdown + Pygments Demo Site
    link_href: https://ntno.github.io/mkdocs-terminal-example-pymdown-pygments
    tile_css: image_border
  - caption: <a id="fnref:2" class="footnote-ref" title="to image description" alt="to Dark PyMdown + Pygments Bash example description." href="#fn:2">PyMdown + Pygments (Dark)</a>
    img_src: ../../img/code-highlighting/dark_terminal_github-dark_pygments.png
    tooltip: to PyMdown + Pygments Dark Demo Site
    alt_text: PyMdown + Pygments Dark Demo Site
    link_href: https://ntno.github.io/mkdocs-terminal-example-pymdown-pygments-dark
  - caption: <a id="fnref:3" class="footnote-ref" title="to image description" alt="to Default Highlight.js Bash example description." href="#fn:3">Highlight.js (Default)</a>
    img_src: ../../img/code-highlighting/default_highlightjs.png
    tooltip: to Highlight.js Demo Site
    alt_text: Highlight.js Demo Site
    link_href: https://ntno.github.io/mkdocs-terminal-example-highlightjs
    tile_css: image_border
  - caption: <a id="fnref:4" class="footnote-ref" title="to image description" alt="to Dark Highlight.js Bash example description." href="#fn:4">Highlight.js (Dark)</a>
    img_src: ../../img/code-highlighting/dark_highlightjs.png
    tooltip: to Highlight.js Dark Demo Site
    alt_text: Highlight.js Dark Demo Site
    link_href: https://ntno.github.io/mkdocs-terminal-example-highlightjs-dark
---
<style>
  .image_border a img {
    border: solid;
    border-width: thin;
    border-color: var(--secondary-color);
  }
</style>


# Code Hilighting

Code blocks can be highlighted for increased readability.  
Please note that there are multiple ways of highlighting code in a MkDocs site and some methods may conflict with each other.

## PyMdown and Pygments

[PyMdown Extensions] and the [Pygments] library can be used to enable language-specific code hilighting in code blocks and in inline code.  They work by adding highlighting to code as it is rendered to HTML during the MkDocs build process.

[Pygments]: https://pygments.org/
[PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

Configuration Instructions:  

- [PyMdown and Pygments Default](https://ntno.github.io/mkdocs-terminal-example-pymdown-pygments)
- [PyMdown and Pygments Dark](https://ntno.github.io/mkdocs-terminal-example-pymdown-pygments-dark)

## highlight.js

The [highlight.js] library can be used to enable language-specific code highlighting.  This library works by applying code highlighting to a page after it is loaded in the user's web browser.

Configuration Instructions:  

- [Highlight.js Default](https://ntno.github.io/mkdocs-terminal-example-highlightjs)
- [Highlight.js Dark](https://ntno.github.io/mkdocs-terminal-example-highlightjs-dark)

[highlight.js]: https://highlightjs.org/



[^1]: light blue background with red strings and green commands.
[^2]: dark grey background with light blue strings and white commands.
[^3]: white background with green strings and brown commands.
[^4]: black background with bright green strings and orange commands.