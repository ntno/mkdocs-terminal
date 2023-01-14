<script>
    console.log(mkdocs_terminal_page_meta);
</script>

# Git Revision Date Plugin
This plugin automatically adds the last revision date to each markdown page's metadata.  The new `revision_date` attribute can then be used to display the page's last revision date.  See the "Page last updated" text at the bottom of this page as an example.

When the `git-revision-date` plugin is installed and enabled, Terminal for MkDocs will automatically display the page's last revision date at the bottom of each page.  This component can be hidden on a per-page basis if necessary.  See [Page Features] for more information on hiding the revision date for individual pages.

[See Plugin on GitHub](https://github.com/zhaoterryy/mkdocs-git-revision-date-plugin){target="_blank"}

[Page Features]: ../features.md#page-features

## Setup

## 1. Install Plugin
Add the package to your `requirements.txt` file:

```text
# MkDocs Plugins
mkdocs-git-revision-date-plugin
```

Then run:  `pip install -r ./requirements.txt`


## 2. Add Plugin to MkDocs Config

Enable the Git Revision Date Plugin by adding `git-revision-date` to the `plugins` configuration in `mkdocs.yml`:

mkdocs.yml
```yaml
plugins:
  - git-revision-date
```

## 3. Verify  



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
