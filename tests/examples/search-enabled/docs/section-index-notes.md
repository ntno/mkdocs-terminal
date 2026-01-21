
### Section index pages

When section index pages are enabled, documents can be directly attached to
sections, which is particularly useful for providing overview pages. Add the
following lines to `mkdocs.yml`:

```yaml
theme:
  features:
    - navigation.indexes # (1)!
```

1.  This feature flag is not compatible with [`toc.integrate`][toc.integrate],
    as sections cannot host the table of contents due to missing space.

=== "With section index pages"

    [![Section index pages enabled]][Section index pages enabled]

=== "Without"

    [![Section index pages disabled]][Section index pages disabled]

In order to link a page to a section, create a new document with the name
`index.md` in the respective folder, and add it to the beginning of your
navigation section:

```yaml
nav:
  - Section:
    - section/index.md
    - Page 1: section/page-1.md
    ...
    - Page n: section/page-n.md
```

  [Section index pages support]: https://github.com/squidfunk/mkdocs-material/releases/tag/7.3.0
  [Section index pages enabled]: ../assets/screenshots/navigation-index-on.png
  [Section index pages disabled]: ../assets/screenshots/navigation-index-off.png
  [toc.integrate]: #navigation-integration


        <!-- Determine all nested items that are index pages -->
      {% set indexes = [] %}
      {% if "navigation.indexes" in features %}
        {% for nav_item in nav_item.children %}
          {% if nav_item.is_index and not index is defined %}
            {% set _ = indexes.append(nav_item) %}
          {% endif %}
        {% endfor %}
      {% endif %}