# Figures
## Setup

Captioned figures require the `attr_list` and `md_in_html` markdown extensions.  Add them to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```

## Example

<section markdown>
<figure markdown>
![some image](../img/picsum/120_small.jpg){ title="a starry night" ; alt="a dark sky filled with stars" }
<figcaption>@Guillaume via Picsum</figcaption>
</figure>
</section>


## Markdown

```markdown
<section markdown>
<figure markdown>
![some image](../img/picsum/120_small.jpg){ title="a starry night" ; alt="a dark sky filled with stars" }
<figcaption>@Guillaume via Picsum</figcaption>
</figure>
</section>
```



