--8<--
sample-languages/python-base.md
--8<--

## Inline Hilighting

Inline highlighting can be added by prefixing the code snippet with three colons and the name of the [pygments-supported programming language](https://pygments.org/languages/):

```text
```:::LANGUAGE some code snippet```
or
`:::LANGUAGE some code snippet`
```

**Example:**

The `:::python print()` function can be used to print content to STDOUT:
```:::python print("Hello World")```.

### Inline Markdown

```text
The `:::python print()` function can be used to print content to STDOUT:
```:::python print("Hello World")```.
```