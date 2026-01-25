# Design Document: Accessibility Testing Infrastructure

Change ID: `add-accessibility-tests`

## Architecture Overview

```
tests/
├── accessibility/
│   ├── __init__.py
│   ├── test_html_validation.py        # HTML structure + semantic checks
│   ├── test_aria.py                   # Buttons, modal, aria-hidden, links
│   ├── test_color_contrast.py         # Palette-level WCAG validation
│   ├── test_color_utils.py            # Unit coverage for parsing + ratios
│   ├── test_css_loading.py            # Palette/site integration coverage
│   ├── utilities/
│   │   ├── color_utils.py             # Parsing + WCAG math
│   │   ├── css_parser.py              # CSS variable extraction helpers
│   │   ├── palette_loader.py          # Palette caching + fixtures
│   │   └── site_context.py            # Site builder helpers
│   └── validators/
│       ├── aria_validator.py          # ARIA/link/form checks
│       ├── contrast_validator.py      # Assertion helpers for WCAG AA
│       ├── helpers.py                 # Shared formatting utilities
│       └── html_validator.py          # Duplicate ID + tidy integration
├── conftest.py                        # Shared fixtures (site builds, palettes)
└── ...existing tests
```

## Key Design Decisions

### 1. Library Choice: BeautifulSoup4 + HTML Tidy via `tidylib`

**Decision:** Use BeautifulSoup4 for DOM traversal plus `tidylib` (HTML Tidy bindings) for structural validation instead of browser-driven libraries such as axe-core.

**Rationale:**
- Both libraries already exist in the dependency graph (BeautifulSoup4 via MkDocs, `tidylib` packaged through the existing tidy system dependency) and are lightweight.
- Custom validators (`tests/accessibility/validators/*.py`) give us precise, theme-specific rules without reverse-engineering axe output.
- Static analysis is deterministic in CI (no headless browser flake) and easy to reason about when tests fail.
- WCAG contrast math is simple enough to keep in-house (`utilities/color_utils.py`), avoiding dormant dependencies like `wcag-contrast-ratio`.

**Alternatives Considered:**
- axe-core-python: Requires Node/Chromium, introduces large dependency surface, and would slow CI significantly.
- pytest-a11y: Helpful starting point but difficult to customize for theme-specific semantics or CSS variable inspection.
- html5lib alone: Validates syntax but cannot express ARIA/link/modal rules; we still need BeautifulSoup and custom logic.

### 2. Test Organization

**Decision:** Keep pytest modules focused on distinct concern areas, with shared helpers under `utilities/` and `validators/`.

**Current Modules:**
- `test_html_validation.py` — Duplicate IDs, landmark semantics, and HTML Tidy validation.
- `test_aria.py` — Button names, aria-hidden usage, modal structure, link text, and form labels.
- `test_color_contrast.py` — Palette-level WCAG AA assertions for text, links, alerts, ghost/error buttons, nav links, etc.
- `test_color_utils.py` — Unit coverage for the color parser/contrast math plus ratio regression tests.
- `test_css_loading.py` — Ensures palette CSS can still be injected into built example sites.

**Shared Helpers:**
- `utilities/` holds CSS parsing (`css_parser.py`), palette caching (`palette_loader.py`), reusable site context builders, and WCAG math (`color_utils.py`).
- `validators/` captures HTML, ARIA, and contrast-specific rule logic so pytest modules remain thin wrappers.

**Rationale:**
- Developers can target a single module (e.g., `test_aria.py`) when iterating on a feature.
- Utilities/validators centralize parsing logic, minimizing subtle drift between tests.
- The folder layout mirrors how we discuss the work in the proposal/tasks, making onboarding easier.

### 3. Test Data Source: Build Real Sites Once Per Module

**Decision:** Reuse the existing MkDocs example configurations and build them via fixtures in `tests/conftest.py` / `utilities/site_context.py`, caching the resulting HTML so each module only pays the cost once.

**Rationale:**
- Validates the exact HTML/CSS the theme ships instead of mocks.
- Exercises the entire navigation/search stack, ensuring template regressions are caught.
- Aligns with other integration helpers (e.g., `SiteContextBuilder`) so new tests can piggyback on existing site skeletons.

**Implementation:**
```python
@pytest.fixture(scope="module")
def built_example_site(site_context_builder):
    """Build the search-enabled example site once per module."""
    return site_context_builder.build_site(example="search-enabled")

def test_semantic_element_structure(built_example_site):
    html = (built_example_site / "index.html").read_text(encoding="utf-8")
    violations = validate_semantic_html(html, "index.html")
    assert not violations
```

### 4. Contrast Ratio Validation

**Decision:** Implement WCAG 2.1 AA contrast ratio checks (4.5:1 normal text, 3:1 large text/UI) using our own parser so we can control CSS variable resolution.

**Implementation:**
- `utilities/palette_loader.py` loads every palette under `terminal/css/palettes/` plus the fallback theme CSS, caching resolved variables for reuse.
- `utilities/color_utils.py` performs normalization (hex/rgb/hsl/named), luminance math, and ratio calculations without external dependencies.
- `validators/contrast_validator.py` supplies assertion helpers used across tests, keeping failure messaging consistent.
- `tests/test_style.py::test_palette_css_files_registered_in_default_palettes` guards against palettes that are added without updating `DEFAULT_PALETTES`, so color tests always exercise the complete set.

**Limitations:**
- Static analysis only (no hover/focus or runtime theming states yet).
- Tests rely on CSS variable presence; missing tokens yield actionable assertion messages but still require manual palette fixes.
- Known failing palettes (default, sans, pink, gruvbox_dark) are tracked via `pytest.xfail` until design remediation lands.

