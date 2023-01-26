## future feature documentation
## (##) Caninae
### (###) Canina (wolf-like)
### (###) Vulpini (fox-like)
#### (####) Canis (wolves, dogs, coyotes)
## Hideable Components
In order to hide components on a per-page basis, you need the meta markdown extension
```mkdocs.yml
markdown_extensions:
  - meta
```

Terminal for MkDocs' Tile Grid relies on the *meta*[^mkdocs-page-meta] attribute of a MkDocs *Page Object*[^mkdocs-page-object].  This means that in order for the tile grid to work properly, 

### references
- [Gioni06/terminal.css](https://github.com/Gioni06/terminal.css)  
- [build](https://pypa-build.readthedocs.io/en/latest/) for building distribution package  
- [twine](https://twine.readthedocs.io/en/stable/) for uploading to PyPI  
- [pypa/sampleproject](https://github.com/pypa/sampleproject)
- [mkdocs/mkdocs-basic-theme](https://github.com/mkdocs/mkdocs-basic-theme)
- [oprypin/mkdocs-section-index](https://github.com/oprypin/mkdocs-section-index)
- section-index support in material theme  
  - https://github.com/squidfunk/mkdocs-material/commit/accc2a34d15635884448d0c61b9b7f8301c0fddb
  - https://github.com/squidfunk/mkdocs-material/commit/149b0dbc475fd77a2cf00fdd6365078a900c023b
  - https://github.com/squidfunk/mkdocs-material/commit/f3926bf444a29310be0d14b1311b3dd832b1c310
- [mkdocs page struction](https://www.mkdocs.org/dev-guide/themes/#mkdocs.structure.pages.Page)
- [jinja namespace() added in 2.10](https://jinja.palletsprojects.com/en/3.0.x/changes/#version-2-10)
- [accessible menu bar nav example](https://www.w3.org/WAI/ARIA/apg/example-index/menubar/menubar-navigation)
- [pyproject.toml config](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
- lorem ipsum generators
  - https://generator.lorem-ipsum.info/
  - https://www.lipsum.com/
- [picture lore ipsum](https://picsum.photos/)
  - details: https://picsum.photos/id/{id}/info
  - img: https://picsum.photos/id/{id}/200/200  
- to read: [Make for devops](https://alexharv074.github.io/2019/12/26/gnu-make-for-devops-engineers.html)  
- to read: [testing bash scripts](https://alexharv074.github.io/2017/07/07/unit-testing-a-bash-script-with-shunit2.html)  
- [pytidylib](https://pythonhosted.org/pytidylib/)
- [jinja2 web render](https://j2live.ttl255.com/)  
- [regex101](https://regex101.com/)
- [schema.org - searchaction](https://schema.org/SearchAction)
- [magic mock](https://docs.python.org/3/library/unittest.mock.html)  
- [python debugger](https://www.geeksforgeeks.org/python-debugger-python-pdb/)  
- [broken link chekcer](https://matthewsetter.com/writing-tools/npm-broken-link-checker/)  
  
## regex
### linked image
`<div .*? <figure(.)[^>]*? <a(.)*<img`

### linked tile
`<div .*? <figure(.)[^>]*? <a(.)*`

### img tile
`<div .*? <figure(.)[^>]*? <img(.)*`



[project.entry-points."mkdocs.plugins"]
# markdown-filter = "mkdocs_markdown_filter.plugin:MarkdownFilterPlugin"