# Accessibility

## Known Issues

### Color Contrast

| Palette      | Primary Links | Buttons | Code Blocks |
| ------------ | ------------- | ------- | ----------- |
| [default](../configuration/palettes/default/) | x | x |  |
| [sans](../configuration/palettes/sans/) | x | x |  |
| [pink](../configuration/palettes/pink/) | x | x |  |
| [gruvbox_dark](../configuration/palettes/gruvbox-dark/) |  | x |  |
| [dark](../configuration/palettes/dark/) |  |  |  |
| [sans_dark](../configuration/palettes/sans-dark/) |  |  |  |

'x' indicates an open WCAG 2.1 AA contrast failure detected by the [test_color_contrast.py] integration test.  

See [Color Contrast Failures](#color-contrast-failures) for the measured ratios and affected components.

Future releases of the Terminal for MkDocs theme will include palettes which meet WCAG 2.1 AA contrast standards.  To track progress, see issue [#119](https://github.com/ntno/mkdocs-terminal/issues/119).


[test_color_contrast.py]: https://github.com/ntno/mkdocs-terminal/blob/main/tests/accessibility/test_color_contrast.py

#### Color Contrast Failures

Ratios and RGB hex pairs come from the January 25 2026 run of [tests/accessibility/test_color_contrast.py](../tests/accessibility/test_color_contrast.py).

Expected contrast for all combinations is `4.5 : 1`

##### default
- Primary links (#1a95e0 on #ffffff) measure `3.27 : 1` 
- Primary buttons (#ffffff text on #1a95e0 background) also measure `3.27 : 1` 

##### dark
- No open contrast failures as of January 25 2026.

##### gruvbox_dark
- Alert message accents (#fb4934 on #282828) measure `4.29 : 1`
- Ghost error buttons (#fb4934 text on #282828 background) also measure `4.29 : 1` 

##### pink
- Primary links (#f90d7a on #ffffff) measure `3.91 : 1` 
- Primary buttons (#f7f7f7 on #f90d7a) measure `3.65 : 1` 

##### sans
- Primary links (#1a95e0 on #ffffff) measure `3.27 : 1 `
- Primary buttons (#ffffff on #1a95e0) measure `3.27 : 1` 

##### sans_dark
- No open contrast failures as of January 25 2026.

## Report An Issue

To report an issue, please create a new issue in the GitHub repository: [mkdocs-terminal > Create new issue](https://github.com/ntno/mkdocs-terminal/issues/new/choose)