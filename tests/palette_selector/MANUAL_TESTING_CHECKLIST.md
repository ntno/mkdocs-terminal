# Manual Testing Checklist for Palette Application Mechanism

This checklist covers functionality that requires a browser and cannot be automated with pytest.

## Prerequisites

Build a test site with palette selector enabled:

```bash
cd /Users/ntno/projects/ntno/mkdocs-terminal/documentation
mkdocs build
cd site && python -m http.server 8000
```

Open http://localhost:8000 in your browser.

---

## Test 1: FOUC Prevention Script Execution

**Purpose:** Verify inline script executes before CSS loads and prevents flash.

### Steps:
1. Open browser DevTools (F12)
2. Go to Console tab
3. Set localStorage: `localStorage.setItem('mkdocs-terminal-palette', 'dark')`
4. Reload page (Cmd/Ctrl+R)

### Expected Results:
- [ ] Page loads with dark palette immediately (no flash of light theme)
  - actual behavior: page did not reload with dark palette
- [x] No JavaScript errors in console
- [x] Inspect `<html>` element: `data-palette="dark"` is set

### Notes:
- Clear localStorage and test again with different palette names
- Test with invalid palette name (should ignore and use build-time default)

---

## Test 2: localStorage Persistence

**Purpose:** Verify palette selection persists across page loads and navigation.

### Steps:
1. Open browser DevTools → Console
2. Set palette: `localStorage.setItem('mkdocs-terminal-palette', 'gruvbox_dark')`  
3. Reload current page
4. Navigate to a different page
5. Navigate back

### Expected Results:
- [x] Palette remains 'gruvbox_dark' after reload
- [x] Palette remains 'gruvbox_dark' when navigating between pages
- [x] Inspect localStorage: `localStorage.getItem('mkdocs-terminal-palette')` returns `"gruvbox_dark"`

---

## Test 3: Invalid localStorage Value Handling

**Purpose:** Verify graceful handling of invalid saved palette names.

### Steps:
1. Open DevTools → Console
2. Set invalid palette: `localStorage.setItem('mkdocs-terminal-palette', 'nonexistent')`
3. Reload page
4. Check `data-palette` attribute on `<html>` element

### Expected Results:
- [x] Page loads with build-time default palette (from mkdocs.yml)
- [x] Invalid value is NOT applied to `data-palette` attribute
- [x] No JavaScript errors in console

---

## Test 4: CSS Scoping via data-palette Attribute

**Purpose:** Verify palette switching works via CSS attribute selectors.

### Steps:
1. Open page in browser
2. Open DevTools → Elements tab
3. Inspect `<html>` element
4. Manually change `data-palette` attribute:
   - In Elements panel, edit attribute: `data-palette="dark"`
   - Change to: `data-palette="light"`
   - Change to: `data-palette="gruvbox_dark"`

### Expected Results:
- [ ] Colors change instantly when attribute is modified
  - actual behavior: colors do not change
- [ ] No page reload required
- [ ] All theme elements update (background, text, links, navigation, etc.)
- [ ] Transitions are smooth with no layout shift

---

## Test 5: Multiple Palette CSS Files Loaded

**Purpose:** Verify all configured palettes are loaded when selector enabled.

### Steps:
1. Build site with selector enabled and multiple options in mkdocs.yml:
   ```yaml
   theme:
     name: terminal
     palette:
       default: dark
       selector:
         enabled: true
         options:
           - dark
           - lightyear
           - gruvbox_dark
   ```
2. Open page in browser
3. Open DevTools → Network tab
4. Reload page
5. Filter by "CSS"

### Expected Results:
- [x] `dark.css` is loaded
- [x] `lightyear.css` is loaded
- [x] `gruvbox_dark.css` is loaded
- [x] All three CSS files return 200 OK status
- [x] CSS files load in parallel (not blocking)

---

## Test 6: Selector Disabled - Only Default Palette Loaded

**Purpose:** Verify only default palette loads when selector is disabled.

### Steps:
1. Build site with selector disabled:
   ```yaml
   theme:
     name: terminal
     palette: dark
   ```
2. Open page in browser
3. Open DevTools → Network tab → Filter "CSS"
4. Reload page

### Expected Results:
- [x] Only `dark.css` is loaded
- [x] `default.css`, `lightyear.css`, etc. are NOT loaded
- [x] `data-available-palettes` attribute is empty string: `""`

---

## Test 7: Custom Palette CSS Path

**Purpose:** Verify custom palette CSS files load from correct path.

### Steps:
1. Create custom palette file: `documentation/docs/css/ocean.css`
2. Configure in mkdocs.yml:
   ```yaml
   theme:
     palette:
       default: dark
       selector:
         enabled: true
         options:
           - dark
           - name: ocean
             css: css/ocean.css
   extra_css:
     - css/ocean.css
   ```
3. Build and open in browser
4. Check DevTools → Network tab

### Expected Results:
- [ ] `css/ocean.css` loads successfully (200 OK)
- [ ] Can switch to ocean palette via: `document.documentElement.setAttribute('data-palette', 'ocean')`
- [ ] Custom palette styles apply correctly

---

## Test 8: data-available-palettes Validation

**Purpose:** Verify FOUC script validates against embedded palette list.

