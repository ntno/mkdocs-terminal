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