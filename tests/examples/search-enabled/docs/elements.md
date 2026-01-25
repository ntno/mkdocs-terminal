## Blockquote Example

<section>
  <blockquote>
    <p>
      Measuring programming progress by lines of code is like measuring aircraft building progress by weight.
    </p>
    <footer>
      <cite><a href="http://www.thegatesnotes.com">Bill Gates</a></cite>
    </footer>
  </blockquote>
</section>

<br>

## Button Examples

[Default](#button-examples){ .btn .btn-default }  

[Primary Button](#button-examples){ .btn .btn-primary }  

[Error Button](#button-examples){ .btn .btn-error }  

[Ghost Default](#button-examples){ .btn .btn-default .btn-ghost }  

[Ghost Primary Button](#button-examples){ .btn .btn-primary .btn-ghost }  

[Ghost Error Button](#button-examples){ .btn .btn-error .btn-ghost }  

[Block Level Button](#button-examples){ .btn .btn-primary .btn-block } 

<div class="btn-group" markdown>
[Left](#button-examples){ .btn .btn-ghost }
[Middle](#button-examples){ .btn .btn-ghost }
[Right](#button-examples){ .btn .btn-ghost }  
</div>

<br>

## Code Example

The `console` command can be used to print text to the console:

```javascript
const numbers = [102, -1, 2];
numbers.sort((a, b) => a - b);
console.log(numbers);
```

<br>

## Definition List Example  

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

<br>

## Details Example  

/// info
This is an info block
///

/// warning
This is a warning
///

/// important
This is important
///

<br>

## Figure Example

<figure markdown>
![some image](https://picsum.photos/1000/600?random&imageWithCaption){ title="a random image" alt="randomly generated image." }
<figcaption>A Random Image</figcaption>
</figure>

<br>

# Footnotes

Footnotes are a great way to add supplemental or additional information to a
specific word, phrase, or sentence without interrupting the flow of a document[^credit].
Terminal for MkDocs provides the ability to define, reference and render
footnotes.

# Setup

This configuration adds the ability to define inline footnotes, which are then
rendered below all Markdown content of a document. Add the following lines to
`mkdocs.yml`:

```yaml
markdown_extensions:
  - footnotes
```

# Usage

## Example Footnote Marker

A footnote marker must be enclosed in square brackets and must start with a
caret `^`, directly followed by an arbitrary identifier, which is similar to
the standard Markdown link syntax.

Aliquam sit amet[^1] mauris ut mi ullamcorper efficitur.[^2]

```markdown
Aliquam sit amet[^1] mauris ut mi ullamcorper efficitur.[^2]
```

## Example Footnote Content

The footnote content must be declared with the same identifier as the marker.
It can be inserted at an arbitrary position in the document and is always
rendered at the bottom of the page. Furthermore, a backlink to the footnote
reference is automatically added.

## Single Line Footnote

Short footnotes can be defined on a single line:

[^1]: Etiam faucibus nunc vel feugiat maximus.

```markdown
[^1]: Etiam faucibus nunc vel feugiat maximus.
```


## Multi-Line Footnote

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


# Links
A link can be specified with markdown by putting the link's **display text** in square brackets followed by the link's **address** in parentheses.  There is no space in between the square brackets and the open parenthesis.

# Simple Example

[Home Page](https://ntno.github.io/mkdocs-terminal/)

## Markdown
```markdown
[Home Page](https://ntno.github.io/mkdocs-terminal/)
```

## Enhanced Links Setup

Adding attributes to links requires the `attr_list` markdown extension.  Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
```

## Example
Note that adding the `target="_blank"` attribute causes the link to open in a new tab.  
The `title="go to source code"` adds a on hover title to the link.


[GitHub Repository](https://github.com/ntno/mkdocs-terminal){target="_blank", title="go to source code"}


### Markdown
```markdown
[GitHub Repository](https://github.com/ntno/mkdocs-terminal){target="_blank", title="go to source code"}
```


# Lists 

Markdown supports unordered lists, ordered lists, and nested lists.  Nested items must be preceded by 4 spaces.

# Ordered List
To create an ordered list, add line items with numbers followed by periods. The numbers don’t have to be in numerical order, but the list should start with the number one.  

1. First item
1. Second item
1. Third item
    1. Indented item
    1. Indented item
1. Fourth item 

## Markdown
```markdown
1. First item
1. Second item
1. Third item
    1. Indented item
    1. Indented item
1. Fourth item 
```

## Unordered List
To create an unordered list, add dashes (-), asterisks (*), or plus signs (+) in front of line items.

* First item
* Second item
* Third item
    * Indented item
    * Indented item
* Fourth item 

## Markdown
```markdown
* First item
* Second item
* Third item
    * Indented item
    * Indented item
* Fourth item 
```

# Credit
Examples and instructional text in this document were adapted from the [basic syntax markdown guide] on [markdownguide.org].

[basic syntax markdown guide]: https://www.markdownguide.org/basic-syntax/#lists-1
[markdownguide.org]: https://www.markdownguide.org


## Table Example

| Release | Supported? |
| :-----: | :---------: |
| [1.0.0] | yes |
| [0.0.0] | no |

  [1.0.0]: https://github.com/ntno/mkdocs-terminal/releases/tag/1.0.0
  [0.0.0]: https://github.com/ntno/mkdocs-terminal/releases/tag/0.0.0

<br>

# Tooltip Setup

Adding tooltips to links requires the `attr_list` markdown extension.  Add it to the `markdown_extensions` configuration in `mkdocs.yml`:

```yaml
markdown_extensions:
  - attr_list
```

## Example

[Hover me][example]

  [example]: https://example.com "I'm a tooltip!"

### Markdown
```markdown
[Hover me][example]

  [example]: https://example.com "I'm a tooltip!"
```


## Inline Example

Here is another [Hover me](https://example.com){title="I'm a tooltip!"} example.  

```markdown
Here is another [Hover me](https://example.com){title="I'm a tooltip!"} example.
```


# Emphasis

Emphasis, aka italics, with *asterisks* or _underscores_.  
Strong emphasis, aka bold, with **asterisks** or __underscores__.  
Combined emphasis with **_asterisks and underscores_**.  

```markdown
Emphasis, aka italics, with *asterisks* or _underscores_.  
Strong emphasis, aka bold, with **asterisks** or __underscores__.  
Combined emphasis with **_asterisks and underscores_**.  
```

# Strikethrough
Note: requires the [pymdownx.tilde extension]

Strikethrough uses two tildes. ~~Scratch this.~~

```markdown
Strikethrough uses two tildes. ~~Scratch this.~~
```

# Subscript 
Note: requires the [pymdownx.tilde extension]

CH~3~CH~2~OH  
text~a\ subscript~  

```markdown
CH~3~CH~2~OH  
text~a\ subscript~  
```

# Superscript
Note: requires the [pymdownx.caret extension]

2^2^ = 4  
text^a\ superscript^  

```markdown
2^2^ = 4  
text^a\ superscript^  
```

# Marks
Note: requires the [pymdownx.mark extension]

- ==This was marked==
- ^^This was inserted^^
- ~~This was deleted~~


```markdown
- ==This was marked==
- ^^This was inserted^^
- ~~This was deleted~~
```

[pymdownx.tilde extension]: ../../configuration/extensions/pymdown-extensions/#caret-mark-tilde
[pymdownx.caret extension]: ../../configuration/extensions/pymdown-extensions/#caret-mark-tilde
[pymdownx.mark extension]: ../../configuration/extensions/pymdown-extensions/#caret-mark-tilde