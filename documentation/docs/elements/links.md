# Links
A link can be specified with markdown by putting the link's **display text** in square brackets followed by the link's **address** in parentheses.  There is no space in between the square brackets and the open parenthesis.

## Simple Example

[Home Page](https://ntno.github.io/mkdocs-terminal/)

```markdown
[Home Page](https://ntno.github.io/mkdocs-terminal/)
```

## Enhanced Links Setup

Adding attributes to links requires the `attr_list` markdown extension.  Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
```

## Example
Note that adding the `target="_blank"` attribute causes the link to open in a new tab.  
The `title="go to source code"` adds a on hover title to the link.


[GitHub Repository](https://github.com/ntno/mkdocs-terminal){target="_blank", title="go to source code"}

```markdown
[GitHub Repository](https://github.com/ntno/mkdocs-terminal){target="_blank", title="go to source code"}
```