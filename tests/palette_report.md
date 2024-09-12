## Steps
1. Identify the background and foreground colors based on simple keywords (ex: property name contains "background")
2. Check each background-foreground combo for WCAG alignment
3. Report results in an html table
## Notes
- ___keywords___: bg, background, fg, foreground, color, matplotlib color names
- Currently assumes all non-background colors are foreground colors for the test)
## Legend
- ✅: all WCAG tests passed
☑️: some WCAG tests passed
- ❌: no WCAG tests passed
- Symbols link to WCAG api response with tests
# blueberry.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>primary-color (000080)</th>
      <th>font-color (190910)</th>
      <th>secondary-color (3737aa)</th>
      <th>tertiary-color (3737aa)</th>
      <th>error-color (ffbf00)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>progress-bar-background (d4d4d4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=000080&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=3737aa&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=3737aa&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ffbf00&bcolor=d4d4d4&api'>:x:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (f7f7f7)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=000080&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=3737aa&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=3737aa&bcolor=f7f7f7&api'>:white_check_mark:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ffbf00&bcolor=f7f7f7&api'>:x:</a></td>
    </tr>
    <tr>
      <td>background-color (ffc)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=000080&bcolor=ffc&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=ffc&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=3737aa&bcolor=ffc&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=3737aa&bcolor=ffc&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ffbf00&bcolor=ffc&api'>:x:</a></td>
    </tr>
  </tbody>
</table>

# dark.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>primary-color (62c4ff)</th>
      <th>secondary-color (a3abba)</th>
      <th>tertiary-color (a3abba)</th>
      <th>font-color (e8e9ed)</th>
      <th>error-color (ff3c74)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>background-color (222225)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=62c4ff&bcolor=222225&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=222225&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=222225&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=e8e9ed&bcolor=222225&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ff3c74&bcolor=222225&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>progress-bar-background (3f3f44)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=62c4ff&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=e8e9ed&bcolor=3f3f44&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ff3c74&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (3f3f44)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=62c4ff&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=e8e9ed&bcolor=3f3f44&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ff3c74&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
    </tr>
  </tbody>
</table>

# gruvbox_dark.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>gb-dm-dark-blue (458588)</th>
      <th>gb-dm-dark-aqua (689d6a)</th>
      <th>gb-dm-light-blue (83a598)</th>
      <th>gb-dm-light-aqua (8ec07c)</th>
      <th>gb-dm-dark-gray (928374)</th>
      <th>gb-dm-dark-green (98971a)</th>
      <th>gb-dm-fg4 (a89984)</th>
      <th>gb-dm-light-gray (a89984)</th>
      <th>gb-dm-dark-purple (b16286)</th>
      <th>gb-dm-light-green (b8bb26)</th>
      <th>gb-dm-fg3 (bdae93)</th>
      <th>gb-dm-dark-red (cc241d)</th>
      <th>gb-dm-light-purple (d3869b)</th>
      <th>gb-dm-fg2 (d5c4a1)</th>
      <th>gb-dm-dark-orange (d65d0e)</th>
      <th>gb-dm-dark-yellow (d79921)</th>
      <th>gb-dm-fg1 (ebdbb2)</th>
      <th>gb-dm-light-orange (f38019)</th>
      <th>gb-dm-light-yellow (fabd2f)</th>
      <th>gb-dm-light-red (fb4934)</th>
      <th>gb-dm-fg0 (fbf1c7)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>gb-dm-bg0-hard (1d2021)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=1d2021&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=1d2021&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=1d2021&api'>:white_check_mark:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=1d2021&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=1d2021&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=1d2021&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=1d2021&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=1d2021&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=1d2021&api'>:white_check_mark:</a></td>
    </tr>
    <tr>
      <td>gb-dm-bg0 (282828)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=282828&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=282828&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=282828&api'>:white_check_mark:</a></td>
    </tr>
    <tr>
      <td>gb-dm-bg0-soft (32302f)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=32302f&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=32302f&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=32302f&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=32302f&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=32302f&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=32302f&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=32302f&api'>:white_check_mark:</a></td>
    </tr>
    <tr>
      <td>gb-dm-bg1 (3c3836)</td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=3c3836&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=3c3836&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=3c3836&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=3c3836&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=3c3836&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=3c3836&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=3c3836&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=3c3836&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=3c3836&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=3c3836&api'>:white_check_mark:</a></td>
    </tr>
    <tr>
      <td>gb-dm-bg2 (504945)</td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=504945&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=504945&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=504945&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=504945&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=504945&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=504945&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=504945&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=504945&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=504945&api'>:white_check_mark:</a></td>
    </tr>
    <tr>
      <td>gb-dm-bg3 (665c54)</td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=665c54&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=665c54&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=665c54&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=665c54&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=665c54&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=665c54&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=665c54&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=665c54&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=665c54&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=665c54&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=665c54&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=665c54&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=665c54&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>gb-dm-bg4 (7c6f64)</td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=458588&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=689d6a&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=83a598&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8ec07c&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=928374&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=98971a&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b16286&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=b8bb26&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=cc241d&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d3869b&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d5c4a1&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d65d0e&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d79921&bcolor=7c6f64&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=7c6f64&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f38019&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=7c6f64&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=7c6f64&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fbf1c7&bcolor=7c6f64&api'>:ballot_box_with_check:</a></td>
    </tr>
  </tbody>
</table>

# lightyear.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>font-color (190910)</th>
      <th>primary-color (4B0082)</th>
      <th>secondary-color (6e4e84)</th>
      <th>tertiary-color (6e4e84)</th>
      <th>error-color (db3030)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>background-color (E0FFE0)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=E0FFE0&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=4B0082&bcolor=E0FFE0&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=6e4e84&bcolor=E0FFE0&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=6e4e84&bcolor=E0FFE0&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=db3030&bcolor=E0FFE0&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>progress-bar-background (d4d4d4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=4B0082&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=6e4e84&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=6e4e84&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=db3030&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (f7f7f7)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=4B0082&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=6e4e84&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=6e4e84&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=db3030&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
    </tr>
  </tbody>
</table>

# pink.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>font-color (190910)</th>
      <th>secondary-color (715864)</th>
      <th>tertiary-color (715864)</th>
      <th>error-color (bb0047)</th>
      <th>primary-color (f90d7a)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>progress-bar-background (d4d4d4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=715864&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=715864&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bb0047&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f90d7a&bcolor=d4d4d4&api'>:x:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (f7f7f7)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=715864&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=715864&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bb0047&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f90d7a&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>background-color (ffffff)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=ffffff&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=715864&bcolor=ffffff&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=715864&bcolor=ffffff&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bb0047&bcolor=ffffff&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=f90d7a&bcolor=ffffff&api'>:ballot_box_with_check:</a></td>
    </tr>
  </tbody>
</table>

# red_drum.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>font-color (190910)</th>
      <th>primary-color (8B0000)</th>
      <th>secondary-color (976161)</th>
      <th>tertiary-color (976161)</th>
      <th>error-color (FFA07A)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>background-color (EEE8AA)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=EEE8AA&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8B0000&bcolor=EEE8AA&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=976161&bcolor=EEE8AA&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=976161&bcolor=EEE8AA&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=FFA07A&bcolor=EEE8AA&api'>:x:</a></td>
    </tr>
    <tr>
      <td>progress-bar-background (d4d4d4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8B0000&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=976161&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=976161&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=FFA07A&bcolor=d4d4d4&api'>:x:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (f7f7f7)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=8B0000&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=976161&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=976161&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=FFA07A&bcolor=f7f7f7&api'>:x:</a></td>
    </tr>
  </tbody>
</table>

# sans.css
- Style does not have enough foregrounds and bakcgrounds to compare.

# sans_dark.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>primary-color (62c4ff)</th>
      <th>secondary-color (a3abba)</th>
      <th>tertiary-color (a3abba)</th>
      <th>font-color (e8e9ed)</th>
      <th>error-color (ff3c74)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>background-color (222225)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=62c4ff&bcolor=222225&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=222225&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=222225&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=e8e9ed&bcolor=222225&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ff3c74&bcolor=222225&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>progress-bar-background (3f3f44)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=62c4ff&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=e8e9ed&bcolor=3f3f44&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ff3c74&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (3f3f44)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=62c4ff&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a3abba&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=e8e9ed&bcolor=3f3f44&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ff3c74&bcolor=3f3f44&api'>:ballot_box_with_check:</a></td>
    </tr>
  </tbody>
</table>

# soundside.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>primary-color (004D4D)</th>
      <th>font-color (190910)</th>
      <th>secondary-color (496262)</th>
      <th>tertiary-color (496262)</th>
      <th>error-color (ffb11f)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>progress-bar-background (d4d4d4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=004D4D&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=496262&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=496262&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ffb11f&bcolor=d4d4d4&api'>:x:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (f7f7f7)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=004D4D&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=f7f7f7&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=496262&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=496262&bcolor=f7f7f7&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ffb11f&bcolor=f7f7f7&api'>:x:</a></td>
    </tr>
    <tr>
      <td>background-color (ffe5b4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=004D4D&bcolor=ffe5b4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=ffe5b4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=496262&bcolor=ffe5b4&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=496262&bcolor=ffe5b4&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ffb11f&bcolor=ffe5b4&api'>:x:</a></td>
    </tr>
  </tbody>
</table>

# volans.css

<table>
  <thead>
    <tr>
      <th>backgrounds</th>
      <th>font-color (190910)</th>
      <th>primary-color (5C4033)</th>
      <th>secondary-color (A9A9A9)</th>
      <th>tertiary-color (A9A9A9)</th>
      <th>error-color (d64400)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>code-bg-color (A9A9A9)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=A9A9A9&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=5C4033&bcolor=A9A9A9&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=A9A9A9&bcolor=A9A9A9&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=A9A9A9&bcolor=A9A9A9&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d64400&bcolor=A9A9A9&api'>:x:</a></td>
    </tr>
    <tr>
      <td>background-color (F5F5DC)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=F5F5DC&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=5C4033&bcolor=F5F5DC&api'>:white_check_mark:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=A9A9A9&bcolor=F5F5DC&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=A9A9A9&bcolor=F5F5DC&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d64400&bcolor=F5F5DC&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>progress-bar-background (d4d4d4)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=190910&bcolor=d4d4d4&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=5C4033&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=A9A9A9&bcolor=d4d4d4&api'>:x:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=A9A9A9&bcolor=d4d4d4&api'>:x:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=d64400&bcolor=d4d4d4&api'>:ballot_box_with_check:</a></td>
    </tr>
  </tbody>
</table>
