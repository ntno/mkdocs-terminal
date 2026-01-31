---
title: Color Palette Selector
status: proposal
author: Natan Organick
date: 2026-01-18
---

# Color Palette Selector

Summary
-------
Add an optional, built-in color-palette selector to the `mkdocs-terminal` theme that allows
site visitors to choose between configured palette options (for example, `dark`, `light`,
and named palettes like `solarized`). The selector should be configurable via `mkdocs.yml`,
persist user selection (localStorage), be accessible, and degrade gracefully when JavaScript
is disabled.

Motivation
----------
- Improve end-user control and accessibility by allowing runtime palette switching.
- Provide a simple site-level configuration for theme authors to expose curated palettes.
- Avoid forcing consumers to write custom JS/CSS for a common UX pattern.

Design
------
- Theme YAML configuration (example):

```yaml
theme:
  name: terminal
  palette:
    default: dark
    selector:
      enabled: true
      ui: auto   # values: auto | toggle | select
      options:
        - dark
        - light
        - solarized
```

- Implementation details:
  - CSS: introduce CSS variables for color tokens and a small set of palette files (e.g. `palette-dark.css`, `palette-light.css`, `palette-solarized.css`) under `terminal/css/palettes/`.
  - Templates: add a small selector control in `terminal/partials/top-nav` (or appropriate partial) that renders the UI when `theme.palette.selector.enabled` is truthy.
    - Overridable UI: implement the selector UI as a dedicated partial (for example `terminal/partials/palette_selector.html`) and expose a Jinja block such as `{% block palette_selector %}{% endblock %}` or provide a named include. This allows site authors to override the selector UI via `theme.custom_dir` or packaged theme overrides if they prefer to supply a custom control. The default partial must provide the documented `auto/toggle/select` behavior and be the fallback when no override is present.
    - Customer documentation: document the override process and example usage in the customer-facing configuration docs at `documentation/docs/configuration/blocks.md` (not the developer README). Include a short example showing how to place an override in `docs_dir` or `theme.custom_dir`, and demonstrate how the override should reference `selector.options` and respect `extra_css` for custom palette files.
  - JavaScript: add a lightweight client script (under `terminal/js`) to handle toggle UI, apply a palette by adding a `data-palette` attribute or class on the `html` element, and persist selection to `localStorage`.
  - No-JS fallback: ensure the default palette declared in config is used server-side (via template) so sites render correctly without JS.

  - UI selection rules: the control implementation adapts to the number of configured `selector.options` and the `selector.ui` preference:
    - `selector.ui: auto` (default):
      - If `selector.options` contains exactly 2 entries, render a binary toggle.
      - If `selector.options` contains more than 2 entries, render a native `<select>` or an accessible menu.
    - `selector.ui: toggle`: force a binary toggle UI. If there are more than 2 `selector.options`, the theme must fall back to a `<select>` (and may log a developer console warning).
    - `selector.ui: select`: force a `<select>` UI. If there are less than 2 `selector.options`, do not render the control.
    - For accessibility, prefer native controls when possible and ensure keyboard focus and ARIA labels are present.

  - Default bundled palettes: the theme will ship a curated set of palette files under `terminal/css/palettes/`. These files are the default options exposed by the selector unless a site overrides `selector.options` in its `mkdocs.yml`.

  - Custom palettes: site authors must be able to specify custom palette CSS files in `mkdocs.yml`. The `theme.palette.selector.options` list may include either named bundled palettes or mappings that point to a CSS file path (relative to the documentation or theme static directories). Example:

```yaml
theme:
  name: terminal
  palette:
    default: dark
    selector:
      enabled: true
      ui: auto
      options:
        - dark
        - light
        - solarized
        - name: mysite
          css: assets/css/mysite-palette.css
```

  The theme will not automatically inject arbitrary user files into MkDocs' `extra_css` — therefore site authors must include any custom palette CSS in their `mkdocs.yml` `extra_css` list so MkDocs will copy and link the file into the built site. For example:

```yaml
theme:
  name: terminal
  palette:
    default: dark
    selector:
      enabled: true
      ui: auto
      options:
        - dark
        - name: mysite
          css: assets/css/mysite-palette.css

extra_css:
  - assets/css/mysite-palette.css
```

