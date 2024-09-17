import cssutils
import logging
from matplotlib import colors
import os
from pathlib import Path
from requests import get, exceptions

cssutils.log.setLevel(logging.ERROR)
palette_dir = Path(os.getcwd()) / "terminal/css/palettes"
palettes = [p for p in palette_dir.glob(pattern="*.css") if "default" not in p.name]
color_labels = colors.cnames.keys()
bg_labels = ["background", "bg"]
fg_labels = ["foreground", "fg"]
drop_labels = ["var(", "invert"]
palettes.sort()

intro = ('## Steps\n'
         '1. Identify the background and foreground colors '
         'based on simple keywords (ex: property name contains "background")\n'
         '2. Check each background-foreground combo for WCAG alignment\n'
         '3. Report results in an html table\n'
         '## Notes\n'
         '- ___keywords___: bg, background, fg, foreground, color, matplotlib '
         'color names\n'
         '- Currently assumes all non-background colors are foreground colors for the test)\n')
legend = ("## Legend\n"
          "- ✅: all WCAG tests passed\n"
          "- ☑️: some WCAG tests passed\n"
          "- ❌: no WCAG tests passed\n"
          "- Symbols link to WCAG api response with tests")

with open(Path(os.getcwd()) / "tests" / "palette_report.md", "w") as f:
    f.write(intro)
    f.write(legend)
for p in palettes:
    backgrounds = {}
    foregrounds = {}
    sheet = cssutils.parseFile(p)
    for rule in sheet:
        if isinstance(rule, cssutils.css.csscomment.CSSComment):
            continue
        style_text = rule.style.cssText.replace("\n", "")
        for i in style_text.split(";"):
            pair = i.split(": ")
            label = pair[0].replace("--", "")
            value = pair[1].replace("#", "")
            if "invert" in label or "var(" in value:
                pass
            else:
                if value == "fff":
                    value = "ffffff"
                if any(x in label for x in bg_labels):
                    backgrounds[label] = value
                else:
                    if any(x in label for x in fg_labels):
                        foregrounds[label] = value
                    elif any(x in label.replace("-", "") for x in list(color_labels)):   
                        foregrounds[label] = value
                    elif "color" in label:
                        foregrounds[label] = value
    if len(backgrounds.keys()) < 1 or len(foregrounds.keys()) < 1:
        with open(Path(os.getcwd()) / "tests" / "palette_report.md", "a+") as f:
            f.write(f"\n# {p.name}")
            f.write("\n- Style does not have enough foregrounds and bakcgrounds to compare.\n")
    else:
        backgrounds = {k: v for k, v in sorted(backgrounds.items(), key=lambda item: item[1])}
        foregrounds = {k: v for k, v in sorted(foregrounds.items(), key=lambda item: item[1])}
        table_start = "\n<table>\n  <thead>\n    <tr>"
        headers = "\n      <th>backgrounds</th>"
        table_middle = "\n  <tbody>"
        table_end = "\n  </tbody>\n</table>"
        for k, v in foregrounds.items():
            headers += f"\n      <th>{k} ({v})</th>"
        for k, v in backgrounds.items():
            row = f"\n    <tr>\n      <td>{k} ({v})</td>"
            for x, y in foregrounds.items():
                try:
                    url = f"https://webaim.org/resources/contrastchecker/?fcolor={y}&bcolor={v}&api"
                    resp = get(url)
                    grades = resp.json()
                    del grades["ratio"]
                    if all(grade == "pass" for grade in grades.values()):
                        row += f"\n      <td><a href='{url}'>:white_check_mark:</a></td>"
                    elif any(grade == "pass" for grade in grades.values()):
                        row += f"\n      <td><a href='{url}'>:ballot_box_with_check:</a></td>"
                    else:
                        row += f"<\n      <td><a href='{url}'>:x:</a></td>"
                except (ConnectionError, ConnectionRefusedError, ConnectionRefusedError):
                    row += f"<\n      <td><a href='{url}'>:no_entry:</a></td>"
            row += "\n    </tr>"
            table_middle += row
        headers += "\n    </tr>\n  </thead>"
        page = table_start + headers + table_middle + table_end
        with open(Path(os.getcwd()) / "tests" / "palette_report.md", "a+") as f:
            f.write(f"\n# {p.name}\n")
            f.write(f"{page}\n")