### 5. Known Failure Tracking & Expectation Management

**Decision:** Track genuine accessibility gaps via `pytest.xfail` (with documentation references) instead of ad-hoc inline skip markers.

**Current Usage:**
- `test_html_validation.py::test_semantic_element_structure` is `xfail` because multiple `<nav>` regions still need `aria-label`s.
- `test_aria.py` marks modal + aria-hidden violations as expected failures while the search modal is being rebuilt.
- `test_color_contrast.py` calls `xfail_if_known()` for palettes/components documented in `documentation/docs/accessibility.md`.

**Rationale:**
- Keeps the pytest output honest—the failures are visible but do not block CI until remediation PRs land.
- Each `xfail` string links back to documentation/issues so contributors know where to focus.
- Avoids introducing bespoke HTML annotations (`data-a11y-skip`) that would have to ship in the theme output.

### 6. Dependency Management

**Dependencies Added:**
- `beautifulsoup4` — Shared HTML/CSS parsing layer for validators and utilities.
- `pytidylib` + system `tidy` — HTML5 validation in `validate_html_structure` (installed via the existing `tidy` apt dependency in the test container).

**Avoided:**
- No axe-core / Selenium / pytest-a11y dependencies were introduced; static analysis keeps the surface area small and portable.

**Existing Tooling Reused:**
- Pytest fixtures + factories in `tests/conftest.py` (site builders, palette loaders).
- The Docker/Make-based test runner already provisions `tidy`, so CI changes were minimal.

### 7. Configuration & Customization

**Decision:** Keep configuration inside the test suite (fixtures + helper functions) so developers do not need bespoke pytest ini flags.

**Examples:**
- `KNOWN_CONTRAST_FAILURES` + `xfail_if_known()` centralize palette/component exceptions so contributors add/remove data in one place.
- Fixtures such as `built_example_site`, `palette_css_attributes`, and `all_palette_css_attributes` live in `tests/conftest.py`, giving every module uniform access to site output and CSS tokens.
- Validators accept optional parameters for filenames/context, enabling reuse without extra pytest markers.

Future enhancements (e.g., CLI flags to toggle strictness) can still be layered on later, but today the defaults keep onboarding simple.

## Testing Philosophy

### What We Test

1. **Structural** — Valid HTML5 (via tidy), semantic landmarks, duplicate ID detection.
2. **Interactive** — Button names, aria-hidden usage, modal role/aria-modal, form labels, nav/header/footer links.
3. **Visual** — Palette-driven WCAG contrast checks plus regression math for common palettes.
4. **CSS Integration** — Palette loading into rendered sites, ensuring CSS variables remain in sync with `DEFAULT_PALETTES`.

### What We Don't Test

1. **Runtime behavior** — Hover/focus states, JavaScript focus trapping, and keyboard navigation (future work).
2. **Browser rendering** — Layout/typography fidelity (requires browser automation).
3. **Content authoring** — Image alt text, heading hierarchy, and custom Markdown; authors control that output.
4. **Assistive tech output** — Actual screen reader announcements still require manual QA.

### Scenarios

Each test should include at least one scenario demonstrating the check:

```python
def test_buttons_have_text_or_aria_label(built_example_site):
    """
    Scenario: Screen reader user encounters theme buttons
    - Buttons must expose text content or aria-label
    - We fail fast if the site build unexpectedly lacks buttons
    """
    html_files = list(built_example_site.glob("**/*.html"))
    assert html_files, "No HTML files found in built site"

    violations = []
    for html_file in html_files:
        html = html_file.read_text(encoding="utf-8")
        violations.extend(validate_aria_buttons(html, html_file.name))

    assert not violations, "Buttons missing text or aria-label:\n" + "\n".join(violations)
```

## Error Reporting

**Format:**
```
ACCESSIBILITY VIOLATION: [Rule Name]
Location: [file.html#line.column]
Element: [HTML snippet]
Issue: [Description]
Suggestion: [How to fix]
Reference: [WCAG guideline link]
```

**Example:**
```
ACCESSIBILITY VIOLATION: Missing Image Alt Text
Location: search/index.html:45
Element: <img src="icon.png">
Issue: Image missing descriptive alt attribute
Suggestion: Add alt="Search icon" attribute
Reference: WCAG 2.1 AA 1.1.1 Non-text Content
```

## Performance Considerations

- Run accessibility tests sequentially (fewer sites to build)
- Cache built sites across multiple tests where safe
- Consider splitting into fast/slow test suites
- Profile to identify slow checks

## Future Enhancements

1. **Continuous Improvement**
   - Add checks for keyboard navigation (Tab order, focus management)
   - Validate language attributes for multilingual sites
   - Check for proper use of skip links

2. **Integration**
   - Create GitHub Actions summary with violations
   - Add accessibility scoreboard to CI dashboards

3. **Automation**
   - Auto-fix common issues (add missing alt text placeholders)
   - Generate accessibility checklist for reviewers
   - Track a11y improvements over time

**Note:** CSS attribute extraction utilities for report generation are planned as a separate feature and will be addressed in a future specification.

## Testing the Tests

The accessibility test suite itself must be tested:

1. **Coverage:** 80%+ line coverage of test code
2. **False Positives:** Manual review of check results against WCAG guidelines
3. **Regressions:** Ensure existing accessible sites continue to pass
4. **Edge Cases:** Test with various HTML structures, CSS patterns, color schemes

## Maintenance

**Regular Tasks:**
- Review WCAG guideline updates annually
- Update contrast ratio validation if standards change
- Monitor for new accessibility issues in popular frameworks
- Gather feedback from developers on false positives

**Deprecation:**
- If external a11y library becomes necessary, plan migration path
- Document why built-in checks are insufficient