If a custom CSS path is provided in `selector.options`, the selector will list the provided name and apply the referenced stylesheet when selected; the author must ensure the file is available in `extra_css` so the browser can load it at runtime.

  - Misconfiguration handling: the theme must validate custom palette entries before exposing them as selectable options. At build/render time the theme should confirm the referenced CSS file is present (for example, listed in `config.extra_css` or available in the built site assets). If the file cannot be found, the theme should:
    - omit the invalid option from the selector UI,
    - surface a non-blocking warning for developers (console log during runtime and/or builder-time warning in docs build output), and
    - continue using the configured `default` palette so end-users are not affected.

Accessibility
-------------
- Ensure palettes meet contrast guidelines (WCAG AA where feasible) — document expected contrast requirements for maintainers adding new palettes.
- Toggle control must be keyboard-accessible and announced to screen readers (use accessible role/labels).

Backwards Compatibility
-----------------------
- Default behavior: if `theme.palette` is not configured, there is no change.
- Existing sites that set custom CSS should not be impacted unless they opt into `palette` config or include the toggle UI.
 - Preserve legacy `palette` string config: some sites currently set `palette: "dark"` (a plain string). The theme must continue to accept that form and treat it as the equivalent of:

```yaml
palette:
  default: dark
  selector:
    enabled: false
```

  In other words, a string `palette` value selects the default palette server-side and does not enable the selector UI.

 - Migration: when the theme detects the legacy string form at build/render time, it should normalize the config internally to the new object shape (for template rendering and tests) so downstream code can depend on the new structure without breaking older `mkdocs.yml` files.


Testing
-------
- Add unit/integration tests to validate:
  - Template renders toggle only when enabled.
  - Default palette is present server-side.
  - Client-side script applies and persists palette selection (JS-enabled test harness).
  - Visual smoke checks (manual or screenshot tests) for sample palettes.

Docs
----
- Add documentation under `documentation/docs/configuration/` describing `theme.palette` usage, examples, and guidance for creating new palettes.
- Update `README.md` and any theme demos to show the toggle in action.

Implementation Plan
-------------------
1. Add palette CSS files and define a minimal set of tokens.
2. Add template partial for toggle and wire conditional rendering based on config.
3. Add lightweight JS to apply/persist palette selection.
4. Add tests and documentation updates.
5. Publish as a minor release (backwards-compatible feature).

Acceptance Criteria
-------------------
- Template renders the selector UI when `theme.palette.selector.enabled` is truthy and lists options from `theme.palette.selector.options`.
- Legacy string config `palette: "<name>"` continues to set the server-side default palette and does not enable the selector UI. The theme internally normalizes legacy config to the new object shape.
- Custom palette entries referencing CSS files are only exposed when the referenced file is present in `config.extra_css` (or otherwise available in built site assets); missing files are omitted from the selector, a non-blocking warning is surfaced, and the `default` palette is used.
- Selector respects `selector.ui` and adapts: binary toggle for two options, select/menu for >2; fallbacks behave as specified (e.g., `ui: toggle` falls back to select when incompatible).
- Client-side selection is applied immediately, persisted to `localStorage`, and restored on subsequent page loads.
- The selector UI is overridable: a site can replace the partial `terminal/partials/palette_selector.html` or a provided `{% block palette_selector %}` and the theme falls back to the default implementation when no override is present.

Default Bundled Palettes
------------------------
The theme will include a curated default set of palette files under `terminal/css/palettes/`. Initial bundled files should include at least:

- dark: `dark.css`
- light: `default.css`

Additional palettes may be added in future releases; these defaults should be documented in the release notes and configuration docs.

Alternatives Considered
-----------------------
- Provide only server-side theme configuration without client toggle — reduces complexity but loses user control.
- Force consumers to implement their own toggles via docs examples — places burden on site authors.

Open Questions
--------------
- What palette names should be bundled by default? (decision: use the curated set under `terminal/css/palettes/` and document them in the configuration docs.)
- Contrast validation: this will be handled as a separate feature/EPIC; the palette toggle proposal does not include automated contrast checks.
