# Phase 4: Color Contrast & Visual Accessibility — Implementation Plan

**Change ID:** `add-accessibility-tests`  
**Phase:** 4  
**Status:** Ready to Start  
**Date:** 2026-01-21

---

## Overview

Phase 4 implements WCAG 2.1 AA color contrast validation for the Terminal for MkDocs theme. This validates that text and interactive elements meet minimum contrast ratios (4.5:1 for normal text, 3:1 for large text).

---

## Requirements

From spec (`specs/testing/spec.md`):

### Requirement: Color Contrast Validation

MUST validate that text and interactive elements meet WCAG 2.1 AA color contrast standards (4.5:1 minimum for normal text, 3:1 for large text or UI components).

**Scenarios:**
- Detect low contrast text in theme (text color vs background color)
- Verify focus indicator contrast
- Validate that focus states have sufficient contrast

---

## Design Approach

Based on `design.md` specifications:

### Library Choice
- **BeautifulSoup4:** Parse HTML and extract color values from inline styles and CSS
- **Python's `colorsys`:** Standard library for color space conversions (hex/rgb/hsl normalization)
- **Custom contrast calculation:** Implement relative luminance formula per WCAG 2.1 specification
- **CSS parsing:** Extract computed colors from theme CSS files

**Note on PyPI alternatives:** We're not using external libraries like `wcag-contrast-ratio` (last updated 2015) or `colour` (last updated 2017) because they are no longer actively maintained. Using Python's standard library `colorsys` avoids adding unmaintained dependencies while remaining lightweight and maintainable.

### Implementation Strategy

