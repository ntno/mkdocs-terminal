<style> 
    /* the no_hljs CSS class is used in this documentation page to call out the visual difference between markdown rendered with highlight.js and the original markdown file code snippet */
    .no_hljs span { 
        color: var(--global-font-color) !important;
        font-weight: inherit !important;
    }
</style>

# Code Hilighting

Code blocks can be highlighted for increased readability.  There are multiple ways of highlighting code in a MkDocs site.

## Browser Side Highlighting With hilight.js
### Example hilight.js Code Block

```javascript
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```

### Example highlight.js Code Block Markdown

The [highlight.js] library can be used to enable language-specific code highlighting.  See [highlight.js override] for instructions.

<div class="no_hljs">
````
```javascript
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```
````
</div>

[highlight.js]: https://highlightjs.org/
[highlight.js override]: ../../configuration/overrides/highlightjs