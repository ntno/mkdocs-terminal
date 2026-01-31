# Color Palette Selector Proposal

## Why

The mkdocs-terminal theme currently lacks runtime color palette switching capability, forcing users to manually edit configuration files to change themes. Adding an optional, built-in palette selector improves user experience by allowing visitors to choose their preferred color scheme and have it persist across sessions. This addresses a common UX pattern that currently requires site authors to write custom JavaScript and CSS.

## What Changes

- Add `theme.palette` configuration schema supporting both legacy string format and new object structure with `default`, `selector.enabled`, `selector.ui`, and `selector.options` fields
- Create `ThemePaletteConfig` class to handle palette configuration parsing, validation, and normalization at build time
- Standardize CSS architecture using CSS custom properties scoped under `[data-palette="<name>"]` attribute selectors
- Add `terminal/partials/palette_selector.html` partial with conditional rendering based on configuration
- Create `terminal/js/palette_selector.js` for client-side palette switching and localStorage persistence
- Add inline script in `<head>` to restore saved palette before first paint (FOUC prevention)
- Link all palette CSS files in `<head>` during build (static site constraint - no dynamic loading)
- Validate custom palette CSS files exist in `config.extra_css` at build time
- Support UI adaptation: binary toggle for 2 options, select dropdown for >2 options
- **BREAKING**: None - feature is opt-in via `theme.palette.selector.enabled`

## Capabilities

### New Capabilities

- `palette-configuration`: Parse and validate `theme.palette` configuration from mkdocs.yml, supporting both legacy string format and new object structure
- `palette-css-architecture`: Manage CSS custom properties and scoping mechanism for palette switching via data attributes
- `palette-selector-ui`: Render adaptive UI control (toggle or select) in theme templates with ARIA accessibility attributes
- `palette-client-switching`: Handle client-side palette application, localStorage persistence, and restoration on page load
- `palette-validation`: Validate palette options at build time, filter invalid entries, emit warnings for misconfigured palettes

### Modified Capabilities

<!-- No existing capabilities are being modified -->

## Impact

**Affected Components:**
- Theme configuration schema (new `palette` field)
- CSS architecture (introduction of CSS custom properties across all 9 existing palette files)
- Template structure (new partial in `terminal/partials/`, integration in top-nav or appropriate location)
- JavaScript bundle (new ~2-3KB client script)
- Build process (configuration validation hook via MkDocs `on_config` event)

**Affected Files:**
- `terminal/css/palettes/*.css` - 9 existing files require standardization to CSS custom properties
- `terminal/partials/top-nav/*.html` - integration point for selector UI
- `terminal/base.html` or similar - inline FOUC prevention script
- `documentation/docs/configuration/` - new configuration documentation

**Dependencies:**
- No new external dependencies
- Leverages existing MkDocs configuration system
- Uses browser localStorage API (degrades gracefully when unavailable)

**Performance:**
- Minimal impact: ~2-3KB JavaScript, multiple CSS files pre-linked (only configured palettes loaded)
- FOUC prevention via inline script adds ~0.5-1KB to HTML size

**Accessibility:**
- All bundled palettes must meet WCAG AA contrast standards (validation via existing `tests/accessibility/test_color_contrast.py`)
- Selector UI must be keyboard accessible with proper ARIA attributes

**Backwards Compatibility:**
- Legacy `palette: "string"` format continues working (normalized internally)
- Sites without `theme.palette` configuration unchanged
- Existing custom CSS unaffected (palette CSS is additive)

## Non-goals

- **Automated contrast validation during build**: Contrast checking for custom palettes is out of scope; WCAG AA compliance is documented as a guideline but not enforced
- **System preference detection (prefers-color-scheme)**: Auto-selecting palette based on OS/browser dark mode preference is deferred to future enhancement
- **Palette preview/hover states**: Interactive palette previews in the selector are considered a future enhancement
- **Multiple selector instances**: Supporting palette selector in multiple locations (nav, footer, sidebar) simultaneously is out of scope
- **Lazy-loading palette CSS**: Static site architecture requires all palette CSS to be pre-linked; dynamic loading is not possible
- **CDN-hosted palette URLs**: Only relative file paths supported initially; external URLs are a future enhancement
- **Runtime palette creation**: All palettes must be defined at build time; dynamic palette generation is not supported
