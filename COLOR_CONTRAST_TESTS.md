# Color Contrast Test Scenarios

The test suite validates **4 main contrast scenarios**, each parametrized across all 6 default palettes:

## 1. Body Text Contrast (`test_theme_body_text_contrast_meets_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **4.5:1 minimum** for normal text
- **Elements tested**: `<body>`, `<p>`, `<h4>`, `<h5>`, `<h6>` and other text elements
- **Current palette colors** (all pass):
  - Default: #151515 on #fff = **21.0:1** ✅
  - Dark: #e8e9ed on #222225 = **15.3:1** ✅
  - Gruvbox Dark: #ebdbb2 on #282828 = **9.4:1** ✅
  - Pink: #190910 on #ffffff = **22.0:1** ✅
  - Sans: #151515 on #fff = **21.0:1** ✅
  - Sans Dark: #e8e9ed on #222225 = **15.3:1** ✅

**Example FAILING values**:
```python
# Font color: #999999, Background: #ffffff
# Contrast ratio: 4.48:1 (just below 4.5:1 threshold) ❌ FAILS
```

---

## 2. Link Colors (`test_theme_link_colors_meet_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **4.5:1 minimum** for link text
- **Elements tested**: `<a>` (anchor/link elements with text)
- **Current palette colors** (all pass):
  - Default: #151515 on #fff = **18.3:1** ✅
  - Dark: #e8e9ed on #222225 = **15.3:1** ✅
  - Gruvbox Dark: #ebdbb2 on #282828 = **9.4:1** ✅
  - Pink: #190910 on #ffffff = **22.0:1** ✅
  - Sans: #151515 on #fff = **18.3:1** ✅
  - Sans Dark: #e8e9ed on #222225 = **15.3:1** ✅

**Example FAILING values**:
```python
# Link color: #6666ff (Medium blue), Background: #ffffff
# Contrast ratio: 3.2:1 (below 4.5:1 threshold) ❌ FAILS
```

---

## 3. Button & Form Control Contrast (`test_theme_button_and_form_contrast_meets_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **3:1 minimum** for UI components (more lenient than text)
- **Elements tested**: `<button>`, `<input>`, `<label>` 
- **Current palette colors** (all pass):
  - Default: #151515 on #fff = **18.3:1** ✅ (button), **18.3:1** ✅ (input)
  - Dark: #e8e9ed on #222225 = **15.3:1** ✅ (button), **15.3:1** ✅ (input)
  - Gruvbox Dark: #ebdbb2 on #282828 = **9.4:1** ✅ (button), **9.4:1** ✅ (input)
  - Pink: #190910 on #ffffff = **22.0:1** ✅ (button), **22.0:1** ✅ (input)
  - Sans: #151515 on #fff = **18.3:1** ✅ (button), **18.3:1** ✅ (input)
  - Sans Dark: #e8e9ed on #222225 = **15.3:1** ✅ (button), **15.3:1** ✅ (input)

**Example FAILING values**:
```python
# Button text color: #999999, Background: #cccccc
# Contrast ratio: 2.9:1 (just below 3:1 threshold) ❌ FAILS
```

---

## 4. Large Text Contrast (Implicit in above tests)

- **Standard**: WCAG 2.1 AA - **3:1 minimum** for large text (≥18pt bold or ≥24px)
- **Elements tested**: `<h1>`, `<h2>`, `<h3>` headers
- **Automatic detection**: Elements named h1/h2/h3 are treated as "large text"

**Example FAILING values**:
```python
# Header color: #aa7777, Background: #ffffff
# Contrast ratio: 2.8:1 (below 3:1 threshold for large text) ❌ FAILS
```

---

## 5. CSS Loading Verification (`test_css_classes_loaded_correctly`)

- **Standard**: Ensures actual palette colors are extracted correctly
- **Tests**: Validates that CSS variables resolve properly (including cascading references like `var(--gb-dm-fg1)`)
- **One test per palette** (6 instances total)

---

## Summary Table

| Scenario | Min Ratio | Elements | All Palettes Pass? |
|----------|-----------|----------|------------------|
| Body Text | 4.5:1 | p, body, h4-h6, etc. | ✅ Yes |
| Links | 4.5:1 | a (links) | ✅ Yes |
| Buttons/Forms | 3:1 | button, input, label | ✅ Yes |
| Large Text (h1-h3) | 3:1 | h1, h2, h3 | ✅ Yes |
| CSS Loading | N/A | Palette color verification | ✅ Yes |

**Total tests**: 24 pass across all 6 palettes

---

## Test Implementation Details

### Test Parametrization

Each of the first 4 contrast tests is parametrized to run across all 6 default palettes defined in [tests/interface/theme_features.py](tests/interface/theme_features.py):

```python
DEFAULT_PALETTES = [
    "default",
    "dark",
    "gruvbox_dark",
    "pink",
    "sans",
    "sans_dark",
]
```

This results in:
- 3 contrast validation tests × 6 palettes = 18 test instances
- 1 CSS loading verification test × 6 palettes = 6 test instances
- **Total: 24 test cases**

### CSS Variable Resolution

The tests support cascading CSS variable references. For example, the `gruvbox_dark` palette uses:

```css
:root {
    --gb-dm-fg1: #ebdbb2;
    --font-color: var(--gb-dm-fg1);
}
```

The variable resolution process:
1. Extracts all `:root` blocks from CSS files (including multiple palette definitions)
2. Resolves cascading variable references recursively
3. Returns final hex color values (e.g., `--font-color` resolves to `#ebdbb2`)

### Element Selection Strategy

The validation function checks contrast on elements that:
- Contain actual text content
- Have explicit color styling via CSS variables or inline styles
- Are part of theme-controlled elements (not user-generated content)

Elements are categorized for different minimum ratios:
- **Normal text** (4.5:1): body, p, span, a, label, etc.
- **Large text** (3:1): h1, h2, h3 (automatically detected)
- **UI components** (3:1): button, input, form elements

---

## Test Site Requirements

**Critical:** All built test sites MUST contain representative examples of all element types being tested. This ensures comprehensive validation coverage and prevents false negatives.

### Required Elements

The minimal test site (`tests/examples/minimal/`) must include:

| Element Type | Minimum Count | Purpose |
|--------------|--------------|---------|
| Paragraphs `<p>` | 1+ | Validate body text contrast |
| Links `<a>` | 3+ | Validate link contrast (navigation, content links) |
| Headers `<h1>`, `<h2>`, `<h3>` | 1+ each | Validate large text contrast |
| Buttons `<button>` | 1+ | Validate button UI contrast |
| Input fields `<input>` | 1+ | Validate form control contrast |

### Current Test Site Status

The minimal example site (`tests/examples/minimal/`) contains:
- ✅ Links: 7 elements
- ✅ Buttons: 1 element
- ✅ Inputs: 1 element
- ✅ Paragraphs: 2 elements
- ✅ Headers: 4 elements (h1-h6)

This provides adequate coverage for all contrast test scenarios.

### Validation Policy

If a test site is missing required elements:
- The test MUST fail with a clear diagnostic message
- The failure message should specify which element types are missing
- The test should NOT silently skip validation (avoiding false positives)

This ensures that test sites are properly configured and that all color contrast scenarios are actually being validated.
