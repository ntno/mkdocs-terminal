# Proposal: Add Accessibility Tests

**Change ID:** `add-accessibility-tests`

**Status:** In Progress — core HTML/ARIA/contrast suites landed; Windows CI + remaining ARIA/focus coverage still outstanding.

**Created:** 2026-01-19

## Summary

Add automated accessibility testing to ensure the Terminal for MkDocs theme maintains WCAG 2.1 AA compliance and follows web accessibility best practices. This includes HTML validation, semantic structure verification, ARIA attribute checks, and color contrast validation of theme components only.

## Current State (2026-01-25)

- HTML structural and semantic checks live in `tests/accessibility/test_html_validation.py`, combining BeautifulSoup-based duplicate ID detection with HTML Tidy validation. Landmark coverage for multiple `<nav>` regions is implemented but currently marked `xfail` pending template fixes.
- ARIA coverage (buttons, aria-hidden, modal, forms, link text) ships via `tests/accessibility/test_aria.py` and shared helpers in `tests/accessibility/validators/aria_validator.py`. Search modal regressions are tracked through `pytest.xfail` with documentation references.
- Palette-focused WCAG 2.1 AA contrast tests run through `tests/accessibility/test_color_contrast.py`, `tests/accessibility/utilities/color_utils.py`, and `tests/accessibility/utilities/palette_loader.py`. Known palette failures (default, sans, pink, gruvbox_dark) are explicitly documented and expected-failed until new palette values are delivered.
- Supporting utilities (`css_parser.py`, `palette_loader.py`, `site_context.py`) and validators (`html_validator.py`, `contrast_validator.py`, `helpers.py`) centralize parsing logic, enabling reuse across tests.
- Accessibility tests run in CI for Python 3.8–3.12 on Ubuntu and macOS. Windows execution is blocked by dependency issue [#59](https://github.com/ntno/mkdocs-terminal/issues/59) and will be re-enabled once the upstream fix lands.
- Current coverage for the shared accessibility test utilities sits at 73%, measured via `pytest --cov=tests/accessibility --cov-branch --cov-report=html`.

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
4. **Documentation:** Developer guide for writing and maintaining accessibility tests, plus end-user guidance in `documentation/docs/accessibility.md` that enumerates current contrast failures detected by the automated suite.

### What's Out of Scope

- Fixing existing accessibility issues (separate work)
- Runtime accessibility enforcement (only testing)
- Browser-based GUI testing (only static analysis)
- Internationalization/localization accessibility (future phase)
- **Validation of user-provided content** — Site authors are responsible for accessible page structure, headings, forms, and content. Tests validate the theme structure only, not user content.

## Technical Design

### Testing Strategy

The implemented suite relies on static analysis of built example sites plus palette-level CSS inspection:

1. **HTML validity + semantics** — `tests/accessibility/test_html_validation.py` calls helpers in `validators/html_validator.py` to run duplicate-ID checks with BeautifulSoup and structural validation via `tidylib`. The semantic landmark test is currently marked `xfail` until `<nav>` elements receive unique labels.
2. **ARIA + interactive patterns** — `tests/accessibility/test_aria.py` feeds all built HTML through validators in `validators/aria_validator.py`, covering buttons, aria-hidden usage, search modal attributes, form labeling, and navigation links. Search modal regressions are tracked with explicit `pytest.xfail` markers referencing the accessibility documentation.
3. **Palette-level WCAG contrast** — `tests/accessibility/test_color_contrast.py`, `utilities/color_utils.py`, `utilities/css_parser.py`, and `validators/contrast_validator.py` compute WCAG 2.1 AA ratios directly from the palette CSS files. CSS variables are resolved via `palette_loader.py`, ensuring every palette in `terminal/css/palettes/` is exercised.
4. **CSS + parser regression coverage** — `tests/accessibility/test_css_loading.py` ensures palettes can still be injected into built sites, while `tests/accessibility/test_color_utils.py` unit-tests color parsing, luminance math, and regression ratios.

**In Scope:** Theme-controlled HTML templates and CSS variables (body text, primary/secondary colors, buttons, form controls). The suite purposely stops at static analysis; hover/focus states and runtime keyboard interactions remain future work.
**Out of Scope:** User-authored Markdown/HTML, inline colors, or JavaScript extensions supplied by documentation authors. Those remain the responsibility of site maintainers.

### Implementation Approach

- Shared fixtures in `tests/conftest.py` build the “search-enabled” example site once per test module and expose palette attribute dictionaries via `palette_loader` to keep runtime low.
- Accessibility validators live under `tests/accessibility/validators/` so pytest modules remain declarative and easy to extend.
- Known regressions (nav aria-labels, search modal aria-hidden usage, palette contrast gaps) are tracked with `pytest.xfail` to keep CI signal high while preventing accidental noise.
- CI executes the full `pytest tests/accessibility` matrix inside tox for Python 3.8–3.12 on Ubuntu and macOS; Windows runs are paused until dependency issue [#59](https://github.com/ntno/mkdocs-terminal/issues/59) is resolved.

### Files to Create/Modify

**Create:**
- `tests/accessibility/__init__.py`
- `tests/accessibility/test_html_validation.py`
- `tests/accessibility/test_aria.py`
- `tests/accessibility/test_color_contrast.py`
- `tests/accessibility/test_color_utils.py`
- `tests/accessibility/test_css_loading.py`
- `tests/accessibility/utilities/` (`color_utils.py`, `css_parser.py`, `palette_loader.py`, `site_context.py`)
- `tests/accessibility/validators/` (`aria_validator.py`, `html_validator.py`, `contrast_validator.py`, `helpers.py`)

**Modify:**
- `tests/conftest.py` — Share site-building fixtures and palette loaders across modules
- `documentation/docs/accessibility.md` — Document known failures surfaced by the suite
- `pyproject.toml` / `requirements.test.txt` — Add `beautifulsoup4`, `tidylib`, and related testing dependencies
- GitHub Actions / tox configuration — Ensure accessibility tests are part of every Python-version matrix run

## Acceptance Criteria

- [ ] All accessibility tests pass for at least one example configuration (current suite relies on documented `xfail`s for nav landmarks, modal ARIA gaps, and palette contrast issues)
- [x] Tests detect common accessibility violations (buttons without labels, invalid modal structure, insufficient contrast, duplicate IDs)
- [x] Documentation is provided for extending/maintaining accessibility tests (`documentation/docs/accessibility.md` + inline test docstrings)
- [x] New dependencies are documented and added to `pyproject.toml`
- [x] CI runs accessibility tests automatically on all PRs across Python 3.8–3.12
- [ ] Test coverage is 80%+ for accessibility test code (currently ~73% for `tests/accessibility` measured via `pytest --cov=tests/accessibility --cov-branch --cov-report=html`)

## Dependencies

### New Dependencies

- `beautifulsoup4` — HTML traversal for validators, CSS parsing, and palette extraction (already shared by multiple tests)
- `tidylib` + system `tidy` binary — structural HTML validation used by `validate_html_structure`
- `pytest` plugins already in tree (no axe-core or pytest-a11y dependency was added; contrast math is handled in-house via `color_utils.py`)

### Compatibility

- All dependencies must support Python 3.8+
- `tidylib` requires the `tidy` binary; Windows CI remains blocked until dependency issue [#59](https://github.com/ntno/mkdocs-terminal/issues/59) is resolved
- No breaking changes to existing test infrastructure
- All existing tests must continue to pass

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| New dependencies add maintenance burden | Medium | Choose stable, widely-used libraries with active maintenance |
| False positives in automated checks | Medium | Manual review of check results, document known limitations |
| Performance impact on CI | Low | Run accessibility tests in parallel with other tests |
| Complexity of setting up HTML rendering for tests | Medium | Reuse existing integration test infrastructure |
| Windows CI blocked by tidy dependency | Medium | Track [issue #59](https://github.com/ntno/mkdocs-terminal/issues/59); rerun Windows matrix once the upstream dependency is fixed |

## Timeline

- **Phase 1:** Scaffold test structure, add HTML/semantic validation
- **Phase 2:** Add ARIA and color contrast checks
- **Phase 3:** Add link/image/heading validation
- **Phase 4:** Documentation and CI integration

## Open Questions

1. What is the timeline for fixing the remaining `xfail`s (nav aria-labels, search modal aria-hidden usage, out-of-compliance palettes) so the suite can run fully green?
2. How should we surface accessibility artifacts in CI (e.g., publish JSON summaries vs rely on pytest output)?
3. When the Windows tidy dependency is resolved, do we run the full accessibility matrix on Windows or keep it Linux/macOS-only?

## Future Enhancements

### Automated Contrast Reporting (Proposed)

Add a follow-on feature that automatically captures every measured contrast ratio from the pytest suite and publishes it for documentation and CI visibility:

1. Extend `tests/accessibility/test_color_contrast.py` (or a pytest plugin) to emit structured JSON for each evaluated palette/component pair, including palette name, component, foreground/background colors, and the measured ratio.
2. Persist the aggregated JSON to `artifacts/accessibility/contrast_failures.json` (one entry per measurement) so CI can upload it and downstream tooling can reuse it.
3. Create a CLI helper (for example `scripts/export_contrast_report.py`) that reads the JSON artifact and renders reusable outputs: Markdown fragments for docs, CSV for spreadsheets, or other formats.
4. Update the docs build to include the generated Markdown fragment (e.g., `documentation/docs/includes/contrast_failures.md`) so the Accessibility page always reflects the latest ratios without manual editing.
5. Optionally wire CI to comment on pull requests or fail builds when new failures appear by diffing the JSON artifact between branches.

This enhancement would keep user-facing documentation synchronized with test output and reduce manual effort when palette contrast issues change over time.

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [pytest-a11y](https://github.com/abrinley/pytest-a11y)
