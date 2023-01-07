---
---
# Table of Contents
By default, only the top two sections by nesting level will display in the table of contents at the bottom left.  

For fine-grained control of which items display in the table of contents, add `toc` to the `markdown_extensions` list in `mkdocs.yml` and configure according to the `toc` package's [extension options ](https://python-markdown.github.io/extensions/toc/#usage){target="_blank"}.

```yaml
markdown_extensions:
  - toc:
      baselevel: "3"
      toc_depth: "3"
```

You can also style the section headings by setting the `permalink` symbol and its tooltip hover `permalink_title`:
```yaml
markdown_extensions:
  - toc:
      permalink: "#"
      permalink_title: Anchor link to this section for reference
```
<br>

### Default Nesting Explanation
For example, on this page **h1-Felidae** shows up in the table of contents because it is one of the highest level sections.  **h2-Felinae** and **h2-Pantherinae** show up because they are directly underneath a top level section.  

**h3-Felis-catus**, **h3-Panthera-leo**, and **h3-Panthera tigris** do *NOT* display in the table of contents because they are nested at a third level (not because they use the `<h3>` header).  Note that **h5-Canis-familiaris** displays in the table of contents even though it uses a `<h5>` header.  This is because it is in a subsection directly underneath the top level **h1-Canidae** section.

<hr>
Detailed TOC Example Below <span>&#11015;</span>
<hr>

# (h1) Felidae 

Praesent enim enim, imperdiet vel erat dapibus, pulvinar placerat urna. Pellentesque a tristique metus. Mauris iaculis, quam et pulvinar tempor, mi ligula dignissim lectus, et venenatis nulla est dignissim quam. Phasellus sollicitudin quis quam id vestibulum. Quisque convallis in justo vel volutpat.

- Sed molestie nisl eu enim euismod ultricies.
- In sit amet lacus ac ex ornare sagittis.

## (h2) Felinae - (purring)
Quisque sed posuere erat. Praesent et volutpat orci. Cras vulputate, leo id pretium cursus, elit risus aliquet est, eget finibus purus orci in velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean est metus, sollicitudin eu tincidunt et, feugiat nec est. 

### (h3) Felis catus
Domestic cats:  
- [Maine Coon](https://en.wikipedia.org/wiki/Maine_Coon){target="_blank"}  
- [Siberian](https://en.wikipedia.org/wiki/Siberian_cat){target="_blank"}  
- [Sphynx](https://en.wikipedia.org/wiki/Sphynx_cat){target="_blank"}  

## (h2) Pantherinae - (roaring)
Aliquam turpis purus, mattis et enim nec, euismod varius augue. Duis sit amet pretium justo. Praesent tortor dolor, tempor tempor erat vitae, facilisis blandit urna. Quisque lacinia fermentum ligula, sit amet dapibus mauris laoreet eget. Cras facilisis viverra libero, vel molestie ante posuere eget. 

### (h3) Panthera leo 
The Lion.

### (h3) Panthera tigris 
The Tiger.

# (h1) Canidae

Suspendisse eget neque sed nulla maximus ornare vitae non ligula. In a sollicitudin ligula. Donec fringilla dolor id sapien venenatis maximus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nam lacinia consectetur posuere. Praesent malesuada sapien et velit gravida, vel aliquet tellus porttitor. Suspendisse pellentesque id ligula a rutrum. 

Curabitur metus tellus, commodo et faucibus vitae, posuere ut dolor. Vivamus ultricies, risus sed euismod imperdiet, est ante convallis nibh, nec venenatis leo nulla et elit. Morbi malesuada rutrum est ac tristique. Fusce sit amet dolor ut nibh posuere elementum ut eget nisi. Cras sed accumsan ante. Fusce luctus iaculis dui. 

##### (h5) Canis familiaris
Domestic dogs:  
- [Alaskan Husky](https://en.wikipedia.org/wiki/Alaskan_husky){target="_blank"}  
- [Beagle](https://en.wikipedia.org/wiki/Beagle){target="_blank"}  
- [Greyhound](https://en.wikipedia.org/wiki/Greyhound){target="_blank"}  



