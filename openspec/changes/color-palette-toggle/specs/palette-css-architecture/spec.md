# Palette CSS Architecture Specification

## ADDED Requirements

### Requirement: Use CSS custom properties for palette variables

The system SHALL define all palette-specific styles using CSS custom properties (variables).

#### Scenario: Define palette variables
- **WHEN** palette CSS file is loaded
- **THEN** all colors, typography, spacing, and other palette-specific values are defined as CSS variables (e.g., `--color-background`, `--color-text`, `--color-primary`)

#### Scenario: Theme CSS references variables
- **WHEN** theme stylesheet applies styles
- **THEN** all palette-dependent properties reference CSS variables using `var()` function (e.g., `background-color: var(--color-background)`)

---

### Requirement: Scope palette variables with data attribute selectors

The system SHALL scope all palette CSS variables under `[data-palette="<name>"]` attribute selectors.

#### Scenario: Dark palette scoped
- **WHEN** dark.css palette file is loaded
- **THEN** all variables are scoped under `[data-palette="dark"] { --color-background: #1a1a1a; ... }`

#### Scenario: Light palette scoped
- **WHEN** light.css palette file is loaded
- **THEN** all variables are scoped under `[data-palette="light"] { --color-background: #ffffff; ... }`

#### Scenario: Custom palette scoped
- **WHEN** custom palette CSS is loaded with name "ocean"
- **THEN** all variables are scoped under `[data-palette="ocean"] { ... }`

---

### Requirement: Standardize variable names across all palettes

The system SHALL use consistent CSS variable names across all bundled and custom palettes.

#### Scenario: Same variable name in multiple palettes
- **WHEN** dark.css defines `--color-background: #1a1a1a` and light.css defines `--color-background: #ffffff`
- **THEN** both use the exact same variable name `--color-background` with different values

#### Scenario: All bundled palettes use standard variable set
- **WHEN** any bundled palette CSS file is examined
- **THEN** it defines all required standard variables (background, text, primary, secondary, accent, borders, shadows, etc.)

---

### Requirement: Link all configured palette CSS files in HTML head

The system SHALL include `<link>` elements for all configured palette CSS files in the `<head>` section during build.

#### Scenario: Multiple palettes configured
- **WHEN** selector.options contains "dark" and "light" palettes
- **THEN** HTML `<head>` includes both `<link rel="stylesheet" href="css/palettes/dark.css">` and `<link rel="stylesheet" href="css/palettes/light.css">`

#### Scenario: Custom palette configured
- **WHEN** selector.options contains custom palette with css path "assets/custom.css"
- **THEN** HTML `<head>` includes `<link rel="stylesheet" href="assets/custom.css">`

#### Scenario: Only default palette when selector disabled
- **WHEN** selector.enabled is false and default is "dark"
- **THEN** HTML `<head>` includes only `<link rel="stylesheet" href="css/palettes/dark.css">`

---

### Requirement: Apply palette on HTML element via data attribute

The system SHALL control active palette by setting `data-palette` attribute on the `<html>` element.

#### Scenario: Default palette applied at build time
- **WHEN** HTML is rendered with default palette "dark"
- **THEN** `<html>` element has `data-palette="dark"` attribute in server-rendered HTML

#### Scenario: Palette switched at runtime
- **WHEN** JavaScript changes palette from "dark" to "light"
- **THEN** JavaScript updates `<html>` element's `data-palette` attribute to "light"

#### Scenario: CSS scoping activates correct palette
- **WHEN** `<html data-palette="dark">` is set
- **THEN** browser applies CSS variables from `[data-palette="dark"]` selector, overriding other palette definitions

---

### Requirement: Support palette switching without page reload

The system SHALL enable palette changes by modifying the data attribute without reloading assets or the page.

#### Scenario: Instant visual update on palette change
- **WHEN** data-palette attribute changes from "dark" to "light"
- **THEN** browser immediately re-evaluates CSS and updates all styled elements without page reload or asset fetching

#### Scenario: No new CSS loaded on switch
- **WHEN** palette switches from "blueberry" to "pink"
- **THEN** no new CSS files are requested (all palette CSS pre-linked in `<head>`)
