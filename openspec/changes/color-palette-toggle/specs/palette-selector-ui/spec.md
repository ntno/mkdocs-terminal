# Palette Selector UI Specification

## ADDED Requirements

### Requirement: Render selector partial when enabled

The system SHALL render the palette selector UI partial only when `selector.enabled` is `true`.

#### Scenario: Selector enabled
- **WHEN** configuration has `selector.enabled: true`
- **THEN** palette_selector.html partial renders in the page

#### Scenario: Selector disabled
- **WHEN** configuration has `selector.enabled: false`
- **THEN** palette_selector.html partial does not render

#### Scenario: Legacy config without selector
- **WHEN** configuration is legacy string format `palette: "dark"`
- **THEN** palette_selector.html partial does not render (selector disabled by default)

---

### Requirement: Automatically select UI control type based on option count

The system SHALL choose between toggle button and select dropdown based on the number of valid palette options when `selector.ui` is "auto".

#### Scenario: Two options - render toggle
- **WHEN** selector.options contains exactly 2 valid palettes and `selector.ui: "auto"`
- **THEN** system renders a binary toggle button control

#### Scenario: Three or more options - render select
- **WHEN** selector.options contains 3 or more valid palettes and `selector.ui: "auto"`
- **THEN** system renders a select dropdown control

#### Scenario: One option - hide selector
- **WHEN** selector.options contains only 1 valid palette
- **THEN** system does not render selector UI (nothing to switch between)

---

### Requirement: Allow author override of UI control type

The system SHALL respect author-specified `selector.ui` value when set to "toggle" or "select".

#### Scenario: Force toggle with 2 options
- **WHEN** configuration has `selector.ui: "toggle"` and 2 valid options
- **THEN** system renders toggle button control

#### Scenario: Force select with 2 options
- **WHEN** configuration has `selector.ui: "select"` and 2 valid options
- **THEN** system renders select dropdown control

#### Scenario: Invalid toggle request
- **WHEN** configuration has `selector.ui: "toggle"` and 3 or more options
- **THEN** system emits build warning and falls back to select dropdown

---

### Requirement: Render accessible toggle button UI

The system SHALL render toggle button with proper ARIA attributes and keyboard accessibility.

#### Scenario: Toggle button markup
- **WHEN** toggle UI is rendered
- **THEN** HTML contains button element with `role="button"`, `aria-label` describing the control, and `aria-pressed` or similar state attribute

#### Scenario: Toggle button keyboard navigation
- **WHEN** user tabs to toggle button
- **THEN** button receives focus with visible focus indicator

#### Scenario: Toggle button activation
- **WHEN** user presses Enter or Space on focused toggle button
- **THEN** palette switches to the other option

---

### Requirement: Render accessible select dropdown UI

The system SHALL render select dropdown with proper ARIA attributes and keyboard accessibility.

#### Scenario: Select dropdown markup
- **WHEN** select UI is rendered
- **THEN** HTML contains `<select>` element with `aria-label` describing the control and `<option>` elements for each palette

#### Scenario: Select dropdown keyboard navigation
- **WHEN** user tabs to select dropdown
- **THEN** dropdown receives focus with visible focus indicator

#### Scenario: Select dropdown option selection
- **WHEN** user opens dropdown and presses arrow keys then Enter
- **THEN** palette switches to the selected option

---

### Requirement: Display current active palette in UI

The system SHALL visually indicate which palette is currently active in the selector UI.

#### Scenario: Active toggle state
- **WHEN** toggle button is rendered and "dark" palette is active
- **THEN** toggle shows "dark" as active state (via icon, text, or visual indicator)

#### Scenario: Selected dropdown option
- **WHEN** select dropdown is rendered and "light" palette is active
- **THEN** "light" option is selected in the dropdown

#### Scenario: Update UI after palette change
- **WHEN** palette switches from "dark" to "light"
- **THEN** selector UI updates to show "light" as active

---

### Requirement: Apply responsive CSS for mobile devices

The system SHALL ensure selector UI meets WCAG touch target size requirements on mobile devices.

#### Scenario: Touch target minimum size
- **WHEN** selector UI is rendered on mobile viewport
- **THEN** all interactive elements (button, select) are at least 44x44 pixels

#### Scenario: Adequate spacing on mobile
- **WHEN** selector UI is rendered on mobile viewport
- **THEN** selector has appropriate spacing from adjacent navigation elements

---

### Requirement: Display palette names from configuration

The system SHALL display palette names exactly as defined in configuration options.

#### Scenario: Bundled palette name
- **WHEN** option has name "dark"
- **THEN** UI displays "dark" as the palette label

#### Scenario: Custom palette name
- **WHEN** option has name "Ocean Theme"
- **THEN** UI displays "Ocean Theme" as the palette label

#### Scenario: Multiple word names preserved
- **WHEN** option has name "Gruvbox Dark"
- **THEN** UI displays "Gruvbox Dark" with exact spacing and capitalization
