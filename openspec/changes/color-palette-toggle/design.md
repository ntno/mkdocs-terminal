# Color Palette Selector Design

## Context

The mkdocs-terminal theme is a static site generator theme for MkDocs that renders documentation sites with a retro terminal aesthetic. Currently, the theme supports multiple color palettes (9 bundled options in `terminal/css/palettes/`) but lacks runtime switching capability—users must edit `mkdocs.yml` and rebuild the site to change themes.

**Current State:**
- Static HTML generation via MkDocs (Python/Jinja2)
- All processing occurs at build time (`mkdocs build`)
- No runtime server or dynamic content generation
- Existing palettes implemented as standalone CSS files with hardcoded selectors
- No standardized CSS variable architecture across palettes

**Constraints:**
- **Static Site Architecture:** All configuration parsing, validation, and template rendering happens during build. No server-side logic at runtime.
- **No Dynamic Asset Loading:** All CSS files must be pre-linked in `<head>` at build time; browsers cannot fetch additional stylesheets on demand.
- **Browser-Only State:** Palette preference persistence must use client-side storage (localStorage); no server to track user state.
- **Backwards Compatibility:** Must support existing `palette: "string"` configuration format without breaking changes.
- **Accessibility:** All palettes must meet WCAG AA contrast standards; selector UI must be keyboard accessible with ARIA attributes.

**Stakeholders:**
- **Site Authors:** Configure palette options in `mkdocs.yml`
- **Site Visitors:** Select preferred palette via UI and have choice persisted
- **Theme Developers:** Maintain CSS architecture and build-time validation logic

## Goals / Non-Goals

**Goals:**
- Enable runtime palette switching without site rebuild
- Persist user preference across sessions via localStorage
- Support both bundled palettes and custom author-provided palettes
- Maintain backwards compatibility with existing `palette: "string"` configuration
- Provide build-time validation to catch misconfigured palettes early
- Prevent FOUC (Flash of Unstyled Content) when restoring saved palette on page load
- Adapt UI based on number of options (toggle for 2, select for >2)

**Non-Goals:**
- Automated contrast validation during build (WCAG AA compliance documented as guideline, not enforced)
- System preference detection (`prefers-color-scheme` media query integration)
- Palette preview/hover states in selector UI
- Multiple selector instances (nav + footer + sidebar simultaneously)
- Dynamic palette CSS loading or lazy-loading
- CDN-hosted or external URL palette sources
- Runtime palette creation or modification

## Decisions

### Decision 1: CSS Custom Properties Architecture

**Choice:** Migrate all palette CSS files to use CSS custom properties (variables) scoped under `[data-palette="<name>"]` attribute selectors.

**Rationale:**
- **Why this approach:** Enables palette switching by changing a single `data-palette` attribute on the `<html>` element, triggering cascading variable updates across the entire page. No need to load/unload stylesheets or manipulate multiple DOM elements.
- **Alternatives considered:**
  - **Class-based scoping (`class="palette-dark"`):** Works similarly but pollutes global class namespace; data attributes are semantically clearer for state management.
  - **Dynamic stylesheet loading:** Incompatible with static site constraint—no server to fetch CSS from; all assets must be pre-linked at build time.
  - **Inline style injection:** Poor performance (recalculating styles for thousands of elements); doesn't support pseudo-elements or media queries.

**Implementation:**
```css
/* Example: terminal/css/palettes/dark.css */
[data-palette="dark"] {
  --color-background: #1a1a1a;
  --color-text: #e0e0e0;
  --color-primary: #00ff00;
  /* ...other variables */
}

/* Theme CSS references variables */
body {
  background-color: var(--color-background);
  color: var(--color-text);
}
```

**Impact:** Requires refactoring all 9 existing palette CSS files to standardize variable names and scoping mechanism.

---

### Decision 2: Build-Time Validation Only

**Choice:** Validate all palette configuration during MkDocs build phase using `on_config` event hook. No runtime validation.

