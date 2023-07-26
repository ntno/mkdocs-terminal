# Footnotes

Footnotes are a great way to add supplemental or additional information to a
specific word, phrase, or sentence without interrupting the flow of a document[^credit].
Terminal for MkDocs provides the ability to define, reference and render
footnotes.

## Setup

This configuration adds the ability to define inline footnotes, which are then
rendered below all Markdown content of a document. Add the following lines to
`mkdocs.yml`:

``` yaml
markdown_extensions:
  - footnotes
```

## Usage

### Example Footnote Marker

A footnote marker must be enclosed in square brackets and must start with a
caret `^`, directly followed by an arbitrary identifier, which is similar to
the standard Markdown link syntax.

Aliquam sit amet[^1] mauris ut mi ullamcorper efficitur.[^2]

```markdown
Aliquam sit amet[^1] mauris ut mi ullamcorper efficitur.[^2]
```

### Example Footnote Content

The footnote content must be declared with the same identifier as the marker.
It can be inserted at an arbitrary position in the document and is always
rendered at the bottom of the page. Furthermore, a backlink to the footnote
reference is automatically added.

### Single Line Footnote

Short footnotes can be defined on a single line:

[^1]: Etiam faucibus nunc vel feugiat maximus.

```markdown
[^1]: Etiam faucibus nunc vel feugiat maximus.
```


### Multi-Line Footnote

To define a multi-line footnote, create a paragraph on the next line after the marker identifier.  The multi-line definition must be indented by four spaces:

[^2]:
    Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque nisl nisl, aliquam sit amet erat sed, molestie scelerisque nunc. 
    
    Nullam ultricies non leo at commodo. Aliquam vehicula tempus ipsum, a scelerisque diam pharetra quis. Duis tempor semper tortor nec gravida. 
    
    Aliquam tincidunt scelerisque leo ut scelerisque. Duis massa eros, bibendum ac suscipit sit amet, maximus sit amet libero. 

```markdown
[^2]:
    Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque nisl nisl, aliquam sit amet erat sed, molestie scelerisque nunc. 

    Nullam ultricies non leo at commodo. Aliquam vehicula tempus ipsum, a scelerisque diam pharetra quis. Duis tempor semper tortor nec gravida. 
    
    Aliquam tincidunt scelerisque leo ut scelerisque. Duis massa eros, bibendum ac suscipit sit amet, maximus sit amet libero. 
```


[^credit]:
    This documentation page is based on squidfunk's [Material for MkDocs Footnotes](https://squidfunk.github.io/mkdocs-material/reference/footnotes/) documentation.

