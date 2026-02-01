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
   │   --font-color: #151515;             │ ← Default values
   │   --background-color: #fff;          │
   │   /* ...other defaults... */           │
   │ }                                      │
   └────────────────────────────────────────┘

2. theme.css
   ┌────────────────────────────────────────┐
   │ :root {                                │
   │   /* Compatibility layer */            │
   │   --font-color: var(                   │
   │     --mkdocs-terminal-font-color,      │ ← Prefer namespaced
   │     var(--font-color)                  │ ← Fall back to legacy
   │   );                                   │
   │   /* ...all variables... */            │
   │ }                                      │
   └────────────────────────────────────────┘

3. palettes/dark.css
   ┌────────────────────────────────────────┐
   │ [data-palette="dark"] {                │ ← Only applies when
   │   /* Namespaced (primary) */           │   data-palette="dark"
   │   --mkdocs-terminal-font-color:        │
   │     #e8e9ed;                         │
   │                                        │
   │   /* Legacy alias (consistency) */     │
   │   --font-color: var(                   │
   │     --mkdocs-terminal-font-color       │
   │   );                                   │
   │ }                                      │
   └────────────────────────────────────────┘

4. palettes/light.css
   ┌────────────────────────────────────────┐
   │ [data-palette="light"] {               │ ← Only applies when
   │   --mkdocs-terminal-font-color:        │   data-palette="light"
   │     #151515;                         │
   │   --font-color: var(                   │
   │     --mkdocs-terminal-font-color       │
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
→ theme.css: var(--mkdocs-terminal-font-color, var(--font-color))
→ --mkdocs-terminal-font-color undefined
→ Fallback: var(--font-color)
→ terminal.css :root defines --font-color: #151515
→ Result: #151515 ✅ (default from terminal.css)
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

**Migration Effort**
- All 9 bundled palettes need refactoring
- Must add compatibility layer to theme.css
- Must update templates to link all palettes

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
