# Definition Lists

## Setup

Enabling definition list styling requires the `def_list` markdown extension.  Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - def_list
```

# Example

`Lorem ipsum dolor sit amet`

:   Sed sagittis eleifend rutrum. Donec vitae suscipit est. 
    Nullam tempus tellus non sem sollicitudin, 
    quis rutrum leo facilisis.

`Cras arcu libero`

:   Aliquam metus eros, pretium sed nulla venenatis, 
    faucibus auctor ex. Proin ut eros sed sapien ullamcorper 
    consequat. Nunc ligula ante.

    Duis mollis est eget nibh volutpat, fermentum aliquet dui 
    mollis.  Nam vulputate tincidunt fringilla.  Nullam 
    dignissim ultrices urna non auctor.

## Markdown

```markdown
`Lorem ipsum dolor sit amet`

:   Sed sagittis eleifend rutrum. Donec vitae suscipit est. 
    Nullam tempus tellus non sem sollicitudin, 
    quis rutrum leo facilisis.

`Cras arcu libero`

:   Aliquam metus eros, pretium sed nulla venenatis, 
    faucibus auctor ex. Proin ut eros sed sapien ullamcorper 
    consequat. Nunc ligula ante.

    Duis mollis est eget nibh volutpat, fermentum aliquet dui 
    mollis.  Nam vulputate tincidunt fringilla.  Nullam 
    dignissim ultrices urna non auctor.
```