# CSS Architecture for Palette Selector

This document explains how the CSS architecture supports runtime palette switching in a static site context.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    BUILD TIME (MkDocs)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Configuration Processing (PalettePlugin)                │
│     • Parse mkdocs.yml palette config                       │
│     • Validate bundled/custom palettes                      │
│     • Normalize to standard format                          │
│     • Expose to Jinja2 templates                            │
│                                                             │
│  2. Template Rendering (styles.html)                        │
│     • Set data-palette attribute on <html>                  │
│     • Link ALL configured palette CSS files                 │
│     • Embed available palettes in data attribute            │
│     • Inject inline FOUC prevention script                  │
│                                                             │
│  3. Static HTML Output                                      │
│     <html data-palette="dark"                               │
│           data-available-palettes='["dark","light"]'>       │
│       <head>                                                │
│         <script>/* FOUC prevention */</script>              │
│         <link href="css/terminal.css">                      │
│         <link href="css/theme.css">                         │
│         <link href="css/palettes/dark.css">                 │
│         <link href="css/palettes/light.css">                │
│       </head>                                               │
│     </html>                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   RUNTIME (Browser)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Inline Script Executes (before CSS parsing)             │
│     • Read localStorage                                     │
│     • Validate against data-available-palettes              │
│     • Update data-palette attribute if valid                │
│     Result: <html data-palette="light">                     │
│                                                             │
│  2. CSS Cascade Resolves                                    │
│     terminal.css → theme.css → palettes → consuming code    │
│                                                             │
│  3. User Interaction (palette selector UI)                  │
│     • Click/change palette                                  │
│     • JS updates data-palette attribute                     │
│     • CSS cascade instantly updates                         │
│     • Save to localStorage                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## CSS Load Order & Variable Resolution

```
LOAD ORDER:
───────────

1. terminal.css
   ┌────────────────────────────────────────┐
   │ :root {                                │
   │   /* Structural variables ONLY */      │
   │   --global-font-size: 15px;            │
   │   --global-line-height: 1.4em;         │
   │   --page-width: 60em;                  │
   │   /* NO color variables */             │
   │ }                                      │
   └────────────────────────────────────────┘

2. theme.css
   ┌────────────────────────────────────────┐
   │ :root {                                │
   │   /* Compatibility layer */            │
   │   --font-color: var(                   │
   │     --mkdocs-terminal-font-color,      │ ← Prefer namespaced
   │     #151515                          │ ← Actual default value
   │   );                                   │   (NOT circular ref!)
   │   --background-color: var(             │
   │     --mkdocs-terminal-bg-color,        │
   │     #fff                             │
   │   );                                   │
   │   /* ...all variables... */            │
   │ }                                      │
   └────────────────────────────────────────┘

3. palettes/dark.css
   ┌────────────────────────────────────────┐
   │ :root {                                │
   │   /* Color constants only */           │
   │   --dark-bg: #222225;                │
   │   --dark-fg: #e8e9ed;                │
   │   /* ... other constants ... */        │
   │ }                                      │ ← No variable mappings!
   │                                        │   (prevents conflicts)
   │ [data-palette="dark"] {                │ ← Only applies when
   │   /* Namespaced (primary) */           │   data-palette="dark"
   │   --mkdocs-terminal-font-color:        │
   │     var(--dark-fg);                    │
   │   --mkdocs-terminal-bg-color:          │
   │     var(--dark-bg);                    │
   │                                        │
   │   /* Legacy alias (consistency) */     │
   │   --font-color: var(                   │
   │     --mkdocs-terminal-font-color       │
   │   );                                   │
   │   --background-color: var(             │
   │     --mkdocs-terminal-bg-color         │
   │   );                                   │
   │ }                                      │
   └────────────────────────────────────────┘

4. palettes/light.css
   ┌────────────────────────────────────────┐
   │ :root {                                │
   │   /* Color constants only */           │
   │   --light-bg: #fff;                  │
   │   --light-fg: #151515;               │
   │   /* ... other constants ... */        │
   │ }                                      │ ← No variable mappings!
   │                                        │
   │ [data-palette="light"] {               │ ← Only applies when
   │   --mkdocs-terminal-font-color:        │   data-palette="light"
   │     var(--light-fg);                   │
   │   --mkdocs-terminal-bg-color:          │
   │     var(--light-bg);                   │
   │   --font-color: var(                   │
   │     --mkdocs-terminal-font-color       │
   │   );                                   │
   │   --background-color: var(             │
   │     --mkdocs-terminal-bg-color         │
   │   );                                   │
   │ }                                      │
   └────────────────────────────────────────┘

5. extra_css/custom-ocean.css (if user provides)
   ┌────────────────────────────────────────┐
   │ :root {                                │
   │   --font-color: #003366;             │ ← Overrides theme.css
   │   --background-color: #e6f2ff;       │   :root via cascade
   │ }                                      │   (same specificity,
   │                                        │    but loads later)
   └────────────────────────────────────────┘


RESOLUTION EXAMPLES:
────────────────────

Example A: Dark palette active (data-palette="dark")
──────────────────────────────────────────────────

var(--font-color)
→ theme.css: var(--mkdocs-terminal-font-color, var(--font-color))
→ palettes/dark.css defines --mkdocs-terminal-font-color: #e8e9ed
→ Result: #e8e9ed ✅


Example B: Custom palette in extra_css (no data-palette, or unmatched)
────────────────────────────────────────────────────────────────────

var(--font-color)
→ theme.css: var(--mkdocs-terminal-font-color, var(--font-color))
→ --mkdocs-terminal-font-color undefined (no matching [data-palette])
→ Fallback: var(--font-color)
→ extra_css :root overrode --font-color to #003366
→ Result: #003366 ✅


Example C: No palette active, no custom CSS
────────────────────────────────────────────

var(--font-color)
→ theme.css: var(--mkdocs-terminal-font-color, #151515)
→ --mkdocs-terminal-font-color undefined (no matching [data-palette])
→ Fallback: #151515
→ Result: #151515 ✅ (default from theme.css fallback)
```

