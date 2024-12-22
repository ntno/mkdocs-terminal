# Code

Specify code in markdown by enclosing text content between three backticks (<code>\`\`\`</code>).  If each beginning/closing backtick group is given its own line, the code block will be rendered with an outlined box as an independent block.  

If the backtick groups are *not* given their own lines, the code block will be rendered inline.

For convenience, inline code blocks can also be specified by enclosing text between one backtick (<code>\`</code>) instead of three.

## Code Block

```javascript
const numbers = [102, -1, 2]; 
numbers.sort((a, b) => a - b);
console.log(numbers);
```

## Code Block Markdown

````markdown
```javascript
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```
````

## Inline Code

The ```printf``` and ```echo``` commands can be used to print text to the screen in a shell session.  However, `printf` supports text formatting and `echo` does not.

### Inline Code Markdown

````
The ```printf``` and ```echo``` commands can be used to print text to the screen in a shell session.  However, `printf` supports text formatting and `echo` does not.
````