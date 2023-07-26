# Table of Contents
By default, only the top two sections by nesting level will display in the table of contents at the bottom left.  

For fine-grained control of which items display in the table of contents, add `toc` to `markdown_extensions` and configure according to the `toc` package's [extension options](https://python-markdown.github.io/extensions/toc/#usage).

**file**: `mkdocs.yml`  
```yaml
markdown_extensions:
  - toc:
      baselevel: "3"
      toc_depth: "3"
```

You can also style the section headings by setting the `permalink` symbol and its tooltip hover `permalink_title`:

**file**: `mkdocs.yml`    
```yaml
markdown_extensions:
  - toc:
      permalink: "#"
      permalink_title: Anchor link to this section for reference
```

## Default Nesting Explanation
On this page **(h1) Felidae** shows up in the table of contents because it is one of the highest level sections.  

**(h2) Felinae** and **(h2) Pantherinae** show up because they are directly underneath a top level section.  

**(h3) Felis catus**, **(h3) Panthera leo**, and **(h3) Panthera tigris** do *not* display in the table of contents because they are nested at a third level (not because they use the `<h3>` header).  

Note that **(h5) Canis familiaris** shows up in the table of contents even though it uses a `<h5>` header.  This is because it is in a subsection directly underneath the top level **(h1) Canidae** section.

<hr>
<strong>Detailed TOC Example Below</strong> <span>&#11015;</span>
<hr>

# (h1) Felidae 

Felidae is the family of mammals in the order Carnivora colloquially referred to as cats.

## (h2) Felinae - (purring)
The Felinae are a subfamily of the family Felidae. This subfamily comprises the small cats having a bony hyoid, because of which they are able to purr but not roar.

### (h3) Felis catus
Domestic cats:  
- [Maine Coon](https://en.wikipedia.org/wiki/Maine_Coon)  
- [Siberian](https://en.wikipedia.org/wiki/Siberian_cat)  
- [Sphynx](https://en.wikipedia.org/wiki/Sphynx_cat)  

## (h2) Pantherinae - (roaring)
Pantherinae is a subfamily within the family Felidae.  Pantherinae species are characterised by an imperfectly ossified hyoid bone with elastic tendons that enable their larynx to be mobile.

### (h3) Panthera leo 
The lion.

### (h3) Panthera tigris 
The tiger.

# (h1) Canidae

Canidae is a biological family of dog-like carnivorans, colloquially referred to as dogs, and constitutes a clade. A member of this family is also called a canid.  There are three subfamilies found within the canid family, which are the extinct Borophaginae and Hesperocyoninae, and the extant Caninae.

##### (h5) Canis familiaris
Domestic dogs:  
- [Alaskan Husky](https://en.wikipedia.org/wiki/Alaskan_husky)  
- [Beagle](https://en.wikipedia.org/wiki/Beagle)  
- [Greyhound](https://en.wikipedia.org/wiki/Greyhound)  