**Rationale:**
- **Why this approach:** Static site architecture has no runtime server to perform validation. Build-time validation provides immediate feedback to authors via MkDocs CLI warnings/errors before site deployment.
- **Alternatives considered:**
  - **Runtime validation in JavaScript:** Too late—users would see broken UI before JavaScript detects misconfiguration; cannot prevent deployment of broken sites.
  - **No validation:** Increases risk of silent failures (selector renders with missing palettes, custom CSS 404 errors).

**Validation Checks:**
1. Bundled palette names exist in `terminal/css/palettes/` directory
2. Custom palette CSS paths exist in `config.extra_css` list
3. `selector.ui` value is one of: `"auto"`, `"toggle"`, `"select"`
4. At least one valid palette option exists if selector is enabled

**Error Handling:**
- Invalid palette options are filtered out (with build warning)
- If all options invalid and selector enabled, emit error and disable selector
- Missing default palette falls back to first valid option

---

### Decision 3: Inline FOUC Prevention Script

**Choice:** Inject a small inline `<script>` in `<head>` (before CSS) to restore saved palette from localStorage synchronously.

**Rationale:**
- **Why this approach:** Prevents FOUC by setting `data-palette` attribute before browser parses CSS files. Inline scripts in `<head>` execute immediately; external scripts would load too late.
- **Alternatives considered:**
  - **External script in `<head>`:** Adds network round-trip delay; FOUC still possible during script fetch.
  - **Defer to main JavaScript bundle:** Executes after DOM parsing; guaranteed FOUC.
  - **Server-side rendering with cookie:** No server at runtime in static sites.

**Implementation:**
```html
<head>
  <script>
    (function() {
      var saved = localStorage.getItem('mkdocs-terminal-palette');
      if (saved) document.documentElement.setAttribute('data-palette', saved);
    })();
  </script>
  <!-- CSS links follow -->
</head>
```

**Size:** ~150 bytes (minified, gzipped: ~120 bytes). Acceptable overhead for FOUC prevention.

---

### Decision 4: Adaptive UI Selection

**Choice:** Automatically choose UI control type based on number of valid palette options:
- **2 options:** Binary toggle (button with icon swap)
- **3+ options:** Select dropdown

**Rationale:**
- **Why this approach:** Optimizes UX—toggles are faster for binary choices, dropdowns scale better for multiple options. "Auto" mode reduces author decision burden.
- **Alternatives considered:**
  - **Always use select:** Poor UX for common dark/light binary case (extra click to open dropdown).
  - **Always use toggle:** Doesn't scale—how to toggle between 5+ options?
  - **Radio buttons:** Requires more screen space; uncommon pattern for theme selectors.

**Author Override:** `selector.ui: "toggle"` or `selector.ui: "select"` forces specific control (with validation: toggle requires exactly 2 options).

---

### Decision 5: Pre-Link All Palette CSS Files

**Choice:** Link all configured palette CSS files in `<head>` during build, regardless of which palette is active. Switching occurs via CSS scoping, not asset loading.

