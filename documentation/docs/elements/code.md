<style> 
    .no_hljs span { 
        color: var(--global-font-color) !important;
        font-weight: inherit !important;
    }
</style>

# Code

Specify code in markdown by enclosing text between three backticks (<code>\`\`\`</code>).  If each beginning/closing backtick group is given its own line, the code block will be rendered with an outlined box.  If the backtick groups are not given their own lines, the code block will be rendered inline.

## Examples

### Inline Code

The ```printf``` and ```echo``` commands can be used to print text to the screen in a shell session.  However, `printf` supports text formatting and `echo` does not.

### Default Code Block

<div class="no_hljs">
```
const numbers = [102, -1, 2]; 
numbers.sort((a, b) => a - b);
console.log(numbers);
```
</div>

### Highlighted Code Block

```javascript
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```

## Markdown

### Inline Code Markdown

A single backtick can also be used to mark code text inline:

````
The ```printf``` and ```echo``` commands can be used to print text to the screen in a shell session.  However, `printf` supports text formatting and `echo` does not.
````

### Default Code Block Markdown

<div class="no_hljs">
````
```
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```
````
</div>

### Highlighted Code Block Markdown

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