## Specificity Analysis

Understanding CSS specificity is critical to how this architecture works:

```
SPECIFICITY VALUES:
───────────────────

:root                         = (0,0,1)  ← Type selector
[data-palette="dark"]         = (0,1,0)  ← Attribute selector

RULE: Higher specificity wins. If equal, cascade order wins.


SCENARIO: Which definition wins?

┌──────────────────────────────────────────────────────┐
│ :root {                                              │
│   --font-color: #151515;  ← Specificity: (0,0,1)   │
│ }                                                    │
└──────────────────────────────────────────────────────┘
                    VS
┌──────────────────────────────────────────────────────┐
│ [data-palette="dark"] {                              │
│   --font-color: #e8e9ed;  ← Specificity: (0,1,0)   │
│ }                                                    │
└──────────────────────────────────────────────────────┘

Result: [data-palette] wins when <html data-palette="dark">
        :root wins when no data-palette or doesn't match


SCENARIO: Multiple :root definitions

┌──────────────────────────────────────────────────────┐
│ /* terminal.css */                                   │
│ :root {                                              │
│   --font-color: #151515;  ← Specificity: (0,0,1)   │
│ }                                                    │
└──────────────────────────────────────────────────────┘
                    VS
┌──────────────────────────────────────────────────────┐
│ /* theme.css */                                      │
│ :root {                                              │
│   --font-color: var(...); ← Specificity: (0,0,1)     │
│ }                                                    │
└──────────────────────────────────────────────────────┘
                    VS
┌──────────────────────────────────────────────────────┐
│ /* extra_css/custom.css */                           │
│ :root {                                              │
│   --font-color: #003366;  ← Specificity: (0,0,1)   │
│ }                                                    │
└──────────────────────────────────────────────────────┘

Result: Equal specificity → cascade order wins → extra_css wins
```

## Critical Architecture Decision: Palette :root Blocks

