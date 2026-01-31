# Implementation Tasks: Color Palette Toggle

Change ID: `color-palette-toggle`

## Overview

Implementation tasks for adding an optional, built-in color palette selector to the `mkdocs-terminal` theme. This feature allows site visitors to choose between configured palette options (dark, light, named palettes) with localStorage persistence.

**Specification:** [2026-01-18-color-palette-toggle.md](./2026-01-18-color-palette-toggle.md)

### Static Site Architecture Impact

**Critical Constraint:** MkDocs generates static HTML sites. All pages are pre-rendered once during the build process.

**Implications:**

1. **Build-time vs Runtime:**
   - Configuration processing: **Build-time only** (mkdocs.yml is read during `mkdocs build`)
   - Palette validation: **Build-time only** (must verify CSS files exist before generating HTML)
   - Template rendering: **Build-time only** (Jinja templates → static HTML once)
   - Palette switching: **Runtime only** (JavaScript modifies DOM in user's browser)

2. **No Server-Side Logic:**
   - Cannot dynamically fetch palette CSS files on demand
   - Cannot validate user's localStorage selection server-side
   - All palette CSS files must be included in built site assets
   - All selector options must be pre-rendered into the static HTML

3. **JavaScript is Essential (for switching only):**
   - Default palette works without JavaScript (rendered in HTML at build time)
   - User preference switching requires JavaScript (changes data-palette attribute)
   - localStorage persistence is purely client-side
   - No server to coordinate state across page loads

4. **Template Context:**
   - Configuration available via Jinja2 context during build
   - Must embed selector options as data attributes or JSON in HTML
   - JavaScript reads embedded data to know available palettes

5. **CSS Asset Management:**
   - All palette CSS files must be linked in <head> at build time
   - MkDocs handles copying CSS to build output (via extra_css or theme files)
   - Palette switching is CSS scoping via data attribute, not file loading
   - Cannot lazy-load CSS files (no server to fetch from)

**Simplified Mental Model:**
- **Build phase (Python/Jinja):** Validate config → render static HTML with all palettes embedded → copy assets
- **Runtime phase (Browser/JS):** Read localStorage → change data-palette attribute → CSS scoping handles visual change

## Task Checklist

### Phase 1: Configuration Schema & Validation

_Status: ❌ Not started — foundation for all subsequent work._

- [ ] Define configuration schema structure in theme code (build-time processing)
  - [ ] Add `ThemePaletteConfig` class/dataclass to handle palette configuration
  - [ ] Support legacy string format: `palette: "dark"` → normalize to object shape
  - [ ] Support new object format with `default`, `selector.enabled`, `selector.ui`, `selector.options`
  - [ ] Add configuration validation during MkDocs build (not runtime - static site has no runtime server)
  - [ ] Hook into MkDocs theme's `on_config` or equivalent event to process palette config early
- [ ] Implement palette option validation (build-time only)
  - [ ] Validate bundled palette names against available CSS files in `terminal/css/palettes/`
  - [ ] Validate custom palette entries (name + css path)
  - [ ] Check custom CSS files exist in `config.extra_css` (checked during mkdocs build)
  - [ ] Emit build warnings (via MkDocs logging) for missing/invalid palettes
  - [ ] Filter out invalid options from selector UI during template rendering
  - [ ] **Critical:** All validation must complete before templates render (no runtime validation possible)
- [ ] Add configuration normalization logic
  - [ ] Convert legacy string config to new object shape internally
  - [ ] Set defaults: `selector.enabled: false`, `selector.ui: "auto"`
  - [ ] Ensure normalized config is available to Jinja template context (for HTML rendering)
  - [ ] Ensure palette options are embedded in HTML for JavaScript access (as data attributes or JSON)
- [ ] Document configuration schema
  - [ ] Add inline code documentation/docstrings
  - [ ] Create configuration reference in `documentation/docs/configuration/`

**Dependencies:** None  
**Blocks:** Phase 2, 3, 4, 5

**Acceptance:**
- Configuration loads successfully for both legacy and new formats
- Invalid palette options are filtered with appropriate warnings
- Normalized config structure is available to template context

---

### Phase 2: CSS Architecture & Palette Files

_Status: ❌ Not started — establishes theming foundation._

- [ ] Review existing palette files in `terminal/css/palettes/`
  - [ ] Audit current palette CSS structure (9 existing: blueberry, dark, default, gruvbox_dark, lightyear, pink, red_drum, sans, sans_dark)
  - [ ] Document current CSS variable patterns used across palettes
  - [ ] Identify missing or inconsistent variables
- [ ] Standardize palette CSS structure
  - [ ] Define complete CSS custom property set for all theme elements
  - [ ] Create CSS variable naming convention (e.g., `--terminal-color-primary`, `--terminal-bg-body`)
  - [ ] Update all existing palette files to use standardized variables
  - [ ] Document required CSS variables for custom palettes
- [ ] Implement palette application mechanism
  - [ ] Add CSS to scope palette styles under `[data-palette="<name>"]` attribute selector
  - [ ] Ensure all palette CSS files are linked in <head> at build time (cannot lazy-load - static site)
  - [ ] Use CSS scoping to show/hide palette-specific styles based on data-palette attribute
  - [ ] Add fallback for no-JS environments (render default palette's data-palette attribute in HTML)
  - [ ] Avoid FOUC: inline critical JS in <head> to apply localStorage palette before first paint
- [ ] Create palette documentation
  - [ ] Document CSS variable structure for palette authors
  - [ ] Provide example custom palette file
  - [ ] Add WCAG AA contrast requirements to palette guidelines

**Dependencies:** Phase 1  
**Blocks:** Phase 3, 4

**Acceptance:**
- All bundled palettes use consistent CSS variable structure
- Palette switching mechanism works via data attribute
- Documentation exists for creating custom palettes
- No visual flash when switching palettes

---

### Phase 3: Template Implementation

_Status: ❌ Not started — UI surface for user interaction._

- [ ] Create `terminal/partials/palette_selector.html` partial
  - [ ] Implement conditional rendering based on `theme.palette.selector.enabled`
  - [ ] Render UI based on `selector.ui` setting and option count
  - [ ] Binary toggle UI for 2 options (when `ui: auto` or `ui: toggle`)
  - [ ] Select/dropdown UI for >2 options (when `ui: auto` or `ui: select`)
  - [ ] Fallback behavior when `ui: toggle` with >2 options (use select, emit build warning)
  - [ ] Add ARIA attributes for accessibility (role, labels, keyboard navigation)
  - [ ] Embed available palette options as data attributes (e.g., `data-palettes='["dark","light"]'`) for JS
- [ ] Create Jinja block for override capability
  - [ ] Add `{% block palette_selector %}{% endblock %}` in appropriate location
  - [ ] Ensure block includes default partial implementation
  - [ ] Test override mechanism via `theme.custom_dir`
- [ ] Integrate selector into theme layout
  - [ ] Add selector to `terminal/partials/top-nav` or appropriate partial
  - [ ] Ensure selector placement is consistent and accessible
  - [ ] Add data attributes for JavaScript hooks (`data-palette-selector`, `data-palette-option`)
- [ ] Build-time default palette application ("server-side" for static sites)
  - [ ] Apply `data-palette` attribute to `<html>` element based on config default during template rendering
  - [ ] Ensure default palette renders correctly without JavaScript (static HTML includes data-palette)
  - [ ] Ensure all palette CSS files are already linked in <head> (no dynamic loading)
- [ ] Update theme templates for palette CSS variable usage
  - [ ] Replace hardcoded colors with CSS variables where needed
  - [ ] Test all theme components render correctly with each bundled palette

**Dependencies:** Phase 1, Phase 2  
**Blocks:** Phase 4, 5

**Acceptance:**
- Selector UI renders when enabled, hidden when disabled
- UI adapts correctly based on `selector.ui` and option count
- Server-side default palette works without JavaScript
- Override mechanism allows custom selector implementations
- All ARIA attributes present for screen reader support

---

### Phase 4: JavaScript Implementation

_Status: ❌ Not started — client-side interactivity and persistence._

- [ ] Create `terminal/js/palette_selector.js` script
  - [ ] Implement event listeners for selector UI (click/change handlers)
  - [ ] Apply palette by setting `data-palette` attribute on `<html>` element
  - [ ] Remove previous palette data attribute before applying new one
  - [ ] Handle edge cases (missing options, invalid selections)
- [ ] Implement localStorage persistence
  - [ ] Save user selection to `localStorage` on palette change
  - [ ] Read saved selection on page load
  - [ ] Validate saved selection against available options
  - [ ] Fallback to config default if saved selection invalid
- [ ] Add palette restoration logic
  - [ ] Check localStorage on DOMContentLoaded or earlier (inline script in <head>)
  - [ ] Apply saved palette before first paint to avoid FOUC
  - [ ] Validate saved palette exists in available options (read from data attribute)
  - [ ] Fallback to build-time default if saved palette is invalid/unavailable
- [ ] **No dynamic CSS loading** (static site constraint)
  - [ ] All palette CSS files must be pre-linked in <head> during build
  - [ ] Palette switching only changes data-palette attribute (CSS scoping handles visual change)
  - [ ] Cannot fetch CSS files on demand (no server)
- [ ] Add developer console logging
  - [ ] Log palette switches (info level)
  - [ ] Log validation warnings (warn level)
  - [ ] Log errors (error level)
  - [ ] Make logging optional/configurable

**Dependencies:** Phase 3  
**Blocks:** Phase 5, 6

**Acceptance:**
- Palette switches immediately on user interaction
- Selection persists across page navigation and browser sessions
- No FOUC when restoring saved palette
- Invalid saved selections fallback gracefully to default
- Console logging aids debugging without being verbose

---

### Phase 5: Testing

_Status: ❌ Not started — ensure quality and prevent regressions._

- [ ] Unit tests for configuration validation (build-time logic)
  - [ ] Test legacy string config normalization during theme initialization
  - [ ] Test new object config parsing
  - [ ] Test invalid palette option filtering at build time
  - [ ] Test build warning emission for misconfigured options (via MkDocs logging)
  - [ ] Test custom palette CSS path validation against extra_css list
  - [ ] Test that invalid palettes are excluded from rendered HTML
- [ ] Integration tests for template rendering (static HTML output)
  - [ ] Test selector renders in HTML when enabled
  - [ ] Test selector absent from HTML when disabled
  - [ ] Test binary toggle UI markup with 2 options
  - [ ] Test select UI markup with >2 options
  - [ ] Test `ui: auto` logic produces correct HTML
  - [ ] Test `ui: toggle` and `ui: select` explicit settings
  - [ ] Test build-time default palette application (data-palette in <html>)
  - [ ] Test palette options embedded in HTML data attributes
  - [ ] Test all palette CSS files linked in <head>
- [ ] Integration tests for JavaScript behavior
  - [ ] Test palette switching updates data attribute
  - [ ] Test localStorage save/restore
  - [ ] Test invalid saved selection handling
  - [ ] Test palette restoration on page load
  - [ ] Mock localStorage for testing
- [ ] Accessibility tests
  - [ ] Test selector has proper ARIA attributes
  - [ ] Test keyboard navigation works
  - [ ] Test screen reader announcements (manual or automated)
  - [ ] Test focus indicators visible
  - [ ] Verify bundled palettes meet WCAG AA contrast (leverage existing accessibility tests from `tests/accessibility/test_color_contrast.py`)
- [ ] Visual regression tests
  - [ ] Test each bundled palette renders correctly
  - [ ] Test custom palette integration
  - [ ] Smoke test major theme components with each palette
- [ ] Browser compatibility tests
  - [ ] Test in modern browsers (Chrome, Firefox, Safari, Edge)
  - [ ] Test localStorage behavior across browsers
  - [ ] Test CSS custom property support
  - [ ] Verify no-JS fallback works

**Dependencies:** Phase 1, 2, 3, 4  
**Blocks:** Phase 7

**Acceptance:**
- Test coverage ≥80% for new code
- All tests pass in CI pipeline
- Accessibility tests validate ARIA compliance
- Visual tests catch palette rendering issues
- No regressions in existing theme functionality

---

### Phase 6: Documentation

_Status: ❌ Not started — enable users to adopt the feature._

- [ ] User-facing configuration documentation
  - [ ] Create `documentation/docs/configuration/palette-selector.md`
  - [ ] Document `theme.palette` configuration schema
  - [ ] Provide examples: minimal, multi-palette, custom palettes
  - [ ] Explain `selector.ui` options and their behavior
  - [ ] Document legacy string config support
  - [ ] Add troubleshooting section for common issues
- [ ] Custom palette creation guide
  - [ ] Document required CSS variables
  - [ ] Provide complete example custom palette CSS file
  - [ ] Explain how to register custom palettes in `mkdocs.yml`
  - [ ] Document `extra_css` requirement for custom files
  - [ ] Add WCAG AA contrast guidelines for palette authors
- [ ] Override documentation
  - [ ] Document how to override `palette_selector.html` partial
  - [ ] Provide example custom selector implementation
  - [ ] Document available Jinja context variables
  - [ ] Show how to access `selector.options` in custom templates
- [ ] Update existing documentation
  - [ ] Add palette selector to main README.md
  - [ ] Update theme features list
  - [ ] Add palette selector to configuration overview in `documentation/docs/configuration/`
  - [ ] Link to palette selector from relevant sections
- [ ] Developer documentation
  - [ ] Document CSS variable architecture
  - [ ] Explain palette application mechanism
  - [ ] Document JavaScript API (if exposing any hooks)
  - [ ] Add section to DEVELOPER_README.md if needed
- [ ] Create live examples
  - [ ] Add palette selector to documentation site (`documentation/`)
  - [ ] Include examples in `tests/examples/` for testing
  - [ ] Create example with custom palette

**Dependencies:** Phase 1, 2, 3, 4  
**Blocks:** Phase 7

**Acceptance:**
- Users can configure palette selector without referencing code
- Custom palette creation process is clear and documented
- Override mechanism is documented with examples
- Documentation site demonstrates the feature live
- All examples are tested and working

---

### Phase 7: CI/CD & Release

_Status: ❌ Not started — prepare for production deployment._

- [ ] Verify CI/CD pipeline integration
  - [ ] Ensure all new tests run in CI
  - [ ] Verify tests pass on all supported Python versions (3.8-3.12)
  - [ ] Verify tests pass on all supported OS (Ubuntu, macOS, Windows)
  - [ ] Add any new test dependencies to CI configuration
- [ ] Performance validation
  - [ ] Measure JavaScript bundle size impact
  - [ ] Verify CSS file size is reasonable
  - [ ] Test page load performance with palette selector
  - [ ] Ensure no blocking behavior during palette application
- [ ] Create migration guide (if needed)
  - [ ] Document any breaking changes (none expected)
  - [ ] Provide upgrade instructions from previous versions
  - [ ] Explain new configuration options
- [ ] Prepare release artifacts
  - [ ] Update CHANGELOG.md with feature description
  - [ ] Bump version number (minor version for new feature)
  - [ ] Tag release in git
  - [ ] Create release notes highlighting palette selector
- [ ] Post-release validation
  - [ ] Test installation from PyPI
  - [ ] Verify documentation builds and deploys correctly
  - [ ] Monitor for user-reported issues

**Dependencies:** Phase 5, 6  
**Blocks:** None

**Acceptance:**
- All CI tests pass
- Release is tagged and published
- Documentation is live
- Feature is available to users via standard installation

---

### Phase 8: Follow-up & Enhancements (Optional/Future)

_Status: ❌ Future work — nice-to-have improvements._

- [ ] Enhanced UI options
  - [ ] Add palette preview swatches in selector
  - [ ] Implement smooth transition animations between palettes
  - [ ] Add palette preview mode (hover to preview, click to apply)
- [ ] Additional selector positions
  - [ ] Allow configuring selector location (top-nav, side-nav, footer)
  - [ ] Support multiple selector instances on same page
- [ ] Accessibility enhancements
  - [ ] Add prefers-color-scheme media query support
  - [ ] Auto-select palette based on system preference
  - [ ] Provide high-contrast palette option
- [ ] Developer experience
  - [ ] Add CLI tool to validate palette CSS files
  - [ ] Create palette generator/starter template
  - [ ] Add palette preview page for theme development
- [ ] Performance optimizations
  - [ ] Implement CSS-in-JS for palette switching (if beneficial)
  - [ ] Lazy-load palette CSS files on demand
  - [ ] Optimize CSS variable inheritance

**Dependencies:** Phase 7  
**Blocks:** None

**Acceptance:**
- Enhancements evaluated based on user feedback
- Features implemented as minor releases or patches
- No regressions to core palette selector functionality

---

## Implementation Notes

### Critical Dependencies

- **Phase 1** must complete first — all other phases depend on configuration schema
- **Phase 2** establishes CSS foundation — required before template/JS work
- **Phase 3 & 4** are coupled — templates provide UI hooks for JavaScript
- **Phase 5 & 6** can proceed in parallel once Phase 4 completes
- **Phase 7** requires Phase 5 & 6 to complete

### Risk Areas

1. **Static Site Architecture Constraints**
   - All configuration processing must happen at build time (no runtime server)
   - Cannot dynamically load CSS files (must pre-link all palettes)
   - Cannot validate localStorage selections server-side (client-side JS only)
   - Templates render once to static HTML (no dynamic content generation)

2. **FOUC (Flash of Unstyled Content)**
   - **CRITICAL for static sites:** Cannot apply localStorage palette server-side
   - Must inline palette restoration JS in `<head>` (before CSS loads)
   - localStorage read must happen before first paint
   - Default palette in HTML prevents blank page if JS fails

3. **Backwards Compatibility**
   - Legacy string config must continue working indefinitely (normalized at build time)
   - Existing sites with custom CSS must not break (palette CSS is additive)
   - Theme updates should not require mkdocs.yml changes
   - Sites without palette config should build identically to current behavior

4. **Accessibility**
   - Selector must be fully keyboard accessible
   - ARIA attributes critical for screen reader support
   - Palette contrast must meet WCAG AA standards
   - Focus indicators must be visible in all palettes

5. **Performance**
   - Multiple palette CSS files could increase page weight
   - CSS custom properties have good browser support but verify performance
   - localStorage operations should be synchronous but fast

### Development Workflow

1. Create feature branch: `feature/color-palette-toggle`
2. Work through phases sequentially (1 → 2 → 3 → 4 → 5 → 6 → 7)
3. Commit after each major milestone within a phase
4. Run full test suite before moving to next phase
5. Create PR for review before Phase 7 (release)

### Testing Strategy

- **Unit tests:** Configuration validation, helper functions
- **Integration tests:** Template rendering, JS behavior, localStorage
- **Accessibility tests:** ARIA compliance, keyboard navigation, contrast (leverage existing `tests/accessibility/` infrastructure)
- **Visual tests:** Smoke test each palette with major components
- **Manual tests:** Browser compatibility, no-JS fallback, override mechanism

### Success Criteria

- ✅ Feature works with zero configuration (default: selector disabled)
- ✅ Legacy config format continues working
- ✅ Users can add selector with minimal `mkdocs.yml` changes
- ✅ Custom palettes can be added without theme modification
- ✅ Selector UI is accessible (keyboard, screen readers)
- ✅ Selection persists across sessions
- ✅ No JavaScript required for default palette
- ✅ All bundled palettes meet WCAG AA contrast
- ✅ Documentation enables self-service adoption
- ✅ No regressions in existing theme functionality

## Related Work

- **Accessibility Testing:** Existing `tests/accessibility/test_color_contrast.py` can validate palette WCAG compliance
- **Palette Files:** Nine palettes already exist in `terminal/css/palettes/` — audit and standardize these first
- **Theme Blocks:** Document palette_selector override in `documentation/docs/configuration/blocks.md` (create if needed)

## Open Questions

1. **Inline JS for FOUC prevention?**
   - **Decision: YES** — Must inline palette restoration JS in `<head>` to prevent flash
   - Trade-off: Slightly larger HTML (minor) vs better UX (critical for static site)
   - Static sites cannot apply localStorage palette server-side, so inline JS is required

2. ~~**Palette CSS loading strategy?**~~ **RESOLVED by static site constraint**
   - **Must load all palette CSS files upfront** (only option for static sites)
   - Cannot fetch CSS on demand (no server to fetch from)
   - All CSS linked in <head> during build, switching via data-palette attribute

3. ~~**Configuration validation timing?**~~ **RESOLVED by static site constraint**
   - **Must validate at build time only** (no runtime server)
   - MkDocs build emits warnings for invalid palettes
   - JavaScript validates localStorage selections against embedded options (client-side fallback)

4. **Custom palette file paths** — **Decision: Relative paths only (v1)**
   - **Support relative paths only** for initial implementation (simpler, covers 95% of use cases)
   - Paths resolved relative to docs directory or theme static directory
   - Custom palette CSS files must also be listed in `extra_css` for MkDocs to copy them
   - **Future enhancement:** CDN URLs for externally-hosted palettes (low priority, adds complexity)

5. **CSS file inclusion strategy** — **Decision: Smart auto-include**
   - **Built-in palettes:** Automatically included when named in `selector.options`
     - User just lists palette names (e.g., `dark`, `light`, `gruvbox_dark`)
     - Theme automatically links the corresponding CSS files from `terminal/css/palettes/`
     - No need to list built-in palettes in `extra_css`
   - **Custom palettes:** Must be listed in `extra_css`
     - User provides name + css path in config
     - User must also add the CSS file to `extra_css` so MkDocs copies it
   - **Optimization:** Only include CSS for palettes actually listed in options (not all 9 bundled files)

## Timeline Estimate

- **Phase 1:** 2-3 days
- **Phase 2:** 3-4 days (includes palette standardization)
- **Phase 3:** 2-3 days
- **Phase 4:** 2-3 days
- **Phase 5:** 3-5 days (comprehensive testing)
- **Phase 6:** 2-3 days
- **Phase 7:** 1-2 days
- **Total:** ~15-23 days (3-4 weeks for one developer)

Adjust based on team size and familiarity with codebase.
