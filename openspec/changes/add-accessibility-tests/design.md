# Design Document: Accessibility Testing Infrastructure

Change ID: `add-accessibility-tests`

## Architecture Overview

```
tests/
├── accessibility/
│   ├── __init__.py
│   ├── conftest.py           # Accessibility test fixtures
│   ├── utils.py              # Common accessibility helpers
│   ├── test_html_validation.py
│   ├── test_aria_attributes.py
│   ├── test_color_contrast.py
│   ├── test_link_validation.py
│   └── test_image_validation.py
├── conftest.py               # Updated with a11y fixtures
└── ...existing tests
```

## Key Design Decisions

### 1. Library Choice: BeautifulSoup4 + Custom Validators

**Decision:** Use BeautifulSoup4 for HTML parsing with custom validation functions instead of external a11y libraries.

**Rationale:**
- BeautifulSoup4 is already a transitive dependency (via MkDocs/other packages)
- Provides fine-grained control over what we validate
- Avoids adding heavy dependencies like axe-core
- Allows us to define project-specific a11y standards
- Simpler to debug and maintain custom validators

**Alternatives Considered:**
- axe-core-python: Too heavy, browser-dependent
- pytest-a11y: Limited customization
- html5lib validator: Only validates HTML structure, not accessibility

### 2. Test Organization

**Decision:** Group accessibility tests by concern area (HTML, ARIA, contrast, etc.)

**Structure:**
- `test_html_validation.py` — Semantic structure and HTML validity
- `test_aria_attributes.py` — ARIA role and attribute usage
- `test_color_contrast.py` — WCAG contrast ratios
- `test_link_validation.py` — Link text and href attributes
- `test_image_validation.py` — Image alt text
- Shared utilities in `utils.py`

**Rationale:**
- Easier to maintain and extend
- Clear separation of concerns
- Faster to run specific checks during development
- Each test file can have focused fixtures

### 3. Test Data Source: Build Real Sites

**Decision:** Build actual MkDocs sites using `tests/examples/` configurations and validate generated HTML.

**Rationale:**
- Tests actual theme output, not mock HTML
- Catches real-world accessibility issues
- Validates all theme components (navigation, search, sidebars, etc.)
- Matches existing integration test patterns

**Implementation:**
```python
@pytest.fixture
def built_site(tmp_path):
    """Build a test site and return the output directory."""
    config_path = "tests/examples/minimal/mkdocs.yml"
    output_dir = tmp_path / "site"
    # Build site using MkDocs API or subprocess
    return output_dir

def test_semantic_headings(built_site):
    """Verify headings follow h1-h6 sequence."""
    html = (built_site / "index.html").read_text()
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    # Validate sequence...
```

### 4. Contrast Ratio Validation

**Decision:** Implement WCAG 2.1 AA contrast ratio checks (4.5:1 for normal text, 3:1 for large text).

**Implementation:**
- Parse CSS to extract computed colors
- Calculate contrast ratios using relative luminance formula
- Handle color formats: hex, rgb, hsl, named colors
- Flag violations with specific locations in templates

**Limitations:**
- Static analysis only (no JavaScript-computed styles)
- Cannot validate hover/focus states requiring user interaction
- May need manual review for edge cases

### 5. Exception Handling

**Decision:** Support marking elements as exempt from certain checks via HTML comments or data attributes.

**Example:**
```html
<!-- a11y-skip: decorative -->
<img src="spacer.gif" alt="">

<!-- a11y-skip: color-contrast -->
<span style="color: #999;">Less important text</span>
```

**Rationale:**
- Some elements are intentionally non-compliant (decorative, legacy content)
- Allows focusing on real issues vs. false positives
- Document why exceptions exist

### 6. Dependency Management

**Dependencies to Add:**
- `beautifulsoup4` — HTML parsing (likely already available)
- No new external a11y libraries

**Existing Dependencies Used:**
- `pytest` — Test runner
- `lxml` or `html.parser` — HTML parsing backends

### 7. Configuration & Customization

**Decision:** Use pytest configuration for customizing accessibility checks.

**Example in `pyproject.toml`:**
```toml
[tool.pytest.ini_options]
a11y_level = "wcag21aa"
a11y_skip_rules = []
a11y_check_js_computed_styles = false
```

## Testing Philosophy

### What We Test

1. **Structural** — Valid HTML5, semantic markup, heading hierarchy
2. **Interactive** — ARIA attributes, button types, form associations
3. **Visual** — Color contrast, focus indicators
4. **Content** — Alt text, link text, descriptive labels
5. **Navigation** — Navigation landmarks, skip links (if present)

### What We Don't Test

1. **Runtime behavior** — JavaScript interactivity (integration tests cover this)
2. **Browser rendering** — Font rendering, layout (browser testing frameworks cover this)
3. **Screen reader announcements** — Requires actual screen reader testing
4. **User testing feedback** — Real accessibility testing with disabled users

### Scenarios

Each test should include at least one scenario demonstrating the check:

```python
def test_images_have_alt_text():
    """
    Scenario: User with vision impairment uses screen reader
    - Alt text should describe image content
    - Decorative images can have empty alt text
    """
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')
    
    for img in images:
        if not img.has_attr('data-decorative'):
            assert img.get('alt') is not None, f"Image {img.get('src')} missing alt text"
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
