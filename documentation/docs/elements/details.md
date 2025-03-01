# Details setup

Enabling detail blocks requires the `pymdown.blocks.details` extension. Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.blocks.details:
      types:
        - name: info
          class: terminal-alert
          title: Info
        - name: warn
          class: 'terminal-alert terminal-alert-error'
          title: Warning
        - name: important
          class: 'terminal-alert terminal-alert-primary'
          title: Important
```

# Example

/// info
This is an info block
///

/// warning
This is a warning
///

/// important
This is important
///

/// info | Note
This is an info block with the title overwritten to "Note"
///

/// warning
    open: True
This is a warning that is expanded by default
///

# Markdown

```markdown
/// info
This is an info block
///

/// warning
This is a warning
///

/// important
This is important
///

/// info | Note
This is an info block with the title overwritten to "Note"
///

/// warning
    open: True
This is a warning that is expanded by default
///
```


