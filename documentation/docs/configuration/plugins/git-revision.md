# Git Revision Date Plugin
This plugin automatically adds the last revision date to each markdown page's metadata.  This revision date can then be used by a template (in this case Terminal for MkDocs) to display the page's last revision date.

## Setup

## 1. Install Plugin
Add the package to your `requirements.txt` file:

```text
# MkDocs Plugins
mkdocs-git-revision-date-plugin
```

Then run:  `pip install -r ./requirements.txt`


## 2. Add Plugin to MkDocs Config

mkdocs.yml
```yaml
plugins:
  - git-revision-date
```

## 3. Configure Repository URL 



### Supported Repository Hosts

#### GitHub
repo_url: https://github.com/ntno/mkdocs-terminal  
edit_uri_template: https://github.com/ntno/mkdocs-terminal/edit/main/documentation/docs/{path}  
revision.html: https://github.com/ntno/mkdocs-terminal/commits/main/documentation/docs/index.md

#### Bitbucket
repo_url: https://bitbucket.org/norganick/demo
edit_uri_template: src/main/docs/{path}?mode=edit
revision.html: https://bitbucket.org/norganick/demo/src/main/docs/index.md?mode=read&at=main

### Adding Repository Hosts
If you host your repository on a different service, you can override the `revision` template block to include a link to your revision history.  
