# Contrast Report Generator Utility

## Overview

The `generate_contrast_report.py` utility automatically regenerates the `COLOR_CONTRAST_TESTS.md` documentation with current contrast ratio data extracted from the theme's CSS files.

## Location

- **Utility**: `tests/accessibility/generate_contrast_report.py`
- **Output**: `COLOR_CONTRAST_TESTS.md` (generated in project root)

## Usage

### Run from project root:

```bash
python tests/accessibility/generate_contrast_report.py
```

### What it does:

1. **Extracts CSS** from the theme's built site files
2. **Calculates contrast ratios** for each element type across all 6 default palettes:
   - Body text (paragraphs)
   - Links
   - Buttons
   - Input fields
3. **Generates markdown** with current WCAG AA compliance data
4. **Writes output** to `COLOR_CONTRAST_TESTS.md`

## Output Example

The generated report includes:

```markdown
## Body Text (`test_theme_body_text_contrast_meets_wcag_aa`)

- **Standard**: WCAG 2.1 AA - **4.5:1 minimum** for normal text
- **Elements tested**: `<body>`, `<p>`, `<h4>`, `<h5>`, `<h6>` and other text elements
- **Current palette colors** (all pass):
  - Default: #151515 on #fff = **18.3:1** ✅
  - Dark: #e8e9ed on #222225 = **15.3:1** ✅
  - ...
```

## When to Use

- **After color changes**: When the theme's color palette is updated, regenerate to ensure documentation is current
- **During development**: Verify that contrast improvements are reflected in the documentation
- **Before releases**: Ensure documentation matches actual theme colors

## Technical Details

### Data Sources

The utility extracts contrast ratios from:

1. **CSS Files**: `tests/examples/minimal/site/css/`
   - `terminal.css` (default colors)
   - `palettes/*.css` (palette-specific overrides)

2. **HTML Structure**: `tests/examples/minimal/site/index.html`
   - Actual elements in the test site
   - Theme-applied styles

### Functions

#### `get_contrast_ratios_for_palette(palette_name, site_path)`
- Extracts contrast ratios for a specific palette
- Returns dict with element type -> (foreground, background, ratio) mappings

#### `generate_scenario_section(scenario_type, element_type, min_ratio, palettes_ratios)`
- Generates markdown section for a test scenario
- Formats ratios and example failures

#### `main()`
- Orchestrates the generation process
- Handles file I/O

## Limitations

- Uses the static `minimal/site` which applies default colors
- For dynamic palette-specific sites, would need access to pytest-generated temp directories
- Color ratios shown are representative of the default palette structure

## Future Improvements

1. **Dynamic site building**: Could integrate with pytest fixtures to test actual built sites
2. **Per-palette site loading**: Load each palette's built site during test execution
3. **Scheduling**: Could be run automatically as part of CI/CD pipeline
4. **Comparison reports**: Track changes in contrast ratios over time

## Troubleshooting

### "tests/examples directory not found"
- Run from the project root: `cd /path/to/mkdocs-terminal`
- Ensure `tests/examples/minimal/site/` exists and is built

### No ratios extracted for a palette
- Check that the site files contain the required elements:
  - At least one `<p>` tag
  - At least one `<a>` tag  
  - At least one `<button>` tag
  - At least one `<input>` tag
- Verify CSS files are present in `site/css/`

### Generated markdown looks incomplete
- Check the utility output for warnings
- Verify all expected palettes are listed in `tests/interface/theme_features.py`
