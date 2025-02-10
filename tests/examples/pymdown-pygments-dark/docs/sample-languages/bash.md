--8<--
sample-languages/bash-base.md
--8<--

## Inline Hilighting

Inline highlighting can be added by prefixing the code snippet with three colons and the name of the [supported programming language](https://pygments.org/languages/):

```text
```:::LANGUAGE some code snippet```
or
`:::LANGUAGE some code snippet`
```

**Example:**

The `:::bash read` command can be used to read input from STDIN.  Use the array flag `-a` to store the provided word sequence as an array:
```:::bash read -a my_array <<< "hello world"; echo ${my_array[0]}```.

### Inline Markdown

```text
The `:::bash read` command can be used to read input from STDIN.  Use the array flag `-a` to store the provided word sequence as an array:
```:::bash read -a my_array <<< "hello world"; echo ${my_array[0]}```.
```