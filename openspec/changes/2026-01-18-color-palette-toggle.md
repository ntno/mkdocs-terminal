---
title: Color Palette Switcher
status: proposal
author: Natan Organick
date: 2026-01-18
---

# Color Palette Toggle

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
    options:
      - dark
      - light
      - solarized
    switcher: true
```

- Implementation details:
  - CSS: introduce CSS variables for color tokens and a small set of palette files (e.g. `palette-dark.css`, `palette-light.css`, `palette-solarized.css`) under `terminal/css/palettes/`.
  - Templates: add a small switcher control in `terminal/partials/top-nav` (or appropriate partial) that renders the UI when `theme.palette.switcher` is truthy.
  - JavaScript: add a lightweight client script (under `terminal/js`) to handle toggle UI, apply a palette by adding a `data-palette` attribute or class on the `html` element, and persist selection to `localStorage`.
  - No-JS fallback: ensure the default palette declared in config is used server-side (via template) so sites render correctly without JS.

  - UI selection rules: the control implementation adapts to the number of configured options:
    - If `options` contains exactly 2 entries, render a binary toggle/checkbox (e.g., dark ↔ light).
    - If `options` contains more than 2 entries, render a select/dropdown, segmented control, or accessible menu listing all options.
    - For discoverability and accessibility, prefer a native `<select>` or an ARIA-compliant menu when more than two options are present.

  - Default bundled palettes: the theme will ship a curated set of palette files under `terminal/css/palettes/`. These files are the default options exposed by the toggle unless a site overrides the options in its `mkdocs.yml`.

  - Custom palettes: site authors must be able to specify custom palette CSS files in `mkdocs.yml`. The `theme.palette.options` list may include either named bundled palettes or mappings that point to a CSS file path (relative to the documentation or theme static directories). Example:

```yaml
theme:
  name: terminal
  palette:
    default: dark
    options:
      - dark
      - light
      - solarized
      - name: mysite
        css: assets/css/mysite-palette.css
    toggle: true
```

  The theme should resolve provided `css` paths and include them in the built site assets accordingly. If a custom CSS path is provided, the switcher will list the provided name and apply the referenced stylesheet when selected.

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
