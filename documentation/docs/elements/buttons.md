**Buttons**  
## Setup

Adding button classes to links requires the `attr_list` and `md_in_html` markdown extensions.  Add them to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```

### Examples
#### Default
[Default](buttons.md#default){ .btn .btn-default }  

```markdown
[Default](buttons.md#default){ .btn .btn-default }
```

#### Primary
[Primary Button](buttons.md#primary){ .btn .btn-primary }  

```markdown
[Primary Button](buttons.md#primary){ .btn .btn-primary } 
```

#### Error
[Error Button](buttons.md#error){ .btn .btn-error }  

```markdown
[Error Button](buttons.md#error){ .btn .btn-error } 
```

#### Ghost Default
[Ghost Default](buttons.md#ghost-default){ .btn .btn-default .btn-ghost }  

```markdown
[Ghost Default](buttons.md#ghost-default){ .btn .btn-default .btn-ghost }  
```

#### Ghost Primary
[Ghost Primary Button](buttons.md#ghost-primary){ .btn .btn-primary .btn-ghost }  

```markdown
[Ghost Primary Button](buttons.md#ghost-primary){ .btn .btn-primary .btn-ghost } 
```

#### Ghost Error
[Ghost Error Button](buttons.md#ghost-error){ .btn .btn-error .btn-ghost }  

```markdown
[Ghost Error Button](buttons.md#ghost-error){ .btn .btn-error .btn-ghost }  
```

#### Block Level
[Block Level Button](buttons.md#block-level){ .btn .btn-primary .btn-block } 

```markdown
[Block Level Button](buttons.md#block-level){ .btn .btn-primary .btn-block }
```

#### Group 
<div class="btn-group" markdown>
[Left](buttons.md){ .btn .btn-ghost }
[Middle](buttons.md){ .btn .btn-ghost }
[Right](buttons.md){ .btn .btn-ghost }  
</div>

```markdown
<div class="btn-group" markdown>
[Left](buttons.md){ .btn .btn-ghost }
[Middle](buttons.md){ .btn .btn-ghost }
[Right](buttons.md){ .btn .btn-ghost }  
</div>
```
