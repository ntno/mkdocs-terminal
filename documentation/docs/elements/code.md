<style> 
    .no_hljs span { 
        color: var(--global-font-color) !important;
        font-weight: inherit !important;
    }
</style>

# Code

A outlined code block can be specified in markdown by putting three backticks (<code>\`\`\`</code>) at the beginning of a line, content on the following lines, and lastly three back ticks at the beginning   in between three backticks.  


## Example - default

<div class="no_hljs">
```
const numbers = [102, -1, 2]; 
numbers.sort((a, b) => a - b);
console.log(numbers);
```
</div>

## Example - with HilightJS

```
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```

## Markdown
<code class="no_hljs">
```markdown 
``` # start the code block with three backticks 
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
``` # end the code block
``` 
</code>


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