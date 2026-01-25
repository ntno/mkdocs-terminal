# Implementation Tasks: Add Accessibility Tests

Change ID: `add-accessibility-tests`

## Overview

Implementation tasks for adding automated accessibility testing to the Terminal for MkDocs theme.

## Task Checklist

### Phase 1: Infrastructure & Setup

_Status: ✅ Complete — finished during Phase 1 bring-up; no remaining work tracked here._

- [x] Review and document accessibility library choices (axe-core vs pytest-a11y vs custom)
- [x] Update `pyproject.toml` with accessibility testing dependencies
- [x] Update `requirements.test.txt` with new test dependencies
- [x] Create `tests/accessibility/` directory structure
- [x] Create `tests/accessibility/__init__.py`
- [x] Create dedicated validator modules under `tests/accessibility/validators/` (HTML, ARIA, contrast) and retire the interim `utils.py` facade

### Phase 2: HTML & Semantic Validation

_Status: ✅ Complete — semantic tests land with known nav aria-label skip awaiting template fix._

- [x] Create `tests/accessibility/test_html_validation.py`
- [x] Implement HTML5 structure validation tests
- [x] Add tests for semantic HTML elements (headings, nav, main, etc.)
- [x] Add tests to verify required HTML attributes
- [x] Document HTML validation requirements in test docstrings

### Phase 3: ARIA & Semantic Attributes

_Status: ⚠️ In progress — buttons/modals/forms/links covered; landmarks/live regions/complex associations pending._

- [x] Create `tests/accessibility/test_aria.py` (note: named test_aria.py, not test_aria_attributes.py)
- [x] Implement ARIA attribute validation tests (buttons, modal, forms, links)
- [x] Add tests for ARIA roles on interactive elements (button text/aria-label, modal role/aria-modal)
- [x] Add tests for aria-label and aria-labelledby usage (modal, search input, form inputs)
- [x] Add tests for aria-hidden on decorative elements (validation, updated to reflect aria-label preference)
- [x] Add utility functions: validate_modal_accessibility, validate_form_labels, validate_link_text
- [x] Improve validate_aria_hidden to encourage aria-label pattern instead of sr-only
- [ ] Add ARIA role coverage for navigation landmarks (nav/header/footer/aside) and ensure skip-link destinations advertise roles/labels
- [ ] Validate aria-live and status regions for dynamic components (search modal results, alerts)
- [ ] Add assertions for aria-describedby relationships on complex controls (e.g., alert banners, search inputs)

### Phase 4: Color Contrast & Visual Accessibility

_Status: ⚠️ In progress — contrast suite implemented (tests currently fail on five palettes until remediated)._ 

- [x] Create `tests/accessibility/test_color_contrast.py`
- [x] Implement color contrast ratio validation (WCAG AA standard)
- [x] Add tests for text color vs background
- [x] Add palette fixture + utilities (`palette_loader.py`, `ColorCombinationTracker`, `BackgroundColorResolver`)
- [ ] Add tests for focus indicators / outlines / hover states (requires DOM simulation or browser automation)
- [ ] Document color contrast expectations and remediation guidance in developer docs
- [ ] Track and remediate failing palettes (default, pink, sans, gruvbox_dark) or add follow-up issues before merge

### Phase 5: Theme Accessibility

_Status: ❌ Not started — keyboard navigation and focus checks still to be scoped._

- [ ] Verify theme templates support keyboard navigation
- [ ] Add tests for keyboard focus indicators (visible focus states)
- [ ] Verify skip-to-content links work properly
- [ ] Test that interactive elements are keyboard accessible (search, navigation, modals)
- [ ] Document theme-specific accessibility requirements

### Phase 6: Test Coverage & Documentation

_Status: ❌ Not started — coverage baseline and contributor docs outstanding._

- [ ] Ensure test coverage reaches 80%+ for accessibility tests
- [ ] Create developer documentation for adding new accessibility checks to theme
- [ ] Document known limitations: tests validate theme only, not user content
- [ ] Add examples of how to write accessibility checks for theme components
- [ ] Update main README or CONTRIBUTING with accessibility testing info

### Phase 7: CI/CD Integration

_Status: ⚠️ Partial — tests wired into pytest/make flows, but CI + multi-runtime verification still open._

- [ ] Verify accessibility tests run in CI pipeline
- [ ] Ensure tests pass on all supported Python versions (3.8-3.12)
- [ ] Ensure tests pass on all supported OS (ubuntu, macOS, windows)
- [ ] Document how to run accessibility tests locally
- [ ] Add accessibility test results to CI artifacts if needed

### Phase 8: Validation & Cleanup

_Status: ❌ Not started — final validation steps deferred until earlier phases close._

- [ ] Run full test suite to ensure no regressions
- [ ] Verify all accessibility tests pass locally
- [ ] Validate that accessibility issues in templates are properly detected
- [ ] Review test code for maintainability and clarity
- [ ] Final review before merge

## Notes

- Tests should be runnable independently: `pytest tests/accessibility/`
- Integration with existing test infrastructure and fixtures is required
- All new tests must follow existing test patterns in the project
- Use example configurations from `tests/examples/` for validation targets

## Phase 3 Implementation Details

**Completed:** January 20-21, 2026

### Test Classes Created