**IMPORTANT**: When the palette selector is enabled and multiple palette CSS files are loaded simultaneously, palette files MUST NOT define variable mappings in their `:root` blocks.

**What is a "variable mapping"?** Any CSS variable definition that assigns theme variables (like `--mkdocs-terminal-bg-color`, `--font-color`, `--background-color`, etc.) to color values or other variables. These MUST only exist in `[data-palette]` blocks.

**What IS allowed in `:root`?** Only palette-specific color constants that are then referenced by the `[data-palette]` block.

### ❌ WRONG: Variable Mappings in :root

```css
/* dark.css - DO NOT DO THIS! */
:root {
  /* Color constants (OK) */
  --dark-bg: #222225;
  --dark-fg: #e8e9ed;
  
  /* ❌ WRONG: Variable mappings in :root */
  --mkdocs-terminal-bg-color: var(--dark-bg);
  --mkdocs-terminal-font-color: var(--dark-fg);
  --background-color: var(--mkdocs-terminal-bg-color);
  --font-color: var(--mkdocs-terminal-font-color);
  /* These will conflict when multiple palettes load! */
}

[data-palette="dark"] {
  /* Duplicate mappings here won't help - :root already broke it */
  --mkdocs-terminal-bg-color: var(--dark-bg);
  --font-color: var(--mkdocs-terminal-font-color);
}
```

### ✅ CORRECT: Constants Only in :root

```css
/* dark.css - THIS IS CORRECT */
:root {
  /* ✅ Color constants ONLY - no assignments to theme variables */
  --dark-bg: #222225;
  --dark-fg: #e8e9ed;
  --dark-primary: #62c4ff;
  /* Just the hex values, nothing else */
}

[data-palette="dark"] {
  /* ✅ ALL variable mappings go here */
  --mkdocs-terminal-bg-color: var(--dark-bg);
  --mkdocs-terminal-font-color: var(--dark-fg);
  --mkdocs-terminal-primary-color: var(--dark-primary);
  
  /* Legacy aliases */
  --background-color: var(--mkdocs-terminal-bg-color);
  --font-color: var(--mkdocs-terminal-font-color);
  --primary-color: var(--mkdocs-terminal-primary-color);
}
```

### The Problem

When multiple palettes are loaded:
```css
/* dark.css */
:root {
  --mkdocs-terminal-font-color: #e8e9ed;  /* Grabs global :root */
}

/* light.css */  
:root {
  --mkdocs-terminal-font-color: #151515;  /* Overrides dark.css! */
}

/* gruvbox_dark.css (loads last) */
:root {
  --mkdocs-terminal-font-color: #ebdbb2;  /* Wins globally! */
}
```

**Result**: The last-loaded palette's `:root` block sets variables globally, completely ignoring the `data-palette` attribute. Changing `data-palette="dark"` has no effect because gruvbox already set everything in `:root`.

### The Solution

Palette `:root` blocks ONLY define color constants:
```css
/* dark.css */
:root {
  /* Color constants (no conflicts, just values) */
  --dark-bg: #222225;
  --dark-fg: #e8e9ed;
}

[data-palette="dark"] {
  /* Variable mappings ONLY in attribute selector */
  --mkdocs-terminal-font-color: var(--dark-fg);
  --mkdocs-terminal-bg-color: var(--dark-bg);
  --font-color: var(--mkdocs-terminal-font-color);
  --background-color: var(--mkdocs-terminal-bg-color);
}
```

**Why This Works**:
- `:root` color constants don't conflict (just hex values)
- `[data-palette="dark"]` has higher specificity than `:root`
- Only the matching palette's `[data-palette]` block applies
- Changing the attribute instantly switches palettes

### Inline `<link>` Support

The `:root` block in palette files exists to support inline `<link href="palettes/dark.css">` usage when the selector is **disabled**. In this case:
- Only ONE palette CSS file is loaded
- No `:root` conflicts
- Theme.css compatibility layer handles the mapping

When selector is **enabled**, the `:root` blocks are ignored (only constants used by `[data-palette]` blocks).

