# Accessibility

## Known Issues

### Color Contrast

| Palette      | Primary Links | Buttons | Code Blocks |
| ------------ | ------------- | ------- | ----------- |
| [default](../configuration/palettes/default/) | x | x |  |
| [sans](../configuration/palettes/sans/) | x | x |  |
| [pink](../configuration/palettes/pink/) | x | x |  |
| [gruvbox_dark](../configuration/palettes/gruvbox-dark/) |  | x | x |
| [dark](../configuration/palettes/dark/) |  |  | x |
| [sans_dark](../configuration/palettes/sans-dark/) |  |  | x |

x indicates an open WCAG 2.1 AA contrast failure detected by [tests/accessibility/test_color_contrast.py](../tests/accessibility/test_color_contrast.py). Button cells display one x per failing variant (default, primary, error, or ghost). See [Color Contrast Failures](#color-contrast-failures) for the measured ratios and affected components.

Future releases of the Terminal for MkDocs theme will include palettes which meet WCAG 2.1 AA contrast standards.  To track progress, see issue [#119](https://github.com/ntno/mkdocs-terminal/issues/119).

#### Color Contrast Failures

Palettes are listed alphabetically. Ratios and RGB hex pairs come from the January 25 2026 run of [tests/accessibility/test_color_contrast.py](../tests/accessibility/test_color_contrast.py).

##### default
- Primary links (#1a95e0 on #ffffff) measure 3.27 : 1 against the required 4.5 : 1.
- Primary buttons (#ffffff text on #1a95e0 background) also measure 3.27 : 1 (< 4.5 : 1).

##### dark
- Code blocks render #151515 text on #3f3f44 and only reach 1.74 : 1 (needs 4.5 : 1).

##### gruvbox_dark
- Alert/error message accents (#fb4934 on #282828) measure 4.29 : 1, just shy of 4.5 : 1.
- Ghost error buttons (#fb4934 text on #282828 background) also measure 4.29 : 1 (< 4.5 : 1).
- Code blocks use #151515 on #504945 and measure 2.07 : 1 (needs 4.5 : 1).

##### pink
- Primary links (#f90d7a on #ffffff) measure 3.91 : 1 (< 4.5 : 1).
- Primary buttons (#f7f7f7 on #f90d7a) measure 3.65 : 1 (< 4.5 : 1).

##### sans
- Primary links (#1a95e0 on #ffffff) measure 3.27 : 1 (< 4.5 : 1).
- Primary buttons (#ffffff on #1a95e0) measure 3.27 : 1 (< 4.5 : 1).

##### sans_dark
- Code blocks use #151515 on #3f3f44, yielding 1.74 : 1 instead of 4.5 : 1.

## Report An Issue

To report an issue, please create a new issue in the GitHub repository: [mkdocs-terminal > Create new issue](https://github.com/ntno/mkdocs-terminal/issues/new/choose)