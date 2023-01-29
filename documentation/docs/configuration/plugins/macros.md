# MkDocs Macros Plugin

The third-party [macros]{target="_blank"} plugin transforms markdown pagess into jina2 templates.  This allows you to create more complex and feature-rich pages using variables, calls to cutom macros (functions), and filters.  

You can write and publish your own macros or you can install others' macros via pip and enable in your MkDocs config.

[macros]: https://mkdocs-macros-plugin.readthedocs.io/en/latest/


# Quick Setup

## 1. Install Plugin
Add the package to your `requirements.txt` file:

```text
# MkDocs Plugins
mkdocs-macros-plugin
```

Then run:  `pip install -r ./requirements.txt`


## 2. Enable Plugin

Enable the Git Revision Date Plugin by adding `macros` to the `plugins` list in `mkdocs.yml`:
```yaml
plugins:
    - search
    - macros
```


## 3. Verify Setup

Test that the plugin is working correctly by adding `{% raw %}{{ macros_info() }}{% endraw %}` to one of your documentation pages.  You should see a table with entries describing the MkDocs configuration for your site and details about the build environment:

<section markdown>
<figure markdown>
![Info Macro Output](../../img/macros/mkdocs_macros_config_info.png){alt="data table with entries corresponding to attributes in mkdocs.yml." .terminal-mkdocs-thin-border }
<figcaption>Info Macro Output</figcaption>
</figure>
</section>


