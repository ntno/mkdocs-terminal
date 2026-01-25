# Simple Table

| Release | Supported? |
| ------- | ---------- |
| 1.0.0   | yes        |
| 0.0.0   | no         |

## Markdown
```markdown
| Release | Supported? |
| ------- | ---------- |
| 1.0.0   | yes        |
| 0.0.0   | no         |
```

## Table with Alignment

Colons can be used to align columns.  Note that the "Release" column is centered and the "Supported?" column is right aligned:

| Release | Supported? |
| :-----: | ---------: |
|  1.0.0  | yes        |
|  0.0.0  | no         |

## Markdown
```markdown
| Release | Supported? |
| :-----: | ---------: |
|  1.0.0  | yes        |
|  0.0.0  | no         |
```

## Table with Markdown Values
Note: this example requires the [attr_list extension] be enabled.

| Release | Supported? |
| :-----: | :---------: |
| [1.0.0] | yes |
| [0.0.0] | no |

  [1.0.0]: https://github.com/ntno/mkdocs-terminal/releases/tag/1.0.0
  [0.0.0]: https://github.com/ntno/mkdocs-terminal/releases/tag/0.0.0

## Markdown
```markdown
| Release | Supported? |
| :-----: | :---------: |
| [1.0.0] | yes |
| [0.0.0] | no |

  [1.0.0]: https://github.com/ntno/mkdocs-terminal/releases/tag/1.0.0
  [0.0.0]: https://github.com/ntno/mkdocs-terminal/releases/tag/0.0.0
```

[attr_list extension]: ../../configuration/extensions/python-markdown/#attribute-lists