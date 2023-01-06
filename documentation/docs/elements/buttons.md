# Button Setup

Adding button classes to links requires the `attr_list` and `md_in_html` markdown extensions.  Add them to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```
<br>

### Default
[Default](buttons.md#default){class='btn btn-default'}  

```markdown
[Default](buttons.md#default){class='btn btn-default'}
```

### Primary
[Primary Button](buttons.md#primary){class='btn btn-primary'}  

```markdown
[Primary Button](buttons.md#primary){class='btn btn-primary'} 
```

### Error
[Error Button](buttons.md#error){class='btn btn-error'}  

```markdown
[Error Button](buttons.md#error){class='btn btn-error'} 
```

### Ghost Default
[Ghost Default](buttons.md#ghost-default){class='btn btn-default btn-ghost'}  

```markdown
[Ghost Default](buttons.md#ghost-default){class='btn btn-default btn-ghost'}  
```

### Ghost Primary
[Ghost Primary Button](buttons.md#ghost-primary){class='btn btn-primary btn-ghost'}  

```markdown
[Ghost Primary Button](buttons.md#ghost-primary){class='btn btn-primary btn-ghost'} 
```

### Ghost Error
[Ghost Error Button](buttons.md#ghost-error){class='btn btn-error btn-ghost'}  

```markdown
[Ghost Error Button](buttons.md#ghost-error){class='btn btn-error btn-ghost'}  
```

### Block Level
[Block Level Button](buttons.md#block-level){class='btn btn-primary btn-block'} 

```markdown
[Block Level Button](buttons.md#block-level){class='btn btn-primary btn-block'}
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
