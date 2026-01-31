# Palette Client Switching Specification

## ADDED Requirements

### Requirement: Restore saved palette on page load

The system SHALL check localStorage for saved palette preference and apply it before first paint.

#### Scenario: Saved palette exists and is valid
- **WHEN** page loads and localStorage contains "mkdocs-terminal-palette": "dark"
- **THEN** inline script sets `data-palette="dark"` on `<html>` element before CSS parsing

#### Scenario: Saved palette exists but is invalid
- **WHEN** page loads and localStorage contains palette name not in configured options
- **THEN** inline script applies default palette and updates localStorage with default

#### Scenario: No saved palette exists
- **WHEN** page loads and localStorage does not contain "mkdocs-terminal-palette" key
- **THEN** default palette from configuration applies (via server-rendered `data-palette` attribute)

---

### Requirement: Prevent FOUC on palette restoration

The system SHALL restore saved palette synchronously before CSS files are parsed to prevent flash of unstyled content.

#### Scenario: Inline script in head before CSS
- **WHEN** HTML `<head>` is parsed
- **THEN** inline palette restoration script executes before any `<link rel="stylesheet">` elements

#### Scenario: Synchronous execution
- **WHEN** inline script executes
- **THEN** script runs synchronously (not deferred or async) to block CSS parsing until palette is set

#### Scenario: No visible flash
- **WHEN** user has saved palette "light" but default is "dark"
- **THEN** user sees "light" palette immediately on page load without flash of "dark" palette

---

### Requirement: Apply palette change on user interaction

The system SHALL update the active palette when user interacts with selector UI.

#### Scenario: Toggle button clicked
- **WHEN** user clicks toggle button to switch from "dark" to "light"
- **THEN** JavaScript sets `data-palette="light"` on `<html>` element

#### Scenario: Select dropdown changed
- **WHEN** user selects "blueberry" from dropdown
- **THEN** JavaScript sets `data-palette="blueberry"` on `<html>` element

#### Scenario: Instant visual feedback
- **WHEN** palette is changed via UI
- **THEN** page styles update immediately without delay or page reload

---

### Requirement: Persist palette preference to localStorage

The system SHALL save user's palette selection to localStorage for persistence across sessions.

#### Scenario: Palette changed and saved
- **WHEN** user selects "light" palette
- **THEN** JavaScript writes `localStorage.setItem("mkdocs-terminal-palette", "light")`

#### Scenario: Preference persists across page loads
- **WHEN** user selects palette, navigates to another page, and returns
- **THEN** selected palette is still active

#### Scenario: Preference persists across browser sessions
- **WHEN** user selects palette, closes browser, and reopens site
- **THEN** selected palette is still active

---

### Requirement: Gracefully degrade when localStorage unavailable

The system SHALL continue to function when localStorage is disabled or unavailable.

#### Scenario: localStorage disabled
- **WHEN** localStorage.setItem() throws exception (disabled, quota exceeded, private browsing)
- **THEN** palette selection still works during current session but does not persist

#### Scenario: Silent failure on save error
- **WHEN** localStorage.setItem() fails
- **THEN** JavaScript catches exception and continues without showing error to user

#### Scenario: Selector remains functional
- **WHEN** localStorage is unavailable
- **THEN** user can still switch palettes via UI and changes apply immediately

---

### Requirement: Update selector UI to reflect active palette

The system SHALL synchronize selector UI state with the active palette.

#### Scenario: Update toggle button after change
- **WHEN** palette switches from "dark" to "light" via toggle
- **THEN** toggle button updates visual state to show "light" is active

#### Scenario: Update select dropdown after change
- **WHEN** palette switches via dropdown selection
- **THEN** selected option in dropdown updates to match active palette

#### Scenario: Update UI after programmatic change
- **WHEN** palette is set by inline restoration script
- **THEN** selector UI initializes with correct active state when page finishes loading

---

### Requirement: Validate palette option before applying

The system SHALL check that requested palette exists in configured options before applying.

#### Scenario: Valid palette requested
- **WHEN** user selects "dark" palette and "dark" is in configured options
- **THEN** system applies "dark" palette

#### Scenario: Invalid palette requested
- **WHEN** user selects palette name not in configured options (edge case: tampered localStorage)
- **THEN** system ignores request and keeps current palette

#### Scenario: Fallback to default for invalid saved preference
- **WHEN** localStorage contains invalid palette name
- **THEN** system applies default palette and updates localStorage

---

### Requirement: Include selector JavaScript only when enabled

The system SHALL conditionally include palette_selector.js script only when `selector.enabled: true`.

#### Scenario: Selector enabled - include script
- **WHEN** configuration has `selector.enabled: true`
- **THEN** HTML includes `<script src="js/palette_selector.js">` in page

#### Scenario: Selector disabled - no script
- **WHEN** configuration has `selector.enabled: false`
- **THEN** HTML does not include palette_selector.js (no unnecessary JavaScript)

#### Scenario: FOUC prevention script always included when options exist
- **WHEN** palette options are configured (even if selector UI is disabled)
- **THEN** inline FOUC prevention script is included in `<head>`
