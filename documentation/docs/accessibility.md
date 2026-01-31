# Accessibility

The [dark], [sans_dark], [blueberry], [lightyear], and [red_drum] color palettes meet WCAG 2.1 AA color contrast standards.  

The [default], [sans], [pink], and [gruvbox_dark] color palettes currently have the contrast issues noted below.  These palettes will be updated in the next major release and their current settings moved to a legacy version.

[default]: ../configuration/palettes/default/
[sans]: ../configuration/palettes/sans/
[pink]: ../configuration/palettes/pink/
[gruvbox_dark]: ../configuration/palettes/gruvbox-dark/
[dark]: ../configuration/palettes/dark/
[sans_dark]: ../configuration/palettes/sans-dark/
[blueberry]: ../configuration/palettes/blueberry/
[lightyear]: ../configuration/palettes/lightyear/
[red_drum]: ../configuration/palettes/red_drum/

## Known Issues

### Color Contrast

| Palette        | Primary Links | Buttons | Code Blocks |
| -------------- | ------------- | ------- | ----------- |
| [default]      | x             | x       |             |
| [sans]         | x             | x       |             |
| [pink]         | x             | x       |             |
| [gruvbox_dark] |               | x       |             |
| [dark]         |               |         |             |
| [sans_dark]    |               |         |             |
| [blueberry]    |               |         |             |
| [lightyear]    |               |         |             |
| [red_drum]     |               |         |             |

'x' indicates an open WCAG 2.1 AA contrast failure detected by the [test_color_contrast.py] integration test.

See [Color Contrast Failures](#color-contrast-failures) for the measured ratios and affected components.

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
