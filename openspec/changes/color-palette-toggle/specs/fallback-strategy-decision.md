# CSS Variable Fallback Strategy - Decision Summary

**Date:** 2026-01-31  
**Status:** Documented in explore mode  
**Context:** Phase 2 CSS Architecture for color-palette-toggle change

## The Problem

Migrating to namespaced CSS variables (`--mkdocs-terminal-*`) for palette selector feature could break existing users who have custom palettes using legacy variable names (`--font-color`, etc.).

**User constraint:** Custom palettes are currently loaded via `extra_css` after theme CSS:
```
terminal.css → theme.css → palette.css → extra_css/*.css
```

## The Solution

Add a **compatibility layer in theme.css** that maps legacy variables to namespaced versions with fallback chain.

### Implementation

**theme.css** (add at top):
```css
:root {
  --font-color: var(--mkdocs-terminal-font-color, var(--font-color));
  --background-color: var(--mkdocs-terminal-bg-color, var(--background-color));
  /* ...all 17 palette variables... */
}
```

**Bundled palettes** (dark.css, light.css, etc.):
```css
[data-palette="dark"] {
  /* Namespaced (primary source of truth) */
  --mkdocs-terminal-font-color: #e8e9ed;
  
  /* Legacy alias (for consistency) */
  --font-color: var(--mkdocs-terminal-font-color);
}
```

**Custom palettes** (user-provided):

Option A - No migration needed (backwards compatible):
```css
:root {
  --font-color: #003366;  /* Still works! */
}
```

Option B - Opt into new architecture (recommended):
```css
[data-palette="ocean"] {
  --mkdocs-terminal-font-color: #003366;
  --font-color: var(--mkdocs-terminal-font-color);  /* Alias */
}
```

## How It Works

### Scenario 1: New bundled palette
```
User action: Select "dark" palette
HTML state: <html data-palette="dark">

Resolution chain:
  var(--font-color) in terminal.css
  → theme.css: var(--mkdocs-terminal-font-color, var(--font-color))
  → [data-palette="dark"] defines --mkdocs-terminal-font-color: #e8e9ed
  → Result: #e8e9ed ✅
```

### Scenario 2: Legacy custom palette (no changes)
```
User setup: extra_css with :root { --font-color: #003366; }
HTML state: <html> (no data-palette)

Resolution chain:
  var(--font-color) in terminal.css
  → theme.css: var(--mkdocs-terminal-font-color, var(--font-color))
  → --mkdocs-terminal-font-color undefined (no matching [data-palette])
  → Fallback: var(--font-color)
  → extra_css :root overrides theme.css :root (cascade order)
  → Result: #003366 ✅
```

### Scenario 3: Migrated custom palette (with selector)
```
User setup: Registered in selector config
HTML state: <html data-palette="ocean">

Resolution chain:
  var(--font-color) in terminal.css
  → theme.css: var(--mkdocs-terminal-font-color, var(--font-color))
  → [data-palette="ocean"] defines --mkdocs-terminal-font-color: #003366
  → Result: #003366 ✅
```

## Why Include Legacy Aliases in Bundled Palettes?

**Question:** Should bundled palettes define both namespaced AND legacy variables?

```css
[data-palette="dark"] {
  --mkdocs-terminal-font-color: #e8e9ed;  /* Required */
  --font-color: var(--mkdocs-terminal-font-color);  /* Optional? */
}
```

**Answer:** Yes, include aliases. They are **technically optional** but **strongly recommended**.

### Without Aliases (works, but not ideal)
- ✅ Palette works (CSS specificity: `[data-palette]` > `:root`)
- ⚠️ Creates separate definitions in different scopes
- ⚠️ Bypasses the designed fallback mechanism
- ⚠️ Less clear intent for maintainers
- ⚠️ If namespaced and legacy ever diverge, unpredictable behavior

### With Aliases (recommended)
- ✅ Palette works via designed fallback mechanism
- ✅ Single source of truth (define color once, alias it)
- ✅ Consistent with architecture
- ✅ Future-proof (if theme ever references namespaced vars directly)
- ✅ Clear intent for developers

