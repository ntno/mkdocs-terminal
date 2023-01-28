---
ignore_macros: true
---
# Tile Grid Pluglet

## Setup
install `mkdocs-macros-plugin`.
mkdocs.yml:

```
plugins:
  - md-to-html
  - macros:
      modules: 
        - mkdocs-terminal:terminal.pluglets.tile_grid.main
```

## Usage
`{{ tile_grid(page.meta) }}`