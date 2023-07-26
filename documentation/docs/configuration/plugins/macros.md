# MkDocs Macros Plugin

The third-party [mkdocs-macros plugin] transforms markdown pages into [jinja2] templates.  This allows you to create complex and feature-rich pages using variables, calls to custom functions, and filters.  

You can write and publish your own functions to use in your markdown pages.  These functions are called macros.  You can also install macros written by others via pip.  Once a macro has been installed, it must be enabled in your MkDocs config before you can use it.

[mkdocs-macros plugin]: https://mkdocs-macros-plugin.readthedocs.io/en/latest/
[jinja2]: https://jinja.palletsprojects.com/en/3.1.x/intro/

## Quick Setup

### 1. Install Plugin
Add the `mkdocs-macros-plugin` package to your `requirements.txt` file:

```text
# MkDocs Plugins
mkdocs-macros-plugin
```

Then run:  `pip install -r ./requirements.txt`


### 2. Enable Plugin

Enable the MkDocs Macros Plugin by adding `macros` to the `plugins` list in `mkdocs.yml`:
```yaml
plugins:
    - search
    - macros
```


### 3. Verify Setup

Test that the plugin is working correctly by calling the built-in info macro from one of your documentation pages:  

**file**: macros-test.md  
```markdown
{% raw %}{{ macros_info() }}{% endraw %}
```  
A table with entries describing the MkDocs configuration for your site should be rendered in place of the macro call:

<section markdown>
<figure markdown>
![Info Macro Output](../../img/macros/mkdocs-macros-config-info.png){alt="data table with entries corresponding to attributes in mkdocs.yml." .terminal-mkdocs-thin-border }
<figcaption>Info Macro Output</figcaption>
</figure>
</section>


### 4. Configuration

See the plugin's [configuration documentation] for additional options.

[configuration documentation]: https://mkdocs-macros-plugin.readthedocs.io/en/latest/#configuration-of-the-plugin