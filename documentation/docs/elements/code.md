<style> 
    /* the no_hljs CSS class is used in this documentation page to call out the visual difference between code rendered with highlight.js and code rendered with the default styling attributes */
    .no_hljs span { 
        color: var(--global-font-color) !important;
        font-weight: inherit !important;
    }
</style>

# Code

Specify code in markdown by enclosing text content between three backticks (<code>\`\`\`</code>).  If each beginning/closing backtick group is given its own line, the code block will be rendered with an outlined box as an independent block.  

If the backtick groups are *not* given their own lines, the code block will be rendered inline.

For convenience, inline code blocks can also be specified by enclosing text between one backtick (<code>\`</code>) instead of three.

## Code Block

<div class="no_hljs">
```
const numbers = [102, -1, 2]; 
numbers.sort((a, b) => a - b);
console.log(numbers);
```
</div>

## Code Block Markdown

<div class="no_hljs">
````
```
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```
````
</div>

## Inline Code

The ```printf``` and ```echo``` commands can be used to print text to the screen in a shell session.  However, `printf` supports text formatting and `echo` does not.

### Inline Code Markdown

<div class="no_hljs">
````
The ```printf``` and ```echo``` commands can be used to print text to the screen in a shell session.  However, `printf` supports text formatting and `echo` does not.
````
</div>