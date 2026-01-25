# Refactoring Proposal: Accessibility Test Utilities and Test Cases

**Status:** Proposal (Not Yet Implemented)  
**Date:** January 24, 2026  
**Scope:** Improving readability and maintainability of accessibility tests and utilities

---

## Overview

The accessibility testing module (`tests/accessibility/`) currently contains ~2,700 lines of code across 8 files. While functional and comprehensive, the code has opportunities for refactoring to improve:

- **Readability**: Large classes and functions with multiple responsibilities
- **Maintainability**: Utility functions scattered across multiple files; inconsistent patterns
- **Testability**: Helper functions that are difficult to unit test in isolation
- **Documentation**: Complex logic needs better inline documentation
- **Reusability**: Some validation logic duplicated across test files

---

## Proposed Refactoring Changes

### Category 1: Utility Organization and Consolidation

#### 1.1 Split `utils.py` into focused modules
**Problem:** `utils.py` is 800 lines with mixed concerns (HTML validation, ARIA validation, color validation, CSS parsing)

**Proposed Solution:**
- Create `tests/accessibility/validators/html_validator.py` — HTML structure/semantic validation
  - `validate_duplicate_ids()`
  - `validate_semantic_html()`
  - `validate_html_structure()`
  
- Create `tests/accessibility/validators/aria_validator.py` — ARIA attribute validation
  - `validate_aria_buttons()`
  - `validate_aria_hidden()`
  - `validate_modal_accessibility()`
  - `validate_form_labels()`
  - `validate_link_text()`
  
- Create `tests/accessibility/utilities/css_parser.py` — CSS parsing and variable extraction
  - `_extract_css_variables()`
  - `_parse_css_variables()`
  - `_get_element_computed_styles()`
  - `_resolve_css_variable()`
  - `extract_css_attributes()`
  
- Keep `tests/accessibility/utils.py` as a thin convenience layer that re-exports from above, plus general helpers

**Benefits:**
- Each module has a single, clear responsibility
- Easier to locate specific validation logic
- Can test CSS parsing independently of ARIA validation
- Reduces cognitive load when reading/modifying code

**Files Affected:**
- `tests/accessibility/utils.py` (refactored to thin layer + general helpers)
- New: `tests/accessibility/validators/__init__.py`
- New: `tests/accessibility/validators/html_validator.py`
- New: `tests/accessibility/validators/aria_validator.py`
- New: `tests/accessibility/utilities/__init__.py`
- New: `tests/accessibility/utilities/css_parser.py`
- Update imports in `test_html_validation.py`, `test_aria.py`, `test_color_contrast.py`

---

#### 1.2 Extract CSS-related utilities into dedicated utilities module
**Problem:** Color contrast tests contain extensive CSS handling logic mixed with test logic (lines 44-200 in `test_color_contrast.py`)

**Proposed Solution:**
- Move `load_css_from_site()`, `SiteContext`, `iter_site_html_files()` to `tests/accessibility/utilities/site_context.py`
- Create `SiteContextBuilder` class to handle building and managing site context
- Promote `SiteContextBuilder` from a loose collection of helpers into a full class with caching, lazy iteration, and reusable parsing hooks that the forthcoming test helpers can depend on
- Keep `SiteContext` itself as a simple dataclass (plain data carrier) while the builder encapsulates all logic
- Relocate `color_utils.py` into the same utilities package so all color/CSS helpers live together

**Benefits:**
- CSS handling logic isolated from test logic
- Reusable by other test files that need CSS context
- Can test CSS loading independently
- Provides a single entry point (`SiteContextBuilder`) for the shared test helpers (see Section 4.1), so tests iterate over parsed contexts without duplicating parsing logic

**Files Affected:**
- New: `tests/accessibility/utilities/site_context.py`
- `tests/accessibility/test_color_contrast.py` (remove CSS utility functions, import from `site_context.py`)

---

### Category 2: Test File Organization and Clarity

