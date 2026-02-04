# Palette Variable Reference

This document lists all palette variables supported by mkdocs-terminal, including both the new namespaced format and legacy aliases.

## Variable Naming Convention

**Namespaced variables** (recommended for new palettes):
- Format: `--mkdocs-terminal-{category}-{element}`
- Example: `--mkdocs-terminal-font-color`

**Legacy variables** (backwards compatibility):
- Format: `--{element}-{category}` or `--{element}`
- Example: `--font-color`

## Required Color Variables

| Namespaced Variable | Legacy Alias | Description | Example Value |
|---------------------|--------------|-------------|---------------|
| `--mkdocs-terminal-font-color` | `--font-color` | Primary text color | `#003366` |
| `--mkdocs-terminal-bg-color` | `--background-color` | Main background | `#e6f2ff` |
| `--mkdocs-terminal-invert-font-color` | `--invert-font-color` | Text on colored backgrounds | `#ffffff` |
| `--mkdocs-terminal-primary-color` | `--primary-color` | Links, buttons, highlights | `#0066cc` |
| `--mkdocs-terminal-secondary-color` | `--secondary-color` | Muted elements | `#5599dd` |
| `--mkdocs-terminal-tertiary-color` | `--tertiary-color` | Alternative muted elements | `#5599dd` |
| `--mkdocs-terminal-error-color` | `--error-color` | Errors, warnings | `#cc3300` |
| `--mkdocs-terminal-progress-bar-bg` | `--progress-bar-background` | Progress bar background | `#ccddee` |
| `--mkdocs-terminal-progress-bar-fill` | `--progress-bar-fill` | Progress bar fill | `#003366` |
| `--mkdocs-terminal-code-bg-color` | `--code-bg-color` | Code block background | `#f0f8ff` |
| `--mkdocs-terminal-input-style` | `--input-style` | Input border style | `solid` |
| `--mkdocs-terminal-h1-decoration` | `--display-h1-decoration` | H1 decoration | `none` |

## Optional Typography Variables

| Namespaced Variable | Legacy Alias | Description | Default Value |
|---------------------|--------------|-------------|---------------|
| `--mkdocs-terminal-font-size` | `--global-font-size` | Base font size | `15px` |
| `--mkdocs-terminal-line-height` | `--global-line-height` | Line height | `1.4em` |
| `--mkdocs-terminal-spacing` | `--global-space` | Global spacing unit | `10px` |
| `--mkdocs-terminal-font-family` | `--font-stack` | Font family stack | Monospace stack |
| `--mkdocs-terminal-mono-font-family` | `--mono-font-stack` | Monospace font stack | Monospace stack |
| `--mkdocs-terminal-page-width` | `--page-width` | Maximum page width | `60em` |

## Compatibility Layer

The theme includes a compatibility layer in `terminal/css/theme.css` that maps legacy variables to namespaced ones:

```css
:root {
  --font-color: var(--mkdocs-terminal-font-color, var(--font-color));
  --background-color: var(--mkdocs-terminal-bg-color, var(--background-color));
  /* ...etc... */
}
```

**How it works:**
1. If palette defines `--mkdocs-terminal-font-color`, it's used
2. Otherwise, falls back to `--font-color` (from palette or terminal.css default)
3. If neither defined, uses terminal.css default value

**This means:**
- ✅ Old custom palettes using `:root { --font-color: ...; }` still work
- ✅ New palettes using `[data-palette] { --mkdocs-terminal-font-color: ...; }` work
- ✅ Hybrid palettes with both namespaced and legacy variables work
- ✅ No breaking changes for existing users

## Best Practices

### For Custom Palettes (with Selector Feature)

**Recommended:**
```css
[data-palette="mypalette"] {
  /* Define namespaced variables (primary source of truth) */
  --mkdocs-terminal-font-color: #003366;
  
  /* Alias legacy variables for consistency */
  --font-color: var(--mkdocs-terminal-font-color);
}
```

**Minimal (works but not recommended):**
```css
[data-palette="mypalette"] {
  /* Only legacy variables */
  --font-color: #003366;
}
```

### For Custom Palettes (without Selector Feature)

If you're not using the palette selector and just want to override colors:

```css
:root {
  --font-color: #003366;
  --background-color: #e6f2ff;
  /* ...etc... */
}
```

This approach:
- ✅ Works via CSS cascade (last `:root` wins)
- ✅ No need for `[data-palette]` scoping
- ❌ Cannot be used with palette selector dropdown
- ❌ Not namespaced (potential collision with user's extra_css)

## Accessibility Requirements

All custom palettes should meet **WCAG AA contrast standards**:

- **Normal text:** Minimum 4.5:1 contrast ratio
- **Large text (18pt+):** Minimum 3:1 contrast ratio
- **UI components:** Minimum 3:1 contrast ratio

Use tools like [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to validate your color choices.

## Migration from Legacy Format

If you have an existing custom palette using legacy variables in `:root`:

**Before (legacy, still works):**
```css
:root {
  --font-color: #003366;
  --background-color: #e6f2ff;
}
```

**After (recommended for selector support):**
```css
[data-palette="ocean"] {
  --mkdocs-terminal-font-color: #003366;
  --mkdocs-terminal-bg-color: #e6f2ff;
  
  --font-color: var(--mkdocs-terminal-font-color);
  --background-color: var(--mkdocs-terminal-bg-color);
}
```

See [design.md Custom Palette Migration Guide](../design.md#custom-palette-migration-guide) for detailed migration steps.
