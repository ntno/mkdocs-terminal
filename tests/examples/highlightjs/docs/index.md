# mkdocs-terminal with highlight.js

This example site uses the [highlight.js] javascript library to add code highlighting to a page after it is loaded in the user's web browser.

Please review the [highlight.js docs] for more information:

- [supported languages]
- [get the latest files from a CDN]

[highlight.js]: https://highlightjs.org/
[highlight.js docs]: https://highlightjs.readthedocs.io/en/latest/readme.html
[supported languages]: https://highlightjs.readthedocs.io/en/latest/supported-languages.html
[get the latest files from a CDN]: https://highlightjs.readthedocs.io/en/latest/readme.html#fetch-via-cdn

## Set Up
### Add highlight.js

Specify the `highlight.js` javascript and CSS source files.  At a minimum you will need to include the main script `highlight.min.js` and stylesheet `a11y-light.min.css`.  You should also specify language specific scripts as needed.

`mkdocs.yml` excerpt:

```yaml
theme:
  name: terminal

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/highlight.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/bash.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/javascript.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/python.min.js
  - highlight.js

extra_css:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/styles/a11y-light.min.css
```

### Add Custom Highlighter Code

Add a custom javascript file which will trigger the `highlight.js` library to highlight code blocks after an HTML page loads.  You can add the file to `docs/highlight.js` and reference it in the `extra_javascript` section of `mkdocs.yml`:

```javascript
window.addEventListener('load', hljs_highlight, false);

function hljs_highlight() {
    hljs.highlightAll();
}
```
