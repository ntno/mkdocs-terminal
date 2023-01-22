**Links**  

# Simple Example

[Documentation Home Page](https://ntno.github.io/mkdocs-terminal/)

## Markdown
```markdown
[Documentation Home Page](https://ntno.github.io/mkdocs-terminal/)
```

# Enhanced Links
## Setup

Adding attributes to links requires the `attr_list` markdown extension.  Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
```

## Enhanced Example
Note that adding the `target="_blank"` attribute causes the link to open in a new tab.


[GitHub Repository](https://github.com/ntno/mkdocs-terminal){target="_blank"}


### Markdown
```markdown
[GitHub Repository](https://github.com/ntno/mkdocs-terminal){target="_blank"}
```