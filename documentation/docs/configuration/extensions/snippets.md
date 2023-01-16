# Snippets Pymdownx Extension
## Setup

Enable Snippets by adding `pymdownx.snippets` to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.snippets:
      base_path: 
        - docs
```

See the [Snippets documentation][Snippets]{target="_blank"} for more information on additional configuration options.

  [Snippets]: https://facelessuser.github.io/pymdown-extensions/extensions/snippets/
  

# Usage

Let's say you have a header that you want to add to several documentation pages: 

file: `links.md`  
file location: `./configuration/palettes/links.md`  
```markdown
--8<--
configuration/palettes/links.md
--8<--
```

You can add the `--8<--` snippet marker to the page where you want to include this header:  

file: `gruvbox-dark.md`  
file location: `./configuration/palettes/gruvbox-dark.md`  
```markdown
;--8<--
configuration/palettes/links.md
;--8<--

# Gruvbox Dark Palette

To use the gruvbox_dark color palette, add the `palette` attribute to your theme configuration in `mkdocs.yml`:
...
```

This will result in a final markdown for `gruvbox-dark.md` which includes the content in `links.md`: 

```markdown
--8<--
configuration/palettes/gruvbox-dark.md::7
--8<--
...
```
