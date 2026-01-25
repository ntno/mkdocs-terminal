# Proposal: Add Accessibility Tests

**Change ID:** `add-accessibility-tests`

**Status:** Pending Review

**Created:** 2026-01-19

## Summary

Add automated accessibility testing to ensure the Terminal for MkDocs theme maintains WCAG 2.1 AA compliance and follows web accessibility best practices. This includes HTML validation, semantic structure verification, ARIA attribute checks, and color contrast validation of theme components only.

## Motivation

The Terminal for MkDocs theme provides HTML structure and styling that impacts accessibility across all documentation sites using it. Currently, there are no automated tests to verify the theme itself is accessible:

1. Verify WCAG 2.1 compliance standards for theme HTML and styling
2. Validate semantic HTML structure of theme templates
3. Check ARIA attributes on theme interactive components (nav, search, modals)
4. Ensure color contrast meets accessibility standards in theme CSS
5. Verify theme templates support keyboard navigation

These gaps risk shipping an inaccessible theme that would affect all users of Terminal for MkDocs. However, validation of user-provided site content (like page headings and form fields in user documentation) is explicitly out of scope—those are the responsibility of site authors, not the theme.

## Scope

### Capabilities Affected

This change creates a new testing capability for accessibility validation:

- **Testing** — Add accessibility-focused test suite

### What's Included

1. **New test file:** `tests/accessibility/` directory with accessibility validation tests
2. **Test utilities:** Helper functions for common accessibility checks
3. **CI integration:** Accessibility tests run as part of the standard test suite (via pytest)
4. **Documentation:** Developer guide for writing and maintaining accessibility tests

### What's Out of Scope

- Fixing existing accessibility issues (separate work)
- Runtime accessibility enforcement (only testing)
- Browser-based GUI testing (only static analysis)
- Internationalization/localization accessibility (future phase)
- **Validation of user-provided content** — Site authors are responsible for accessible page structure, headings, forms, and content. Tests validate the theme structure only, not user content.

## Technical Design

### Testing Strategy

Accessibility tests will use a multi-layered approach focused on theme components:

1. **HTML Validation** — Use `html5lib` to validate semantic HTML5 structure of theme templates
2. **ARIA Validation** — Check ARIA attributes on theme interactive components (navigation, search, modals, buttons)
3. **Color Contrast** — Validate text/background contrast ratios in theme CSS meet WCAG AA standards (body text, links, buttons, form controls)
4. **Semantic HTML** — Verify theme uses proper semantic elements (`<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`)
5. **Theme Accessibility** — Ensure theme templates support keyboard navigation, focus indicators, and screen reader compatibility

**In Scope:** Theme-controlled colors (body text, link colors, button colors, form control styling) since these are provided by the theme CSS, not by users
**Out of Scope:** User-authored content styling (custom text colors, inline styles set by content authors, user-defined color overrides) — these are the responsibility of content authors

### Implementation Approach

- Use pytest-a11y or axe-core-python libraries for automated checks
- Create test fixtures that render example sites and validate output HTML
- Integrate with existing test infrastructure (`conftest.py`, test utilities)
- Run as part of standard CI/CD pipeline

### Files to Create/Modify

**Create:**
- `tests/accessibility/__init__.py`
- `tests/accessibility/test_html_validation.py`
- `tests/accessibility/test_aria_attributes.py`
- `tests/accessibility/test_color_contrast.py`
- `tests/accessibility/utils.py`

**Modify:**
- `tests/conftest.py` — Add accessibility test fixtures/utilities (all shared fixtures now live here instead of a `tests/accessibility/fixtures.py` module)
- `pyproject.toml` — Add accessibility testing dependencies
- `requirements.test.txt` — Document test dependencies

## Acceptance Criteria

- [ ] All accessibility tests pass for at least one example configuration
- [ ] Tests detect common accessibility violations (missing alt text, poor contrast, etc.)
- [ ] Documentation is provided for extending/maintaining accessibility tests
- [ ] New dependencies are documented and added to `pyproject.toml`
- [ ] CI runs accessibility tests automatically on all PRs
- [ ] Test coverage is 80%+ for accessibility test code

## Dependencies

### New Dependencies

- `html5lib` or `beautifulsoup4` (for HTML parsing)
- `axe-core-python` or `pytest-a11y` (for accessibility checks)
- `wcag-contrast-ratio` (for color contrast validation)

### Compatibility

- All dependencies must support Python 3.8+
- No breaking changes to existing test infrastructure
- All existing tests must continue to pass

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| New dependencies add maintenance burden | Medium | Choose stable, widely-used libraries with active maintenance |
| False positives in automated checks | Medium | Manual review of check results, document known limitations |
| Performance impact on CI | Low | Run accessibility tests in parallel with other tests |
| Complexity of setting up HTML rendering for tests | Medium | Reuse existing integration test infrastructure |

## Timeline

- **Phase 1:** Scaffold test structure, add HTML/semantic validation
- **Phase 2:** Add ARIA and color contrast checks
- **Phase 3:** Add link/image/heading validation
- **Phase 4:** Documentation and CI integration

## Open Questions

1. Which accessibility testing library is preferred? (axe-core-python vs pytest-a11y vs custom checks)
2. Should accessibility tests be required to pass in CI, or initially warnings only?
3. What baseline accessibility level should we target? (WCAG 2.1 AA or higher)

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [pytest-a11y](https://github.com/abrinley/pytest-a11y)
