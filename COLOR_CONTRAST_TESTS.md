# Color Contrast Test Scenarios

The test suite validates **4 main contrast scenarios**, each parametrized across all 6 default palettes:

## Body Text (`test_theme_body_text_contrast_meets_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **4.5:1 minimum** for normal text
- **Elements tested**: `<body>`, `<p>`, `<h4>`, `<h5>`, `<h6>` and other text elements
- **Current palette colors**:
  - Default: #151515 on #fff = **18.3:1** ✅
  - Dark: #3f3f44 on #222225 = **1.5:1** ❌
  - Gruvbox Dark: #32302f on #282828 = **1.1:1** ❌
  - Pink: #f90d7a on #ffffff = **3.9:1** ❌
  - Sans: #151515 on #fff = **18.3:1** ✅
  - Sans Dark: #62c4ff on #222225 = **8.2:1** ✅

**Example FAILING values**:
```python
    # Font color: #999999, Background: #ffffff
    # Contrast ratio: 4.48:1 (just below 4.5:1 threshold) ❌ FAILS
```

---

## Links (`test_theme_link_colors_meet_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **4.5:1 minimum** for link text
- **Elements tested**: `<a>` (anchor/link elements with text)
- **Current palette colors**:
  - Default: #151515 on #fff = **18.3:1** ✅
  - Dark: #3f3f44 on #222225 = **1.5:1** ❌
  - Gruvbox Dark: #32302f on #282828 = **1.1:1** ❌
  - Pink: #f90d7a on #ffffff = **3.9:1** ❌
  - Sans: #151515 on #fff = **18.3:1** ✅
  - Sans Dark: #62c4ff on #222225 = **8.2:1** ✅

**Example FAILING values**:
```python
    # Link color: #6666ff (Medium blue), Background: #ffffff
    # Contrast ratio: 3.2:1 (below 4.5:1 threshold) ❌ FAILS
```

---

## Buttons (`test_theme_button_and_form_contrast_meets_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **3.0:1 minimum** for UI components (more lenient than text)
- **Elements tested**: `<button>`, `<input>`
- **Current palette colors**:
  - Default: #151515 on #fff = **18.3:1** ✅
  - Dark: #3f3f44 on #222225 = **1.5:1** ❌
  - Gruvbox Dark: #32302f on #282828 = **1.1:1** ❌
  - Pink: #f90d7a on #ffffff = **3.9:1** ✅
  - Sans: #151515 on #fff = **18.3:1** ✅
  - Sans Dark: #62c4ff on #222225 = **8.2:1** ✅

**Example FAILING values**:
```python
    # Button text color: #999999, Background: #cccccc
    # Contrast ratio: 2.9:1 (just below 3:1 threshold) ❌ FAILS
```

---

