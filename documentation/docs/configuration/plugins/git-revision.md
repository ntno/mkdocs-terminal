# Git Revision Date Plugin
The third-party [git-revision-date]{target="_blank"} plugin automatically adds the last revision date of a markdown page to its MkDocs Page Metadata[^mkdocs-page-meta].  

[git-revision-date]: https://github.com/zhaoterryy/mkdocs-git-revision-date-plugin
[MkDocs Page Metadata]: https://www.mkdocs.org/dev-guide/themes/#mkdocs.structure.pages.Page.meta
[^mkdocs-page-meta]: see [MkDocs Page Metadata]{target="_blank"} for more information

# Built In Support
When the `git-revision-date` plugin is installed and enabled and the `revision.date` theme feature is enabled, Terminal for MkDocs will display the date of the most recent change to a page's source file on the rendered site page.  This component is added at the bottom of each page unless [page-specific hiding] is enabled.

<section markdown>
<figure markdown>
![Built In Git Revision Date Plugin Support](../../img/annotated/git-revision-date.png){title="Terminal for MkDocs adds 'Page last updated' text when plugin is enabled"; alt="screenshot with revision date Terminal component annotated" .terminal-mkdocs-thin-border }
<figcaption>Built In Git Revision Date Plugin Support</figcaption>
</figure>
</section>
<br>

[page-specific hiding]: git-revision.md#configuration


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

## 3. Configure Theme Display  
mkdocs.yml
```yaml
theme:
  name: terminal
  features:
    - revision.date
    - revision.commit_history
```







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

### Configuration