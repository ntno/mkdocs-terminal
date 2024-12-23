## Steps
1. Identify the background and foreground colors based on simple keywords (ex: property name contains "background")
2. Check each background-foreground combo for WCAG alignment
3. Report results in an html table
## Notes
- ___keywords___: bg, background, fg, foreground, color, matplotlib color names
- Currently assumes all non-background colors are foreground colors for the test)
## Legend
- ✅: all WCAG tests passed
- ☑️: some WCAG tests passed
- ❌: no WCAG tests passed
- Symbols link to WCAG api response with tests
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
      <th>tertiary-color (a89984)</th>
      <th>secondary-color (bdae93)</th>
      <th>font-color (ebdbb2)</th>
      <th>primary-color (fabd2f)</th>
      <th>error-color (fb4934)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>background-color (282828)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=282828&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=282828&api'>:white_check_mark:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=282828&api'>:ballot_box_with_check:</a></td>
    </tr>
    <tr>
      <td>progress-bar-background (504945)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=504945&api'>:x:</a></td>
    </tr>
    <tr>
      <td>code-bg-color (504945)</td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=a89984&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=bdae93&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=ebdbb2&bcolor=504945&api'>:ballot_box_with_check:</a></td>
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fabd2f&bcolor=504945&api'>:ballot_box_with_check:</a></td><
      <td><a href='https://webaim.org/resources/contrastchecker/?fcolor=fb4934&bcolor=504945&api'>:x:</a></td>
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