**Verdict:** Include aliases for consistency, clarity, and future-proofing.

## Benefits

### For Users
- ✅ No breaking changes (existing custom palettes work)
- ✅ Optional migration (can upgrade when ready)
- ✅ Clear documentation (know which variables to use)

### For Maintainers
- ✅ Clean namespaced API going forward
- ✅ Backwards compatibility maintained
- ✅ Single compatibility layer (theme.css, ~20 lines)
- ✅ Can deprecate legacy vars in future major version (if desired)

### For Theme
- ✅ No changes to terminal.css (largest CSS file, ~1000 lines)
- ✅ Minimal changes to theme.css (add one :root block)
- ✅ Bundled palettes follow consistent pattern

## Trade-offs

**Complexity:**
- Three-layer variable resolution (terminal → theme → palette)
- Requires understanding CSS custom properties and fallbacks
- More documentation needed

**Maintenance:**
- Must update compatibility layer when adding new variables
- Must document both namespaced and legacy names
- Potential confusion ("which one should I use?")

**Performance:**
- Negligible (CSS custom property fallback is fast)
- No runtime JavaScript overhead
- No additional HTTP requests

## Documentation Requirements

1. **Design.md** - Architecture rationale and migration guide ✅
2. **Tasks.md** - Implementation steps for Phase 2 ✅
3. **custom-palette-template.css** - Annotated example ✅
4. **variable-reference.md** - Complete variable list ✅
5. **css-architecture.md** - Visual diagrams and examples ✅
6. **User-facing docs** - Phase 6, after implementation complete

## Alternatives Considered

### Alternative 1: No compatibility layer, force migration
```css
/* Bundled palettes only */
[data-palette="dark"] {
  --mkdocs-terminal-font-color: #e8e9ed;
}

/* Custom palettes MUST migrate */
[data-palette="ocean"] {
  --mkdocs-terminal-font-color: #003366;
}
```

**Rejected because:**
- ❌ Breaking change for existing users
- ❌ Violates project's no-breaking-changes goal
- ❌ Forces migration before selector adoption
- ❌ Poor user experience

### Alternative 2: Build-time CSS transformation
```python
# In palette validation
def normalize_palette_variables(css_content):
    if '--font-color:' in css_content:
        # Inject: --mkdocs-terminal-font-color: var(--font-color);
```

**Rejected because:**
- ❌ Build-time transformation complexity
- ❌ Generated CSS doesn't match source (confusing for debugging)
- ❌ Harder to understand for palette authors
- ❌ Doesn't solve the problem (still need to handle :root override)

### Alternative 3: Keep legacy names, no namespacing
```css
/* Just add scoping, keep variable names */
[data-palette="dark"] {
  --font-color: #e8e9ed;  /* No namespace */
}
```

**Rejected because:**
- ❌ Generic names increase collision risk with user CSS
- ❌ Harder to debug (grep for `--font-color` finds too many results)
- ❌ Less clear ownership (is this a theme var or user var?)
- ❌ Missed opportunity to improve developer experience

## Decision

**Implement compatibility layer in theme.css with namespaced variables and legacy fallbacks.**

This approach:
- ✅ Maintains backwards compatibility (no breaking changes)
- ✅ Provides clean namespaced API going forward
- ✅ Minimizes changes to terminal.css (avoids touching ~1000 lines)
- ✅ Enables gradual migration for custom palette authors
- ✅ Clear documentation path

**Implementation order:**
1. Add compatibility layer to theme.css (Phase 2)
2. Refactor bundled palettes with namespaced vars + aliases (Phase 2)
3. Document migration path (Phase 2 & Phase 6)
4. (Optional) Deprecate legacy variables in future major version

## Next Steps

1. ✅ Document architecture in design.md
2. ✅ Update tasks.md with implementation details
3. ✅ Create custom-palette-template.css
4. ✅ Create variable-reference.md
5. ✅ Create css-architecture.md
6. ⏳ Implement compatibility layer (Phase 2 work)
7. ⏳ Test fallback mechanism (Phase 2 work)
8. ⏳ User-facing documentation (Phase 6 work)
