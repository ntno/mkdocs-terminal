# Link Contrast Testing - Comprehensive Analysis

## Overview

The Terminal theme uses multiple link color variants depending on context:
- **Primary color links** (side navigation, inline content): `--primary-color` on `--background-color`
- **Font color links** (inverted sections, footer): `--font-color` on `--background-color`
- **Inverted color links** (banners, headers): `--invert-font-color` on inverted background

Each variant must meet WCAG 2.1 AA contrast requirements (4.5:1 minimum for text).

## New Test Approach

The test suite has been reorganized to perform comprehensive analysis of all actual elements rendered in the built site, rather than testing only a single representative color per palette.

### `test_all_link_color_combinations_meet_wcag_aa`

This test:
1. Builds a temporary site for each palette
2. Parses all HTML files in the built site
3. Finds all `<a>` (link) elements
4. Extracts the computed foreground color for each link
5. Determines the effective background color (from link element, parent elements, or body)
6. Groups links by unique `(foreground, background)` color combinations
7. Calculates contrast ratio for each unique combination
8. Validates that each ratio meets the 4.5:1 WCAG AA minimum

**Reports:**
- Each unique link color combination found
- Number of links using that combination
- Calculated contrast ratio
- Exact locations (file and link text) of examples

**Example output:**
```
Link color #1a95e0 on #fff = 4.32:1 (need 4.5:1) - Found 45 times
Link color #151515 on #fff = 18.26:1 ✅ (need 4.5:1) - Found 7 times
```

### `test_all_text_element_colors_meet_wcag_aa`

This test:
1. Builds a temporary site for each palette
2. Parses all HTML files
3. Finds all text elements (`p`, `span`, `h1-h6`, `li`, `blockquote`, `td`, `th`)
4. Extracts computed foreground color for each element
5. Determines effective background color (element, parent, or body)
6. Groups by unique color combinations
7. Validates contrast ratio meets 4.5:1 minimum
8. Reports element types and locations using each color combination

**Reports:**
- Color combination with count and element types
- Which elements use the combination
- Specific locations and element tags

**Example output:**
```
Text color #151515 on #fff = 18.26:1 ✅ - Elements: h1, h2, p, span - Found 156 times
Text color #e8e9ed on #222225 = 13.13:1 ✅ - Elements: p, span - Found 34 times
```

## Why This Approach?

Previous testing approach only checked:
- The first link found in a site
- Assumed all links used the same color
- Missed secondary color variants

New approach:
- **Complete coverage**: Tests every link and text element in the rendered site
- **Variant detection**: Automatically discovers all link color variants
- **Actionable reporting**: Groups by color combination, not by palette
- **Real rendering**: Uses actual built HTML/CSS, not assumptions
- **Failure details**: Shows exactly where failures occur

## Example: Identifying Problematic Link Colors

If a palette uses `--primary-color: #6666ff` on a white background:
- Contrast ratio = 3.2:1 (below 4.5:1 minimum) ❌
- Old test: Would silently pass (only checked one link)
- New test: Reports all 45 instances of `#6666ff on #fff`, clearly showing the failure

## WCAG Reference

- [WCAG 2.1 Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum)
- Minimum for text/links: 4.5:1
- Minimum for UI components: 3:1