## Why This Architecture?

### ✅ Advantages

**No Breaking Changes**
- Existing custom palettes in extra_css continue working
- Legacy variable names supported indefinitely
- No forced migration for users

**Runtime Switching**
- Changing `data-palette` attribute instantly updates palette
- No CSS file loading/unloading needed
- No FOUC when switching palettes

**Static Site Compatible**
- All CSS pre-linked at build time
- No server required for palette switching
- Works entirely in browser with JavaScript

**Future-Proof**
- New namespaced variables provide clear API
- Compatibility layer can be removed in future major version (if desired)
- Easy to add new palette variables

**Maintainable**
- Single source of truth for each color (namespaced var)
- Legacy aliases reference namespaced vars (no duplication)
- Clear separation: terminal.css (defaults), theme.css (compat), palettes (values)

### ⚠️ Trade-offs

**CSS File Size**
- Must include ALL palette CSS files (not just active one)
- 9 bundled palettes ≈ 18 KB total (acceptable for docs sites)
- Authors can limit to configured palettes only

**Complexity**
- Three-layer variable resolution (terminal → theme → palette)
- Fallback chain requires understanding CSS custom properties
- More documentation needed for custom palette authors
- **Critical**: Palette :root blocks must ONLY contain color constants (not variable mappings)
- Easy to accidentally break by adding variables to :root when multiple palettes load

**Migration Effort**
- All 9 bundled palettes need refactoring
- Must add compatibility layer to theme.css
- Must update templates to link all palettes

## Known Limitations

### Inline Link Override Specificity Issue

**Problem**: When a site has a palette configured in `mkdocs.yml` (e.g., `palette: gruvbox_dark`), the `data-palette="gruvbox_dark"` attribute is set on the `<html>` element. If a documentation page then tries to override this by including an inline `<link href="../../css/palettes/default.css" rel="stylesheet">`, the styles don't apply because:

- `[data-palette="gruvbox_dark"]` has specificity (0,1,0)
- `:root` has specificity (0,0,1)
- The configured palette's `[data-palette]` selector wins

**Example Scenario**:
```yaml
# mkdocs.yml
theme:
  palette: gruvbox_dark
```

```markdown
<!-- some-page.md -->
# Special Page

<link href="../../css/palettes/default.css" rel="stylesheet">

This page should be light themed, but gruvbox_dark still applies.
```

**Considered Solutions**:
1. Add `[data-palette-override="name"]` selectors to all palettes + JavaScript detection
2. Add higher-specificity selectors for inline usage
3. Document workaround: Don't configure a default palette if inline overrides are needed

**Decision**: **Not implementing** - This is an extreme edge case. The recommended pattern is:
- Use palette selector feature for theme-wide switching
- Don't configure a default palette if individual pages need different palettes
- For per-page customization, use CSS variables in page-level `<style>` blocks instead

