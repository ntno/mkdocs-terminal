# mkdocs-terminal with highlight.js

This example site uses the [highlight.js] javascript library to add code highlighting to a page after it is loaded in the user's web browser.

Please review the [highlight.js docs] for more information:

- [supported languages]
- [style options]
- [get the latest files]

[highlight.js]: https://highlightjs.org/
[highlight.js docs]: https://highlightjs.readthedocs.io/en/latest/readme.html
[supported languages]: https://highlightjs.readthedocs.io/en/latest/supported-languages.html
[get the latest files]: https://cdnjs.com/libraries/highlight.js
[style options]: https://highlightjs.org/examples

## Set Up

### Add Highlighter Code

Create a javascript file which will trigger the `highlight.js` library to highlight code blocks.  

Save the file in your MkDocs docs folder and reference it in the `extra_javascript` section of `mkdocs.yml`:

```javascript
window.addEventListener('load', hljs_highlight, false);

function hljs_highlight() {
    hljs.highlightAll();
}
```

For this example site the above javascript code is saved to `docs/add_hljs_highlight.js`.

### Add highlight.js Library
#### javascript files

Add the `highlight.js` javascript library file(s) to your `mkdocs.yml`:

/// define
highlight.min.js

- **Required.** the core `highlight.js` library logic and highlighting instructions for ~40 common programming languages


add_hljs_highlight.js

- **Required.** a small script which uses the `hilight.js` library to hilight code blocks once an HTML page is loaded in the browser (see [Add Highlighter Code](index.md#add-highlighter-code))


LANGUAGE.min.js

- **Optional.** highlighting instructions for any language not included in the core library

///

#### CSS files

Terminal for MkDocs comes with built-in CSS styling for `hilight.js`.  This means that you don't have to specify an external stylesheet for code hilighting when you use `highlight.js`.  However if you prefer one of the community `hilight.js` [style options] you can specify it in the `extra_css` attribute in `mkdocs.yml`:

```yaml
extra_css:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/styles/a11y-light.min.css
```

#### mkdocs.yml example

The following excerpt is used to configure code hilighting on this example site:

```yaml
theme:
  name: terminal

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/highlight.min.js
  - https://unpkg.com/highlightjs-cobol/dist/cobol.min.js
  - add_hljs_highlight.js

extra_css:
  - https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/styles/a11y-light.min.css
```


