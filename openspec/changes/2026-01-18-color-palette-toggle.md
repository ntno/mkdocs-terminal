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

Summary
-------
Add an optional, built-in color-palette switcher to the `mkdocs-terminal` theme that allows
site visitors to switch between configured palette options (for example, `dark`, `light`,
and named palettes like `solarized`). The switcher should be configurable via `mkdocs.yml`,
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
  - JavaScript: add a lightweight client script (under `terminal/js`) to handle toggle UI, apply a palette by adding a `data-palette` attribute or class on the `html` element, and persist selection to `localStorage`.
  - No-JS fallback: ensure the default palette declared in config is used server-side (via template) so sites render correctly without JS.

  - UI selection rules: the control implementation adapts to the number of configured `selector.options` and the `selector.ui` preference:
    - `selector.ui: auto` (default):
      - If `selector.options` contains exactly 2 entries, render a binary toggle/checkbox.
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

  The theme should resolve provided `css` paths and include them in the built site assets accordingly. If a custom CSS path is provided, the selector will list the provided name and apply the referenced stylesheet when selected.

Accessibility
-------------
- Ensure palettes meet contrast guidelines (WCAG AA where feasible) — document expected contrast requirements for maintainers adding new palettes.
- Toggle control must be keyboard-accessible and announced to screen readers (use accessible role/labels).

Backwards Compatibility
-----------------------
- Default behavior: if `theme.palette` is not configured, there is no change.
- Existing sites that set custom CSS should not be impacted unless they opt into `palette` config or include the toggle UI.

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

Alternatives Considered
-----------------------
- Provide only server-side theme configuration without client toggle — reduces complexity but loses user control.
- Force consumers to implement their own toggles via docs examples — places burden on site authors.

Open Questions
--------------
- What palette names should be bundled by default? (decision: use the curated set under `terminal/css/palettes/` and document them in the configuration docs.)
- Contrast validation: this will be handled as a separate feature/EPIC; the palette toggle proposal does not include automated contrast checks.
