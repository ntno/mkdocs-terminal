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
![some image](https://picsum.photos/1000/600?random&imageWithCaption){ title="a random image" ; alt="Random image with a caption" }
<figcaption>Image caption</figcaption>
</figure>
</section>


## Markdown

```markdown
<section markdown>
<figure markdown>
![some image](https://picsum.photos/1000/600?random&imageWithCaption){ title="a random image" ; alt="Random image with a caption" }
<figcaption>Image caption</figcaption>
</figure>
</section>
```



