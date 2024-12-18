# Highlight.js Example Site

This example site uses the [highlight.js] javascript library to add code highlighting after the page is loaded in the user's web browser.

[highlight.js]: https://highlightjs.org/


## Configuration

### Include highlight.js Scripts/Styles

Specify the `highlight.js` javascript and CSS source files.  At a minimum you will need to include the main script `highlight.min.js` and stylesheet `default.min.css`.  You should also specify language specific scripts as needed.

`mkdocs.yml` excerpt:

```yaml
theme:
  name: terminal

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/highlight.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/languages/bash.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/languages/javascript.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/languages/python.min.js
  - highlight.js

extra_css:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/styles/default.min.css
```

### Include Custom Highlighter Code

Add a custom javascript file which will trigger the `highlight.js` library to highlight code blocks after an HTML page loads.  You can add the file to `docs/highlight.js` and reference it in the `extra_javascript` section of `mkdocs.yml`:

```javascript
window.addEventListener('load', hljs_highlight, false);

function hljs_highlight() {
    hljs.highlightAll();
}
```