1. **Color Extraction**
   - Parse inline styles: `style="color: #333; background: white"`
   - Parse CSS classes: map classes to computed colors
   - Handle color formats: hex (#fff, #ffffff), rgb(255,255,255), hsl(0,0%,100%), named colors

2. **Contrast Ratio Calculation**
   - Implement relative luminance formula: (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
   - Calculate contrast ratio: (L1 + 0.05) / (L2 + 0.05) where L1 > L2
   - Normalize L values to 0-1 range with gamma correction

3. **Validation**
   - 4.5:1 minimum for normal text (< 18pt or < 14pt bold)
   - 3:1 minimum for large text (≥ 18pt or ≥ 14pt bold)
   - 3:1 minimum for UI components (buttons, form fields, links)

4. **Scope**
   - **Theme-controlled colors:** Body text, links, buttons, form controls, headings—these are defined by theme CSS
   - **Out of scope:** User-authored custom styles (inline styles, custom CSS classes added by content authors)

### Limitations (Document these)

- **Static analysis only:** Cannot validate JavaScript-computed styles
- **No hover/focus states:** Cannot test dynamic style changes requiring user interaction
- **No actual rendering:** Cannot measure perceived contrast with actual fonts/anti-aliasing
- **Background images:** Cannot extract colors from images

---

## Implementation Tasks

### Task 1: Create Color Utility Functions

Create `tests/accessibility/color_utils.py`:

```python
def normalize_color(color_str: str) -> tuple[float, float, float]:
    """Convert color string to RGB tuple (0.0-1.0 scale)"""
    # Handle: #fff, #ffffff, rgb(255,0,0), hsl(0,0%,100%), named colors
    
def get_relative_luminance(rgb: tuple) -> float:
    """Calculate relative luminance per WCAG 2.1"""
    # Apply gamma correction and luminance formula
    
def get_contrast_ratio(color1: str, color2: str) -> float:
    """Calculate contrast ratio between two colors"""
    # Returns ratio like 4.5:1
    
def meets_wcag_aa(ratio: float, text_size: int = 14, is_bold: bool = False) -> bool:
    """Check if contrast ratio meets WCAG AA standard"""
    # 4.5:1 for normal text, 3:1 for large text
    
def parse_css_file(filepath: str) -> dict:
    """Parse theme CSS and extract color declarations"""
    # Returns mapping of selectors to color values
```

**Reference:** https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum

### Task 2: Create Color Contrast Validation Function

Add to `tests/accessibility/utils.py`:

```python
def validate_color_contrast(html: str, css_content: str = "", filename: str = "index.html") -> List[str]:
    """Validate text/element colors meet WCAG AA contrast standards"""
    violations: List[str] = []
    soup = BeautifulSoup(html, "html.parser")
    
    # Parse CSS to build color map
    color_map = parse_css_file_content(css_content)
    
    # Check theme region elements
    for element in soup.find_all(['a', 'button', 'input', 'label', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        # Get foreground and background colors
        fg_color = element.style.get('color') or get_color_from_class(element, color_map)
        bg_color = element.style.get('background-color') or get_inherited_bg_color(element)
        
        if fg_color and bg_color:
            ratio = get_contrast_ratio(fg_color, bg_color)
            if not meets_wcag_aa(ratio, get_font_size(element)):
                violations.append(...)
    
    return violations
```

### Task 3: Create Test File

Create `tests/accessibility/test_color_contrast.py`:

```python
class TestColorContrast:
    """Tests for WCAG 2.1 AA color contrast compliance"""
    
    @pytest.mark.parametrize("built_example_site", ["simple"], indirect=True)
    def test_theme_element_colors_meet_wcag_aa(self, built_example_site):
        """Verify theme elements (buttons, links, text) meet WCAG AA contrast standards"""
        # Build site, extract CSS, validate all elements
        
    def test_focus_states_have_visible_contrast(self, built_example_site):
        """Verify focus indicators have sufficient contrast (future: dynamic testing)"""
        # Document limitation: focus states require browser testing
        skip("Focus state testing requires browser automation - future phase")
```

### Task 4: Test Configuration & Integration

- Add `css_content` fixture to `conftest.py` that reads built CSS files
- Update `built_example_site` fixture to also copy CSS files to temp directory
- Add color contrast tests to test suite
- Verify tests pass on "simple" example site

### Task 5: Documentation

- Document color format support (hex, rgb, hsl, named colors)
- Document WCAG AA standards (4.5:1, 3:1)
- Document test limitations (static only, no hover/focus, etc.)
- Add examples of compliant vs non-compliant color pairs

---

## Implementation Sequence

1. **Day 1:** Implement color utility functions + unit tests for color parsing/contrast math
2. **Day 2:** Implement contrast validation function, create test file
3. **Day 3:** Integration testing, verify on example site, document findings
4. **Day 4:** Handle edge cases, documentation, update tasks.md

---

## Testing Strategy

### Unit Tests (for color utils)
```python
def test_normalize_color_hex():
    assert normalize_color("#ffffff") == (1.0, 1.0, 1.0)
    assert normalize_color("#000000") == (0.0, 0.0, 0.0)

def test_contrast_ratio_black_white():
    assert get_contrast_ratio("#000000", "#ffffff") == 21.0

def test_meets_wcag_aa():
    assert meets_wcag_aa(4.5, text_size=14)  # Normal text
    assert meets_wcag_aa(3.0, text_size=18)  # Large text
```

### Integration Tests (for theme)
- Run on "simple" example site
- Validate all theme element colors
- Document any violations found

---

## Expected Challenges

1. **CSS Parsing Complexity**
   - Theme may use CSS variables, media queries, nested selectors
   - May need to simplify or skip complex CSS
   - Consider: parse only inline styles first, expand to CSS later

2. **Background Color Inheritance**
   - May need to walk DOM tree to find actual background color
   - Images as backgrounds are unsupported (by design)

3. **Dynamic Styles**
   - Hover, focus, active states not testable without browser
   - Document as limitation, recommend browser-based testing for dynamic validation

4. **Font Size Detection**
   - Need to detect font size for 4.5:1 vs 3:1 standard
   - May rely on CSS defaults if not explicitly set

---

## Success Criteria

✅ **Phase 4 Complete When:**
- [ ] Color utility functions implemented and unit tested
- [ ] Contrast validation function created
- [ ] Test file with 2-3 test methods created
- [ ] Tests pass on "simple" example site (or violations documented)
- [ ] CSS parsing handles at least hex, rgb, hsl, named colors
- [ ] WCAG AA standards correctly implemented (4.5:1, 3:1)
- [ ] Limitations clearly documented
- [ ] All tests have robust configuration validation
- [ ] tasks.md updated with completion details

---

## References

- [WCAG 2.1 Contrast Minimum (1.4.3)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum)
- [Relative Luminance Formula](https://www.w3.org/TR/WCAG20-TECHS/G17.html)
- [Color Specification (hex, rgb, hsl, named)](https://www.w3.org/TR/css-color-3/)
- [Python Color Libraries](https://pypi.org/search/?q=color) (consider: colorspacious, webcolors)

---

## Next Phases

After Phase 4 completes:
- **Phase 5:** Keyboard navigation & theme accessibility
- **Phase 6:** Test coverage & documentation
- **Phase 7:** CI/CD verification
- **Phase 8:** Final validation & cleanup