#### 2.1 Consolidate color contrast helper classes in `test_color_contrast.py`
**Problem:** Multiple helper classes/functions defined in test file (lines 186-400):
- `resolve_background_color()` — standalone function
- `PaletteColors` — dataclass
- `get_palette_colors()` — standalone function
- `assert_contrast_meets_wcag_aa()` — helper assertion
- `ColorCombination` — dataclass
- `ColorCombinationTracker` — utility class

**Proposed Solution:**
- Extract these into `tests/accessibility/validators/contrast_validator.py`:
  - `BackgroundColorResolver` class (encapsulates `resolve_background_color()` logic)
  - `PaletteColors` dataclass
  - `PaletteColorExtractor` class (encapsulates palette extraction)
  - `ColorCombinationTracker` class
  - `ContrastAssertion` class with `assert_contrast_meets_wcag_aa()` method
  
- Keep in test file: Test classes and test methods only

**Benefits:**
- Test file focuses on test logic, not helper implementation
- Easier to unit test contrast validation in isolation
- Reusable components if other tests need similar checks

**Files Affected:**
- New: `tests/accessibility/validators/contrast_validator.py`
- Update: `tests/accessibility/validators/__init__.py`
- `tests/accessibility/test_color_contrast.py` (remove helper implementations, import from contrast_validator.py)

**Current Status:** The palette helpers (`PaletteColors`, `get_palette_colors()`, `assert_contrast_meets_wcag_aa()`) remain in `contrast_validator.py`, while the DOM-oriented `BackgroundColorResolver`/`ColorCombinationTracker` classes were removed once we eliminated the site-scanning tests due to false positives.

---

#### 2.2 Keep palette-related fixtures in the root `tests/conftest.py`
**Problem:** Palette testing logic and fixtures were previously scattered between dedicated modules and ad-hoc helpers.

**Current Solution:**
- Consolidate everything in the existing root-level `tests/conftest.py`, which now exposes `all_palette_css_attributes`, `built_example_site_with_palette`, and related helpers.
- Document fixture scope and usage directly in that file to keep a single source of truth.

**Benefits:**
- Centralizes palette test infrastructure without fragmenting pytest discovery.
- Easier to understand fixture relationships (all consumers import from the same module).
- Avoids maintaining multiple `conftest.py` files, which previously caused fixture duplication and circular import headaches.

**Files Affected:**
- `tests/conftest.py`
- Tests importing fixtures (e.g., `tests/accessibility/test_color_contrast.py`, `tests/accessibility/test_css_loading.py`)

---

### Category 3: Code Quality and Consistency

#### 3.1 Replace multiple similar validation patterns with consistent interface
**Problem:** Validation functions have inconsistent signatures:
- Some: `validate_x(html, filename)`
- Some: `validate_x(element, css_variables)`
- Return types: sometimes `List[str]`, sometimes `Dict`, sometimes tuples

**Proposed Solution:**
- Define abstract base class `AccessibilityValidator`:
  ```python
  class AccessibilityValidator(ABC):
      """Base class for accessibility validators."""
      @abstractmethod
      def validate(self) -> List[str]:
          """Validate and return list of violation messages."""
          pass
      
      @property
      @abstractmethod
      def name(self) -> str:
          """Human-readable name of this validator."""
          pass
  ```
- Implement concrete validators inheriting from base:
  - `HTMLStructureValidator`
  - `ARIAValidator`
  - `ContrastValidator`
  - etc.

**Benefits:**
- Consistent interface across all validators
- Easier to add new validators following established pattern
- Can build generic validation runner that works with any validator

**Files Affected:**
- New: `tests/accessibility/validators/base.py`
- Update: `tests/accessibility/validators/html_validator.py`
- Update: `tests/accessibility/validators/aria_validator.py`
- Update: `tests/accessibility/color/contrast_validator.py`

---

#### 3.2 Improve docstrings and type hints
**Problem:**
- Complex functions lack detailed docstring explanations
- Some type hints are incomplete or missing
- Design decisions not documented in code (e.g., why BeautifulSoup vs. tidylib)

