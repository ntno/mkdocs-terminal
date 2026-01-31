# Palette Validation Specification

## ADDED Requirements

### Requirement: Validate bundled palette names at build time

The system SHALL verify that bundled palette names reference CSS files that exist in the theme's palette directory.

#### Scenario: Valid bundled palette
- **WHEN** selector.options contains `{name: "dark"}`
- **THEN** build validates that `terminal/css/palettes/dark.css` exists

#### Scenario: Invalid bundled palette
- **WHEN** selector.options contains `{name: "nonexistent"}`
- **THEN** build emits warning "Palette 'nonexistent' not found in bundled palettes" and filters option from selector

#### Scenario: Multiple valid bundled palettes
- **WHEN** selector.options contains `[{name: "dark"}, {name: "light"}, {name: "blueberry"}]`
- **THEN** build validates all three exist in `terminal/css/palettes/` directory

---

### Requirement: Validate custom palette CSS paths at build time

The system SHALL verify that custom palette CSS files are listed in `extra_css` configuration.

#### Scenario: Valid custom palette in extra_css
- **WHEN** selector.options contains `{name: "ocean", css: "assets/ocean.css"}` and `extra_css` includes "assets/ocean.css"
- **THEN** build validates custom palette and includes it in selector

#### Scenario: Custom palette missing from extra_css
- **WHEN** selector.options contains `{name: "ocean", css: "assets/ocean.css"}` but `extra_css` does not include "assets/ocean.css"
- **THEN** build emits warning "Custom palette CSS 'assets/ocean.css' not found in extra_css" and filters option from selector

#### Scenario: Custom palette with relative path
- **WHEN** selector.options contains custom palette with relative path "css/custom.css"
- **THEN** build validates path is relative and exists in configured extra_css

---

### Requirement: Validate selector.ui configuration value

The system SHALL verify that `selector.ui` is one of the allowed values: "auto", "toggle", or "select".

#### Scenario: Valid ui value "auto"
- **WHEN** configuration contains `selector.ui: "auto"`
- **THEN** build accepts configuration without warnings

#### Scenario: Valid ui value "toggle"
- **WHEN** configuration contains `selector.ui: "toggle"`
- **THEN** build accepts configuration without warnings

#### Scenario: Valid ui value "select"
- **WHEN** configuration contains `selector.ui: "select"`
- **THEN** build accepts configuration without warnings

#### Scenario: Invalid ui value
- **WHEN** configuration contains `selector.ui: "dropdown"`
- **THEN** build emits error "Invalid selector.ui value 'dropdown', must be 'auto', 'toggle', or 'select'" and falls back to "auto"

---

### Requirement: Validate toggle UI requires exactly 2 options

The system SHALL verify that when `selector.ui` is explicitly set to "toggle", exactly 2 valid options are configured.

#### Scenario: Toggle with 2 valid options
- **WHEN** configuration has `selector.ui: "toggle"` and 2 valid palette options
- **THEN** build accepts configuration and renders toggle UI

#### Scenario: Toggle with 1 option
- **WHEN** configuration has `selector.ui: "toggle"` and 1 valid palette option
- **THEN** build emits warning "Toggle UI requires exactly 2 options, found 1" and disables selector

#### Scenario: Toggle with 3+ options
- **WHEN** configuration has `selector.ui: "toggle"` and 3 valid palette options
- **THEN** build emits warning "Toggle UI requires exactly 2 options, found 3" and falls back to select UI

---

### Requirement: Validate at least one option exists when selector enabled

The system SHALL verify that at least one valid palette option is configured when selector is enabled.

#### Scenario: Selector enabled with valid options
- **WHEN** configuration has `selector.enabled: true` and 2 valid options
- **THEN** build accepts configuration and renders selector

#### Scenario: Selector enabled with no valid options
- **WHEN** configuration has `selector.enabled: true` but all options are invalid
- **THEN** build emits error "Selector enabled but no valid palette options found" and disables selector

#### Scenario: Selector enabled with empty options list
- **WHEN** configuration has `selector.enabled: true` and `selector.options: []`
- **THEN** build emits error "Selector enabled but options list is empty" and disables selector

---

### Requirement: Validate default palette is valid

The system SHALL verify that the configured default palette is either a valid bundled palette or a configured custom palette.

#### Scenario: Valid bundled default palette
- **WHEN** configuration has `default: "dark"`
- **THEN** build validates "dark" exists in bundled palettes

#### Scenario: Valid custom default palette
- **WHEN** configuration has `default: "ocean"` and "ocean" is in selector.options as custom palette
- **THEN** build validates default palette is configured

#### Scenario: Invalid default palette
- **WHEN** configuration has `default: "nonexistent"`
- **THEN** build emits warning "Default palette 'nonexistent' is not valid" and falls back to first valid option

---

### Requirement: Filter invalid options from selector UI

The system SHALL exclude invalid palette options from the rendered selector UI after validation.

#### Scenario: Mixed valid and invalid options
- **WHEN** selector.options contains `[{name: "dark"}, {name: "invalid"}, {name: "light"}]` and "invalid" fails validation
- **THEN** selector UI renders with only "dark" and "light" options

#### Scenario: Invalid option emits warning
- **WHEN** palette option fails validation
- **THEN** build logs warning message identifying the invalid option and reason for failure

#### Scenario: All options filtered leaves selector disabled
- **WHEN** all configured options fail validation
- **THEN** selector is disabled and not rendered in UI

---

### Requirement: Emit build warnings via MkDocs logging

The system SHALL use MkDocs logging infrastructure to emit validation warnings during build.

#### Scenario: Warning logged to MkDocs output
- **WHEN** validation fails for any palette option
- **THEN** warning message appears in `mkdocs build` CLI output

#### Scenario: Warning includes context
- **WHEN** validation warning is emitted
- **THEN** message includes palette name, validation failure reason, and suggested fix

#### Scenario: Multiple warnings for multiple issues
- **WHEN** multiple palette options fail validation
- **THEN** separate warning is emitted for each failed option
