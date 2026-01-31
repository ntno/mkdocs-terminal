# Palette Configuration Specification

## ADDED Requirements

### Requirement: Parse legacy string configuration format

The system SHALL accept `palette: "string"` configuration format in mkdocs.yml and normalize it to the new object structure internally.

#### Scenario: Legacy string config provided
- **WHEN** mkdocs.yml contains `palette: "dark"`
- **THEN** system normalizes to `palette: {default: "dark", selector: {enabled: false}}`

#### Scenario: Legacy string with bundled palette name
- **WHEN** mkdocs.yml contains `palette: "blueberry"`
- **THEN** system normalizes to `palette: {default: "blueberry", selector: {enabled: false}}`

---

### Requirement: Parse new object configuration format

The system SHALL accept `palette: {object}` configuration format with `default`, `selector.enabled`, `selector.ui`, and `selector.options` fields.

#### Scenario: Minimal object config
- **WHEN** mkdocs.yml contains `palette: {default: "dark"}`
- **THEN** system applies default values: `selector.enabled: false`, `selector.ui: "auto"`, `selector.options: []`

#### Scenario: Full object config
- **WHEN** mkdocs.yml contains `palette: {default: "dark", selector: {enabled: true, ui: "select", options: [{name: "dark"}, {name: "light"}]}}`
- **THEN** system parses all fields and makes them available to templates

#### Scenario: Object config with custom palette
- **WHEN** mkdocs.yml contains `palette: {selector: {options: [{name: "custom", css: "assets/custom.css"}]}}`
- **THEN** system parses custom palette with name "custom" and CSS path "assets/custom.css"

---

### Requirement: Apply default values for missing fields

The system SHALL apply default values when optional configuration fields are missing.

#### Scenario: Missing selector.enabled field
- **WHEN** mkdocs.yml contains `palette: {default: "dark"}`
- **THEN** system sets `selector.enabled: false`

#### Scenario: Missing selector.ui field
- **WHEN** mkdocs.yml contains `palette: {selector: {enabled: true}}`
- **THEN** system sets `selector.ui: "auto"`

#### Scenario: Missing selector.options field
- **WHEN** mkdocs.yml contains `palette: {default: "dark", selector: {enabled: true}}`
- **THEN** system sets `selector.options: []` (empty list)

---

### Requirement: Make normalized config available to templates

The system SHALL expose normalized palette configuration to Jinja2 template context during build.

#### Scenario: Access default palette in template
- **WHEN** template renders with palette config `{default: "dark"}`
- **THEN** template can access `config.theme.palette.default` with value "dark"

#### Scenario: Access selector enabled state in template
- **WHEN** template renders with palette config `{selector: {enabled: true}}`
- **THEN** template can access `config.theme.palette.selector.enabled` with value `true`

#### Scenario: Access palette options in template
- **WHEN** template renders with palette config `{selector: {options: [{name: "dark"}, {name: "light"}]}}`
- **THEN** template can iterate over `config.theme.palette.selector.options` list

---

### Requirement: Embed palette options in HTML for JavaScript access

The system SHALL render palette options as data attributes or JSON in HTML for client-side JavaScript to read.

#### Scenario: Embed options as data attribute
- **WHEN** template renders with 2 palette options: "dark" and "light"
- **THEN** HTML contains data attribute with available palette names (e.g., `data-palette-options='["dark","light"]'`)

#### Scenario: Embed default palette as data attribute
- **WHEN** template renders with default palette "dark"
- **THEN** HTML contains `data-palette-default="dark"` attribute on `<html>` or selector element

#### Scenario: No options when selector disabled
- **WHEN** template renders with `selector.enabled: false`
- **THEN** HTML does not contain palette options data attributes