This limitation is acceptable because:
- Very rare use case (configured palette + inline link override)
- Simple workaround exists (don't configure default palette)
- Adding support would require additional JavaScript complexity
- CSS specificity is working as designed

## Custom Palette Template

Authors creating custom palettes should follow this exact structure:

```css
/**
 * Custom Palette Template for mkdocs-terminal
 * Replace "mypalette" and colors with your values
 */

/* CRITICAL: Define color constants in :root, NOT variable mappings!
 * When multiple palettes load (selector enabled), only the last :root
 * block wins. Variable mappings MUST be in [data-palette] only. */

:root {
    /* Color constants - each hex code defined once */
    --mypalette-bg: #yourcolor;
    --mypalette-fg: #yourcolor;
    --mypalette-primary: #yourcolor;
    --mypalette-secondary: #yourcolor;
    --mypalette-error: #yourcolor;
    --mypalette-code-bg: #yourcolor;
    
    /* DO NOT define --mkdocs-terminal-* or --font-color here! */
}

/* Palette scoping - only applies when data-palette="mypalette" */
[data-palette="mypalette"] {
    /* Required namespaced variables */
    --mkdocs-terminal-bg-color: var(--mypalette-bg);
    --mkdocs-terminal-font-color: var(--mypalette-fg);
    --mkdocs-terminal-invert-font-color: var(--mypalette-bg);
    --mkdocs-terminal-primary-color: var(--mypalette-primary);
    --mkdocs-terminal-secondary-color: var(--mypalette-secondary);
    --mkdocs-terminal-tertiary-color: var(--mypalette-secondary);
    --mkdocs-terminal-error-color: var(--mypalette-error);
    --mkdocs-terminal-progress-bar-bg: var(--mypalette-secondary);
    --mkdocs-terminal-progress-bar-fill: var(--mypalette-fg);
    --mkdocs-terminal-code-bg-color: var(--mypalette-code-bg);
    --mkdocs-terminal-input-style: solid;
    --mkdocs-terminal-h1-decoration: none;
    
    /* Typography (optional, use defaults if omitted) */
    --mkdocs-terminal-font-size: 15px;
    --mkdocs-terminal-line-height: 1.4em;
    --mkdocs-terminal-spacing: 10px;
    --mkdocs-terminal-font-family: Menlo, Monaco, monospace;
    --mkdocs-terminal-mono-font-family: Menlo, Monaco, monospace;
    --mkdocs-terminal-page-width: 60em;
    
    /* Legacy variable aliases (for backwards compatibility) */
    --background-color: var(--mkdocs-terminal-bg-color);
    --font-color: var(--mkdocs-terminal-font-color);
    --invert-font-color: var(--mkdocs-terminal-invert-font-color);
    --primary-color: var(--mkdocs-terminal-primary-color);
    --secondary-color: var(--mkdocs-terminal-secondary-color);
    --tertiary-color: var(--mkdocs-terminal-tertiary-color);
    --error-color: var(--mkdocs-terminal-error-color);
    --progress-bar-background: var(--mkdocs-terminal-progress-bar-bg);
    --progress-bar-fill: var(--mkdocs-terminal-progress-bar-fill);
    --code-bg-color: var(--mkdocs-terminal-code-bg-color);
    --input-style: var(--mkdocs-terminal-input-style);
    --display-h1-decoration: var(--mkdocs-terminal-h1-decoration);
    --global-font-size: var(--mkdocs-terminal-font-size);
    --global-line-height: var(--mkdocs-terminal-line-height);
    --global-space: var(--mkdocs-terminal-spacing);
    --font-stack: var(--mkdocs-terminal-font-family);
    --mono-font-stack: var(--mkdocs-terminal-mono-font-family);
    --page-width: var(--mkdocs-terminal-page-width);
}
```

**Usage in mkdocs.yml**:
```yaml
theme:
  name: terminal
  palette:
    default: mypalette
    selector:
      enabled: true
      options:
        - dark  # bundled palette
        - name: mypalette
          css: css/mypalette.css  # custom palette

extra_css:
  - css/mypalette.css  # Required for MkDocs to copy the file
```

**Key Points**:
1. `:root` = color constants ONLY (no variable mappings)
2. `[data-palette]` = ALL variable mappings (namespaced + legacy)
3. Reference constants via `var(--mypalette-name)` for DRY
4. Include legacy aliases for backwards compatibility
5. Add file to `extra_css` in mkdocs.yml

## Testing Strategy

To validate this architecture:

1. **Unit tests** for compatibility layer
   - Test legacy-only variables resolve
   - Test namespaced-only variables resolve
   - Test mixed variables (namespaced takes precedence)

2. **Integration tests** for palette switching
   - Test data-palette attribute changes apply styles
   - Test invalid palette names don't crash
   - Test no-JS fallback (default palette)

3. **E2E tests** for complete flow
   - Build site with multiple palettes
   - Switch palettes via UI
   - Verify localStorage persistence
   - Test custom palette in extra_css

4. **Visual regression tests**
   - Render pages with each palette
   - Compare against baseline screenshots
   - Catch unintended color changes