### Steps:
1. Build site with specific palettes configured
2. Open page and check `<html>` element's `data-available-palettes` attribute
3. Note the palette names in the array
4. In Console, set localStorage to a palette NOT in the array:
   ```javascript
   localStorage.setItem('mkdocs-terminal-palette', 'pink')
   ```
5. Reload page

### Expected Results:
- [ ] If 'pink' is NOT in `data-available-palettes`, it should NOT be applied
- [ ] Page loads with build-time default palette instead
- [ ] Console shows no errors
- [ ] `data-palette` attribute matches the default, not 'pink'

---

## Test 9: Browser Compatibility - localStorage Blocked

**Purpose:** Verify graceful handling when localStorage is unavailable.

### Steps:
1. Open browser in Private/Incognito mode (some browsers block localStorage)
2. OR: Disable localStorage via browser settings/extensions
3. Load page
4. Check Console for errors

### Expected Results:
- [ ] Page loads successfully with build-time default palette
- [ ] No JavaScript errors thrown
- [ ] Try-catch in FOUC script prevents exception
- [ ] Site remains functional

---

## Test 10: Page Load Performance

**Purpose:** Verify multiple palette CSS files don't significantly impact performance.

### Steps:
1. Configure 5+ palettes in selector options
2. Build site
3. Open DevTools → Network tab → Throttle to "Slow 3G"
4. Reload page
5. Check Lighthouse performance score

### Expected Results:
- [ ] All CSS files load in parallel (check Network waterfall)
- [ ] Total CSS load time reasonable (<2s on Slow 3G)
- [ ] No render-blocking detected
- [ ] First Contentful Paint < 3s
- [ ] Lighthouse performance score > 80

---

## Test 11: Cross-Browser Testing

**Purpose:** Verify functionality across major browsers.

### Browsers to Test:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (macOS)
- [ ] Edge

### For Each Browser:
1. Load page
2. Test localStorage persistence (set, reload, verify)
3. Test manual `data-palette` attribute changes
4. Verify no console errors
5. Check CSS custom properties work (colors update)

### Expected Results:
- [ ] All browsers: FOUC prevention works
- [ ] All browsers: localStorage persists
- [ ] All browsers: CSS scoping via `[data-palette]` works
- [ ] All browsers: No console errors

---

## Test 12: Visual Regression - All Palettes

**Purpose:** Verify all configured palettes render correctly.

### Steps:
For each configured palette:
1. Set via DevTools: `document.documentElement.setAttribute('data-palette', 'PALETTE_NAME')`
2. Visually inspect:
   - Page background color
   - Text color (body, headings)
   - Link color and hover states
   - Navigation elements
   - Code blocks
   - Footer

### Palettes to Test:
- [ ] default
- [ ] dark
- [ ] light (if exists)
- [ ] gruvbox_dark
- [ ] sans
- [ ] sans_dark
- [ ] pink
- [ ] blueberry
- [ ] lightyear
- [ ] red_drum

### Expected Results:
- [ ] All palettes apply their defined colors
- [ ] No elements remain unstyled
- [ ] Contrast is readable (WCAG AA informal check)
- [ ] No visual glitches or layout shifts

---

## Test 13: DevTools - Inspect Generated HTML

**Purpose:** Verify build-time template rendering is correct.

### Steps:
1. Open any built HTML file in browser
2. Open DevTools → Elements tab
3. Inspect `<html>` element
4. Inspect `<head>` section

### Expected Results:
- [ ] `<html>` has `lang="en"` attribute
- [ ] `<html>` has `data-palette="..."` attribute (matches mkdocs.yml default)
- [ ] `<html>` has `data-available-palettes="[...]"` attribute
- [ ] FOUC prevention `<script>` appears BEFORE first `<link rel="stylesheet">`
- [ ] All configured palette CSS files linked in `<head>`
- [ ] Comments present: "Palette selector enabled" or "disabled"
- [ ] Bundled palettes have comment: "Bundled palette: dark"
- [ ] Custom palettes have comment: "Custom palette: ocean"

---

## Test 14: Network Tab - CSS Load Order

**Purpose:** Verify CSS files load in optimal order.

### Steps:
1. Open page in browser
2. DevTools → Network tab
3. Filter by "CSS"
4. Reload page
5. Examine load order

### Expected Results:
- [ ] `terminal.css` loads first
- [ ] `theme.css` loads second
- [ ] Palette CSS files load after theme
- [ ] All palette CSS files load in parallel (waterfall shows overlap)
- [ ] No CSS files block initial render

---

## Test 15: Accessibility - Keyboard Navigation

**Purpose:** Verify palette switching doesn't break keyboard navigation.

### Steps:
1. Load page
2. Use Tab key to navigate through page
3. Change palette via: `document.documentElement.setAttribute('data-palette', 'dark')`
4. Continue tabbing

### Expected Results:
- [ ] Focus indicators visible before palette change
- [ ] Focus indicators visible after palette change
- [ ] Tab order unchanged by palette switch
- [ ] No focus trap created
- [ ] Focus ring color has sufficient contrast in all palettes

---

## Summary

**Tests Completed:** _____ / 15

**Issues Found:**
- 
- 
- 

**Notes:**