**Proposed Solution:**
- Add/improve docstrings following Google style:
  - Clear description of what validator checks
  - Args and Returns sections
  - Limitations (e.g., "static analysis only")
  - Reference to WCAG standards when applicable
  
- Complete type hints for all parameters and returns
- Add inline comments explaining non-obvious logic (e.g., color parsing edge cases)
- Add module-level docstrings explaining design decisions

**Example:**
```python
def resolve_background_color(
    element: Tag,
    css_variables: Dict[str, str],
    soup: BeautifulSoup,
    default: str = "#ffffff",
) -> Optional[str]:
    """Resolve the effective background color for an element.
    
    Walks up the DOM tree to find the first non-transparent background color,
    falling back to body background or the provided default. This accounts for
    CSS cascading where an element may inherit its background from a parent.
    
    Args:
        element: The BeautifulSoup Tag element to resolve background for
        css_variables: Extracted CSS variable definitions from stylesheets
        soup: Root BeautifulSoup document (used to find <body>)
        default: Default color if none found (default: white)
    
    Returns:
        Color string in format matching input (hex, rgb, etc.), or None if transparent.
        
    Note:
        This is static analysis and cannot detect:
        - Dynamically applied styles (JavaScript)
        - Background images
        - CSS animations/transitions
    """
```

**Files Affected:**
- All utility files in `tests/accessibility/`

---

#### 3.3 Consolidate CSS variable extraction with better error handling
**Problem:** `_extract_css_variables()` and `_parse_css_variables()` are complex (lines 514-578 in utils.py) with limited error handling

**Proposed Solution:**
- Create `CSSVariableExtractor` class encapsulating extraction logic
- Add detailed error messages and warnings when:
  - Variable references are circular
  - Variable is referenced but not defined
  - Color format is unparseable
  
- Support fallback strategies (e.g., if main palette CSS missing, use default)
- Add logging for debugging CSS parsing issues

**Benefits:**
- Easier to debug CSS parsing failures
- Reusable in other contexts
- Better error messages for developers

**Files Affected:**
- `tests/accessibility/utilities/css_parser.py` (if created per 1.2)

---

#### 3.4 Reduce test_color_contrast.py from 785 to ~300 lines
**Problem:** Large test file mixes many concerns and complexity

**Result of Prior Changes:**
After implementing Categories 1-2, `test_color_contrast.py` should:
- Remove helper class definitions (moved to `color/contrast_validator.py`)
- Remove CSS utilities (moved to `css/site_context.py`)
- Keep only test classes and test methods
- Focus on what needs testing, not how to test it

**Outcome:**
- Current: 785 lines
- Target: ~250-300 lines
- Benefits: Much easier to scan and understand test intent

---

### Category 4: Test Pattern Improvements

#### 4.1 Extract common test patterns into test utilities
**Problem:** Similar test patterns repeated:
```python
# In test_color_contrast.py
site_path = get_site_path(built_example_site_with_palette)
for ctx in iter_site_html_files(site_path):
    # validate...

# In test_aria.py
html_files = list(built_example_site.glob("**/*.html"))
for html_file in html_files:
    html = html_file.read_text(encoding="utf-8")
    # validate...
```

- Create `tests/accessibility/test_utils.py` with helper functions that build on the new `SiteContextBuilder` class (Section 1.2):
  - `iter_html_files(site_path)` — yields `SiteContext` objects from a shared builder (optionally accepts an existing builder instance for reuse)
  - `run_validator_on_site(site_path, validator)` — instantiates a builder once, iterates contexts, and feeds them into a validator implementing the shared interface
  - `collect_all_violations(site_path, validator_list)` — reuses a single builder to drive multiple validators so HTML/CSS parsing work happens only once
  
- Provides consistent pattern across test files

**Benefits:**
- Less code duplication
- Tests are shorter and more focused
- Easier to add new validators that follow same pattern
- Site parsing/caching concerns live entirely inside `SiteContextBuilder`, so helpers just orchestrate validation

