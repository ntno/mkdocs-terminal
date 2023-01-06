# Buttons

Adding button classes to links requires the `attr_list` and `md_in_html` markdown extensions.  Add them to the markdown extensions list in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```
## Solid Buttons
### Default
[Default](buttons.md){class='btn btn-default'}  

```markdown
[Default](buttons.md){class='btn btn-default'}
```

### Primary
[Primary Button](buttons.md){class='btn btn-primary'}  

```markdown
[Primary Button](buttons.md){class='btn btn-primary'} 
```

### Error
[Error Button](buttons.md){class='btn btn-error'}  

```markdown
[Error Button](buttons.md){class='btn btn-error'} 
```

## Ghost Buttons
### Ghost Default
[Ghost Button](buttons.md){class='btn btn-default btn-ghost'}  

```markdown
[Ghost Button](buttons.md){class='btn btn-default btn-ghost'}  
```

### Ghost Primary
[Ghost Primary Button](buttons.md){class='btn btn-primary btn-ghost'}  

```markdown
[Ghost Primary Button](buttons.md){class='btn btn-primary btn-ghost'} 
```

### Ghost Error
[Ghost Error Button](buttons.md){class='btn btn-error btn-ghost'}  

```markdown
[Ghost Error Button](buttons.md){class='btn btn-error btn-ghost'}  
```

## Special Buttons
### Block Level
[Block Level Button](buttons.md){class='btn btn-primary btn-block'} 

```markdown
[Block Level Button](buttons.md){class='btn btn-primary btn-block'}
```

### Group 
<div class="btn-group" markdown>
[Left](buttons.md){class='btn btn-ghost'}
[Middle](buttons.md){class='btn btn-ghost'}
[Right](buttons.md){class='btn btn-ghost'}  
</div>

```markdown
<div class="btn-group" markdown>
[Left](buttons.md){class='btn btn-ghost'}
[Middle](buttons.md){class='btn btn-ghost'}
[Right](buttons.md){class='btn btn-ghost'}  
</div>
```
