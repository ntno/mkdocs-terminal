<style> 
    .no_hljs span { 
        color: var(--global-font-color) !important;
        font-weight: inherit !important;
    }
</style>

# Code

Specify a code block in markdown by enclosing text between three backticks (<code>\`\`\`</code>).  If each of the beginning/closing backtick groups are given their own line, the code block will be rendered with an outlined box (see [Block Examples](#block-examples)).  If the backtick groups are not given their own lines, the code block will be rendered inline (see [Inline Examples](#inline-examples)).



## Code Block Examples
### Default Code Block

<div class="no_hljs">
```
const numbers = [102, -1, 2]; 
numbers.sort((a, b) => a - b);
console.log(numbers);
```
</div>

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

### Highlighted Code Block

```js
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```

### Highlighted Code Block Markdown

<div class="no_hljs">
````
```js
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```
````
</div>










## language-specific highlighting

### javascript

```js
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```

### bash

```bash
echo "hello world" > file.txt
echo "hello stars" >> file.txt
echo "hello moon" >> file.txt
grep --color "s" file.txt
```