**Files Affected:**
- New: `tests/accessibility/test_utils.py`
- Update: `test_color_contrast.py`
- Update: `test_aria.py`
- Update: `test_html_validation.py`

---

#### 4.2 Improve test assertions with better error messages
**Problem:** When tests fail, error messages are sometimes hard to parse:
```python
assert not all_violations, f"Color contrast violations found:\n" + "\n".join(all_violations)
```

**Proposed Solution:**
- Create assertion helpers that format violations clearly:
```python
def assert_no_a11y_violations(violations: List[str], category: str = "Accessibility"):
    """Assert no accessibility violations found.
    
    Args:
        violations: List of violation messages
        category: Category name for error message (e.g., "Color Contrast")
    """
    if violations:
        formatted = "\n".join(f"  • {v}" for v in violations)
        pytest.fail(f"{category} violations found:\n{formatted}")
```

**Benefits:**
- Consistent error message formatting
- Easier to parse test failures
- Better for CI/CD systems

**Files Affected:**
- Update: `test_utils.py` (or `utils.py`)
- Update: All test files using assertions

---

### Category 5: Type Safety and Validation

#### 5.1 Use TypedDict for CSS variable schema
**Problem:** `css_variables` is `Dict[str, str]` everywhere, making it unclear what keys are expected

**Proposed Solution:**
- Define TypedDict for known CSS variables:
```python
class PaletteVariables(TypedDict, total=False):
    """CSS variables defined in palette stylesheets."""
    font_color: str
    background_color: str
    primary_color: str
    error_color: str
    global_font_size: str
    # ... etc
```

- Use in function signatures for better IDE support and type checking
- Migrates to `TypedDict` from plain `Dict[str, str]`

**Benefits:**
- Better IDE autocomplete
- Catches typos at type-check time
- Self-documenting code
- Better mypy/pylance support

**Files Affected:**
- New: `tests/accessibility/types.py` (define TypedDicts)
- Update: CSS parsing functions
- Update: Type hints throughout

#### 5.2 Enforce mypy type checking for utility modules
**Problem:** Without static analysis, regressions in helper utilities (especially the refactored validators and shared utilities) can slip through linting and unit tests.

**Proposed Solution:**
- Add `mypy` configuration (either dedicated `mypy.ini` section or `pyproject.toml` update) to type-check `tests/accessibility/` and newly created `tests/accessibility/utilities/` modules.
- Ensure utility modules, validators, and fixtures pass `mypy` with `--strict` (or near-strict) settings; allow more permissive settings elsewhere if necessary.
- Integrate `mypy` run into CI so regressions are caught automatically.

**Benefits:**
- Guarantees that the refactored helpers remain type-safe over time.
- Provides faster feedback when adding new validators or utilities.
- Encourages contributors to keep type hints accurate and up to date.

**Files/Configs Affected:**
- `pyproject.toml` (add mypy config block if missing)
- `Makefile` / CI workflows (ensure `mypy tests/accessibility` runs)
- All newly refactored utility modules (updates may be required to satisfy mypy)

---

### Category 6: Documentation

#### 6.1 Create accessibility testing guide
**Problem:** Complex testing infrastructure not documented for new developers

