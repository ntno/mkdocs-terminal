# Tooltip Setup

Adding tooltips to links requires the `attr_list` markdown extension.  Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
```

## Example

[Hover me][example]

  [example]: https://example.com "I'm a tooltip!"

```markdown
[Hover me][example]

  [example]: https://example.com "I'm a tooltip!"
```


## Inline Example

Here is another [Hover me](https://example.com){title="I'm a tooltip!"} example.  

```markdown
Here is another [Hover me](https://example.com){title="I'm a tooltip!"} example.
```