
# Setup


requirements.txt
```text
# MkDocs Plugins
mkdocs-git-revision-date-plugin
```

mkdocs.yml
```yaml
plugins:
  - git-revision-date
```

## Supported Repository Hosts

### GitHub
repo_url: https://github.com/ntno/mkdocs-terminal  
edit_uri_template: https://github.com/ntno/mkdocs-terminal/edit/main/documentation/docs/{path}  
revision.html: https://github.com/ntno/mkdocs-terminal/commits/main/documentation/docs/index.md

### Bitbucket
repo_url: https://bitbucket.org/norganick/demo
edit_uri_template: src/main/docs/{path}?mode=edit
revision.html: https://bitbucket.org/norganick/demo/src/main/docs/index.md?mode=read&at=main

## Adding Repository Hosts
If you host your repository on a different service, you can override the `revision` template block to include a link to your revision history.  
