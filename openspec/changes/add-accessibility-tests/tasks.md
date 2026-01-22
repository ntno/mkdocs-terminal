# Implementation Tasks: Add Accessibility Tests

Change ID: `add-accessibility-tests`

## Overview

Implementation tasks for adding automated accessibility testing to the Terminal for MkDocs theme.

## Task Checklist

### Phase 1: Infrastructure & Setup

- [x] Review and document accessibility library choices (axe-core vs pytest-a11y vs custom)
- [x] Update `pyproject.toml` with accessibility testing dependencies
- [x] Update `requirements.test.txt` with new test dependencies
- [x] Create `tests/accessibility/` directory structure
- [x] Create `tests/accessibility/__init__.py`
- [x] Create `tests/accessibility/utils.py` with common accessibility check helpers

### Phase 2: HTML & Semantic Validation

- [x] Create `tests/accessibility/test_html_validation.py`
- [x] Implement HTML5 structure validation tests
- [x] Add tests for semantic HTML elements (headings, nav, main, etc.)
- [x] Add tests to verify required HTML attributes
- [x] Document HTML validation requirements in test docstrings

### Phase 3: ARIA & Semantic Attributes

- [x] Create `tests/accessibility/test_aria.py` (note: named test_aria.py, not test_aria_attributes.py)
- [x] Implement ARIA attribute validation tests (buttons, modal, forms, links)
- [x] Add tests for ARIA roles on interactive elements (button text/aria-label, modal role/aria-modal)
- [x] Add tests for aria-label and aria-labelledby usage (modal, search input, form inputs)
- [x] Add tests for aria-hidden on decorative elements (validation, updated to reflect aria-label preference)
- [x] Add utility functions: validate_modal_accessibility, validate_form_labels, validate_link_text
- [x] Improve validate_aria_hidden to encourage aria-label pattern instead of sr-only

### Phase 4: Color Contrast & Visual Accessibility

- [ ] Create `tests/accessibility/test_color_contrast.py`
- [ ] Implement color contrast ratio validation (WCAG AA standard)
- [ ] Add tests for text color vs background
- [ ] Add tests for focus indicators and visual clarity
- [ ] Document color contrast expectations

### Phase 5: Theme Accessibility

- [ ] Verify theme templates support keyboard navigation
- [ ] Add tests for keyboard focus indicators (visible focus states)
- [ ] Verify skip-to-content links work properly
- [ ] Test that interactive elements are keyboard accessible (search, navigation, modals)
- [ ] Document theme-specific accessibility requirements

### Phase 6: Test Coverage & Documentation

- [ ] Ensure test coverage reaches 80%+ for accessibility tests
- [ ] Create developer documentation for adding new accessibility checks to theme
- [ ] Document known limitations: tests validate theme only, not user content
- [ ] Add examples of how to write accessibility checks for theme components
- [ ] Update main README or CONTRIBUTING with accessibility testing info

### Phase 7: CI/CD Integration

- [ ] Verify accessibility tests run in CI pipeline
- [ ] Ensure tests pass on all supported Python versions (3.8-3.12)
- [ ] Ensure tests pass on all supported OS (ubuntu, macOS, windows)
- [ ] Document how to run accessibility tests locally
- [ ] Add accessibility test results to CI artifacts if needed

### Phase 8: Validation & Cleanup

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