**Rationale:**
- **Why this approach:** Static site constraint—no mechanism to dynamically load CSS files at runtime. All assets must be in the built site's output directory and referenced in HTML.
- **Alternatives considered:**
  - **Lazy-load CSS on palette change:** Requires server or CDN to fetch from; static sites have no server. Loading from relative paths in built site would still require pre-linking (browsers don't support conditional CSS loading without JavaScript hacks like creating `<link>` elements, which is slower and causes FOUC).

**Optimization:** Only link palettes that are explicitly configured in `selector.options`. Authors can minimize bloat by limiting enabled palettes (e.g., only dark + light instead of all 9 bundled options).

**Size Impact:** Each palette CSS file is ~1-2 KB. Worst case (all 9 bundled): ~18 KB total. Acceptable for documentation sites.

---

### Decision 6: localStorage-Only Persistence

**Choice:** Store palette preference exclusively in browser `localStorage` under key `mkdocs-terminal-palette`. No cookies, no server-side state.

**Rationale:**
- **Why this approach:** Static sites have no server to write cookies or database records. localStorage is the standard client-side persistence mechanism for preferences.
- **Alternatives considered:**
  - **Cookies:** Sent with every HTTP request (unnecessary overhead); requires server to read in dynamic sites (not applicable here).
  - **sessionStorage:** Doesn't persist across browser sessions; loses preference on tab close.
  - **IndexedDB:** Overkill for storing a single string value.

**Degradation:** If localStorage is unavailable (disabled, private browsing in some browsers), palette selection works during session but doesn't persist. Selector UI remains functional.

---

### Decision 7: Configuration Schema Normalization

**Choice:** Accept both legacy `palette: "string"` and new `palette: {object}` formats in `mkdocs.yml`. Normalize to object shape internally.

**Rationale:**
- **Why this approach:** Maintains backwards compatibility—existing sites continue working without config changes. New sites can opt into selector features.
- **Alternatives considered:**
  - **Deprecate string format:** Breaking change; requires migration guide and version bump. Violates project goal of non-breaking changes.
  - **Separate config key (`palette_selector`):** Confusing to have two palette-related keys; unclear interaction between `palette` and `palette_selector`.

**Normalization Logic:**
```python
# Legacy format
palette: "dark"
# Normalized to:
palette:
  default: "dark"
  selector:
    enabled: false
```

**Internal Representation:** `ThemePaletteConfig` dataclass with fields: `default`, `selector_enabled`, `selector_ui`, `options` (list of dicts with `name` and optional `css` path).

## Risks / Trade-offs

### Risk 1: CSS Custom Properties Not Fully Standardized Across Palettes
**Impact:** Existing palette CSS files use inconsistent class names and selectors. Refactoring to common variable names may miss edge cases.

**Mitigation:**
- Conduct palette-by-palette audit to identify all unique CSS selectors
- Extract comprehensive variable list covering: colors, typography, spacing, borders, shadows
- Add integration tests that render sample pages with each palette and verify key styles apply
- Document variable naming convention for future palette authors

---

### Risk 2: FOUC Prevention Script Execution Blocked
**Impact:** Some browsers or security policies (CSP without `unsafe-inline`) may block inline scripts, causing FOUC.

**Mitigation:**
- Document CSP configuration requirements if site uses Content Security Policy headers
- Provide fallback: default palette (from config) applies immediately via server-rendered `data-palette` attribute on `<html>`. FOUC only affects users with saved preferences.
- Future enhancement: Generate nonce-based CSP for inline script (requires build-time nonce injection)

---

### Risk 3: localStorage Quota or Availability Issues
**Impact:** Some browsers limit localStorage size (~5MB) or disable it (private browsing). Palette preference may not persist.

**Mitigation:**
- Graceful degradation: JavaScript checks `try { localStorage.setItem(...) }` and silently fails if unavailable
- Selector UI remains functional during session (changes apply but don't persist across page loads)
- Document known limitations in user-facing docs

---

### Risk 4: Custom Palette CSS Missing at Build Time
**Impact:** Authors configure custom palette but forget to add CSS file to `extra_css`. Selector renders with broken option.

**Mitigation:**
- Build-time validation checks custom CSS paths exist in `config.extra_css`
- Emit warning and filter invalid option from selector
- If no valid options remain, disable selector entirely and emit error

---

### Risk 5: Accessibility Gaps in Custom Palettes
**Impact:** Authors create custom palettes with insufficient color contrast, harming readability for users with visual impairments.

**Mitigation:**
- Document WCAG AA contrast requirements prominently in configuration guide
- Provide example palette template with annotated contrast ratios
- Defer automated contrast validation to future enhancement (out of scope for initial implementation)
- Bundled palettes validated via existing `tests/accessibility/test_color_contrast.py`

---

### Risk 6: JavaScript Bundle Size Growth
**Impact:** Adding palette selector JavaScript increases page load time for all visitors, even those who don't use the selector.

**Mitigation:**
- Keep selector JavaScript minimal (~2-3 KB uncompressed, ~1 KB gzipped)
- Conditionally include script only if `selector.enabled: true` (no cost for sites without selector)
- Use vanilla JavaScript (no framework dependencies)
- Inline FOUC script is separate and minimal (~150 bytes)

---

### Trade-off: Pre-Linking All Palettes vs. Load-on-Demand
**Chosen:** Pre-link all configured palettes in `<head>`

**Benefit:** Instant palette switching (no network delay); works in static sites (no server to fetch from).

**Cost:** Initial page load includes CSS for all configured palettes (~2 KB per palette). Authors with 9 palettes enabled add ~18 KB to every page.

**Justification:** Documentation sites typically have small asset sizes. 18 KB is acceptable overhead given instant switching UX and static site constraints. Authors can minimize by enabling only needed palettes (e.g., 2-3 options = 4-6 KB).

## Migration Plan

### Deployment Steps

**Phase 1: CSS Refactoring (No User Impact)**
1. Refactor bundled palette CSS files to use custom properties
2. Add scoping via `[data-palette="<name>"]` attributes
3. Test rendering with each palette—verify visual parity with existing theme
4. Deploy CSS changes in theme update (backwards compatible—no config changes)

**Phase 2: Configuration Schema (Opt-In Feature)**
1. Add `ThemePaletteConfig` class and validation logic
2. Implement `on_config` hook for build-time processing
3. Test configuration parsing and normalization
4. Deploy config system (sites without `selector.enabled` unaffected)

**Phase 3: Template & JavaScript (Feature Complete)**
1. Add `palette_selector.html` partial
2. Implement `palette_selector.js` client script
3. Integrate selector into top-nav template
4. Add inline FOUC prevention script
5. Deploy full feature (sites must set `selector.enabled: true` to opt in)

**Phase 4: Documentation & Release**
1. Publish configuration guide with examples
2. Update theme README and changelog
3. Tag release version (semantic versioning: minor bump for new feature)

### Rollback Strategy

**Scenario:** Critical bug discovered after release (e.g., JavaScript error breaks site navigation)

**Rollback:**
1. Set `selector.enabled: false` by default in theme code (disables feature globally)
2. Issue patch release with fix or feature disabled
3. Sites that explicitly enabled selector can revert config: remove `palette.selector` or set `enabled: false`

**Data Loss Risk:** None—localStorage persistence is additive. Disabling selector doesn't corrupt sites.

### Versioning

- **Initial Release:** Minor version bump (e.g., v1.4.0 → v1.5.0)—new feature, no breaking changes
- **Future Breaking Change:** If palette CSS variable names change incompatibly, major version bump (e.g., v1.5.0 → v2.0.0)

## Open Questions

1. **Should the selector UI be keyboard navigable via custom key bindings (e.g., Ctrl+P for palette)?**
   - Current design: Standard keyboard navigation (Tab, Enter, arrow keys)
   - Alternative: Add global keyboard shortcut for power users
   - Resolution: Defer to user testing feedback post-launch

2. **How to handle palette selector on mobile devices with limited screen space?**
   - Current design: Same UI as desktop (toggle or select)
   - Alternative: Collapse into hamburger menu or modal
   - Resolution: Test on mobile breakpoints; may need responsive adjustments

3. **Should palette option labels be translatable via MkDocs i18n?**
   - Current design: Palette names from config displayed as-is
   - Alternative: Support i18n keys for palette labels (e.g., `dark: { label: "theme.dark" }`)
   - Resolution: Defer to future enhancement—requires i18n infrastructure analysis

4. **What happens if a user's saved palette is no longer available (author removed it from config)?**
   - Current design: Fall back to configured default palette
   - Alternative: Show notification to user that preference is invalid
   - Resolution: Silent fallback is less disruptive; document behavior for authors