1. **TestARIAButtons** — Button accessibility
   - `test_buttons_have_text_or_aria_label()` — Validates all buttons have accessible names
   - Verifies test configuration (requires buttons to exist)

2. **TestARIAAttributes** — ARIA attribute usage
   - `test_aria_hidden_only_on_decorative()` — Validates aria-hidden only on text-free elements
   - Verifies test configuration (requires aria-hidden elements to exist)

3. **TestModalAccessibility** — Search modal ARIA compliance
   - `test_modal_has_correct_aria_attributes()` — Validates modal role, aria-modal, aria-labelledby, close button aria-label, search input labeling
   - Verifies test configuration (requires modal to exist)

4. **TestFormAccessibility** — Form input labeling
   - `test_form_inputs_have_labels()` — Validates all form inputs have label associations (label, aria-label, aria-labelledby)
   - Verifies test configuration (requires form inputs to exist)

5. **TestLinkAccessibility** — Theme region link clarity
   - `test_theme_links_have_text_or_aria_label()` — Validates nav/header/footer/aside links have descriptive text or aria-label
   - Validates each nav element individually to catch empty nav elements
   - Verifies test configuration (requires nav links to exist)

### Utility Functions Added

1. **validate_modal_accessibility()** — Modal ARIA validation
   - Checks: role, aria-modal, aria-labelledby, close button aria-label, search input aria-labelledby

2. **validate_form_labels()** — Form input labeling
   - Checks: label associations, aria-label, aria-labelledby, title fallback

3. **validate_link_text()** — Link accessibility
   - Checks: scoped to theme regions (nav, header, footer, aside)
   - Ensures links have text or aria-label

4. **validate_aria_hidden()** — Improved decorator element validation
   - Simplified from sr-only pattern check to strict decorative-only validation
   - Encourages aria-label approach for icon buttons

### Key Improvements

- **Test Robustness:** All tests now verify test configuration first (hard fail if expected elements not found)
- **Granular Validation:** Link test validates each nav element individually (catches empty nav issues)
- **WCAG Alignment:** Tests follow WCAG 2.1 AA standards and ARIA APG patterns
- **Clear Error Messages:** All assertions provide specific guidance on configuration errors
- **Template Fixes:** Removed empty nav element from top-nav/menu.html (semantic correctness)
- Keep accessibility checks maintainable — prefer standard checks over custom validation

### Remaining Gaps

- Landmark navigation roles still need explicit assertions (aria-label / aria-labelledby on multiple navs, skip-link destinations)
- Dynamic regions (search results, alert banners) should expose `aria-live` or appropriate descriptions
- Composite controls (search input, modal close button) would benefit from aria-describedby coverage

## Phase 4 Implementation Details

**Current Focus:** Site-wide contrast validation is implemented and actively surfacing real palette defects (run completed January 24, 2026).

### Files Created / Updated

1. **tests/accessibility/utilities/color_utils.py** — Shared color handling library
   - Parses hex/rgb/hsl/named colors, computes relative luminance + contrast ratios, and exposes `meets_wcag_aa()`.

2. **tests/accessibility/utilities/palette_loader.py** — Palette fixtures
   - Loads every CSS palette file plus the fallback theme CSS, caches results, and feeds parametrized tests via `load_all_palette_css_attributes()`.

3. **tests/accessibility/validators/contrast_validator.py** — Contrast helpers
   - Hosts `PaletteColors`, `assert_contrast_meets_wcag_aa()`, `ColorCombinationTracker`, `BackgroundColorResolver`, and `validate_color_contrast()`.

4. **tests/accessibility/test_color_contrast.py** — Integration + palette tests
   - Exercises built sites across all palettes (body text, arbitrary text nodes, buttons/forms, alerts, CSS extraction) and palette-only assertions (primary/error colors, regression ratios).

5. **tests/accessibility/test_color_utils.py** — Unit coverage for parsing/luminance logic (33 tests spanning parsing, luminance, ratios, WCAG thresholds, CSS extraction).

### Utility + Fixture Updates

- `SiteContextBuilder` + new `built_example_site_with_palette` fixture share palette-aware site builds across tests.
- Palette CSS attributes are cached via `palette_loader`, dramatically reducing repeated IO.
- `validate_color_contrast()` moved out of the deprecated `utils.py` file into `contrast_validator.py` and now leverages `_get_element_computed_styles()` throughout.

### Key Implementation Decisions

- Continue relying on the in-repo WCAG math instead of external dependencies to minimize supply-chain risk.
- Focus current coverage on static, theme-controlled colors (body text, links, buttons, alerts) while documenting hover/focus limitations.
- Track exact foreground/background pairs so designers receive actionable violation summaries.

### Test Results (2026-01-24)

`pytest tests/accessibility/ -v` → 120 passed, 1 skipped, 5 expected failures:

1. `test_primary_link_color_meets_wcag_aa[default]`
2. `test_primary_link_color_meets_wcag_aa[pink]`
3. `test_primary_link_color_meets_wcag_aa[sans]`
4. `test_alert_error_color_meets_wcag_aa[gruvbox_dark]`
5. `test_ghost_error_button_color_meets_wcag_aa[gruvbox_dark]`

These failures reflect real WCAG AA contrast gaps in the current palette values and must be addressed (or excepted with justification) before closing Phase 4.