**Proposed Solution:**
- Create `tests/accessibility/README.md` with:
  - Architecture overview with diagrams
  - How to write new accessibility validators
  - Common patterns and examples
  - Testing scope (what we validate, what we don't)
  - Known limitations of static analysis
  - Troubleshooting CSS parsing issues

**Files Affected:**
- New: `tests/accessibility/README.md`

---

#### 6.2 Add inline documentation for complex logic
**Problem:** CSS parsing, color contrast calculations, regex patterns lack explanation

**Proposed Solution:**
- Add detailed comments for:
  - CSS variable reference resolution (handles circular refs, recursion)
  - Color normalization (supports multiple color formats)
  - Contrast ratio calculation (WCAG formula)
  - Regular expressions (explain what each regex matches)

**Files Affected:**
- `tests/accessibility/utilities/css_parser.py`
- `tests/accessibility/utilities/color_utils.py`

---

## Implementation Strategy

### Phase 1: Foundation (Low Risk)
1. Create new module structure (validators/ plus consolidated utilities/ directory for CSS + color helpers)
2. Move code without changing logic (just reorganize imports)
3. Update tests to verify no behavior changes
4. Focus: Imports, project structure

### Phase 2: Abstraction Layer (Medium Risk)
1. Implement abstract base classes and new interfaces
2. Migrate existing validators to use new base class
3. Verify all tests still pass
4. Focus: Consistency, reusability

### Phase 3: Consolidation (Medium Risk)
1. Extract test helpers into test_utils.py
2. Reduce code duplication in test patterns
3. Improve error messages
4. Focus: Readability, maintainability

### Phase 4: Polish (Low Risk)
1. Improve docstrings and type hints
2. Add documentation and README
3. Add mypy configuration + CI hook for accessibility utilities
4. Code cleanup and final review
5. Focus: Documentation, knowledge transfer, static analysis

### Phase 5: Validation (Critical)
1. Run full test suite to ensure no regressions
2. Verify test coverage remains above 80%
3. Manual testing of key accessibility checks
4. Focus: Quality assurance

---

## Estimated Impact

### Lines of Code Changes
- **Total lines today:** ~2,700
- **After refactoring:** ~2,500-2,600
  - Organized into clearer modules
  - Some consolidation of utilities
  - Better docstrings add ~100-200 lines
  - Net reduction: code is more maintainable, not necessarily shorter

### File Structure
```
tests/accessibility/
├── __init__.py
├── README.md (new)
├── conftest.py (new)
├── types.py (new)
├── utils.py (refactored - thin layer)
├── test_utils.py (new)
├── test_aria.py (simplified imports)
├── test_color_contrast.py (reduced from 785 to ~300 lines)
├── test_color_utils.py (unchanged)
├── test_css_loading.py (unchanged)
├── test_html_validation.py (simplified imports)
├── validators/ (new)
│   ├── __init__.py
│   ├── base.py
│   ├── html_validator.py
│   ├── aria_validator.py
│   └── contrast_validator.py
└── utilities/ (new)
    ├── __init__.py
    ├── css_parser.py
    ├── color_utils.py (moved from top level)
    └── site_context.py
```

---

## Risk Assessment

### Low Risk Changes
- Module reorganization (moving code without logic changes)
- Adding documentation and docstrings
- Improving type hints
- Adding new helper functions

### Medium Risk Changes
- Introducing abstract base classes and new interfaces
- Consolidating duplicated code patterns
- Extracting helpers from test files

### Mitigations
- Run full test suite after each phase
- Keep test coverage above 80%
- Maintain backward compatibility of public APIs
- Review changes incrementally (phase by phase)

---

## Success Criteria

1. ✅ All accessibility tests pass (no behavior changes)
2. ✅ Test coverage remains ≥80%
3. ✅ Code is more organized (clearer module boundaries)
4. ✅ Easier for new developers to understand and extend
5. ✅ Reduced code duplication
6. ✅ Better documentation and inline comments
7. ✅ Type hints are more complete and accurate
8. ✅ No external dependency changes
9. ✅ `mypy` passes for accessibility utilities/validators in CI

---

## Next Steps

Once this proposal is reviewed and approved:

1. **Detailed Task Breakdown**: Create openspec tasks for each refactoring phase
2. **Implementation Planning**: Determine order of implementation within each phase
3. **Code Review Readiness**: Prepare for phase-by-phase code reviews
4. **Testing Strategy**: Ensure test coverage maintained throughout

---

## Questions for Review

1. Is the proposed module organization clear and logical?
2. Should we introduce abstract base classes (Category 3.1) or keep current pattern?
3. Does consolidating CSS + shared helpers under `utilities/` cover your expectations, or should any pieces stay top-level?
4. Are there other areas of code duplication we should address?
5. Beyond the utilities + validators, are there additional paths you want covered by the new mypy check?
