# Terminal for MkDocs Theme Development
Use this readme to add a feature to this theme or to update the theme documentation.

## Quicklinks

- [Terminal for MkDocs Theme Development](#terminal-for-mkdocs-theme-development)
  - [Quicklinks](#quicklinks)
  - [Developer Setup](#developer-setup)
    - [Prerequisites](#prerequisites)
    - [Fork and Clone Repository](#fork-and-clone-repository)
    - [Confirm Setup](#confirm-setup)
  - [Palette Architecture Overview](#palette-architecture-overview)
  - [Documentation Updates](#documentation-updates)
    - [Create a Feature Branch](#create-a-feature-branch)
    - [Push Local Branch to Remote Repository](#push-local-branch-to-remote-repository)
    - [Start Local Documentation Server](#start-local-documentation-server)
    - [Make Documentation Updates](#make-documentation-updates)
    - [Push Changes and Create PR](#push-changes-and-create-pr)
  - [Theme Updates](#theme-updates)
    - [Create a Feature Branch](#create-a-feature-branch-1)
    - [Push Local Branch to Remote Repository](#push-local-branch-to-remote-repository-1)
    - [Bump Theme Version](#bump-theme-version)
    - [Start Documentation Server with Local Theme](#start-documentation-server-with-local-theme)
    - [Make Updates](#make-updates)
    - [Test Theme Build/Packaging Locally](#test-theme-buildpackaging-locally)
    - [Add Functional Tests](#add-functional-tests)
    - [Push Changes and Create PR](#push-changes-and-create-pr-1)
    - [Review PR Build](#review-pr-build)


## Developer Setup
Development for this project is done within [Docker containers].  Using Docker containers makes setup easy because all developer workspaces will have the same installed software / OS.  If there's a tool that is not available that you think would be helpful to add to the default container image, please feel free to [open an Issue](https://github.com/ntno/mkdocs-terminal/issues/new/choose) and start a discussion.  

*Note*: All software besides the two prerequisites will be installed in the Docker container and not your machine.

[Docker containers]: https://www.docker.com/resources/what-container/

### Prerequisites
- install [docker](https://docs.docker.com/get-docker/)
- install [Make](https://www.gnu.org/software/make/)

### Fork and Clone Repository
- [Fork mkdocs-terminal](https://github.com/ntno/mkdocs-terminal/fork)  
- Clone your fork: `git clone git@github.com:YOUR_GIT_USERNAME/mkdocs-terminal.git`

### Confirm Setup
Test your system's docker setup by running the documentation site server locally:

```bash
cd mkdocs-terminal  
make serve-docs
```

You should be able to visit [http://0.0.0.0:8080/mkdocs-terminal/](http://0.0.0.0:8080/mkdocs-terminal/) in your browser and view the mkdocs-terminal documentation site.  

If you get a `docker.sock: connect: permission denied` error, you probably need to start the Docker engine on your machine.  

**Example Error**:
```log
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json?all=1&filters=%7B%22label%22%3A%7B%22com.docker.compose.project%3Dmkdocs-terminal%22%3Atrue%7D%7D&limit=0": dial unix /var/run/docker.sock: connect: permission denied
make: *** [ubuntu] Error 1
```

**Solution**:
Open the Docker Desktop application and wait until the application indicates that the Docker engine is in a "running" state.  Then retry starting your docker container.  

<img src="documentation/docs/img/developer-setup/engine-starting.png" width="600" title="Docker Engine Starting" alt="orange starting indicator at bottom left of Docker Desktop">

<img src="documentation/docs/img/developer-setup/engine-running.png" width="600" title="Docker Engine Starting" alt="green running indicator at bottom left of Docker Desktop">

## Palette Architecture Overview

The theme uses a **data-attribute scoping** architecture for runtime palette switching in static sites.

### How It Works

**Build Time:**
1. All configured palette CSS files are linked in `<head>`
2. Default palette set via `<html data-palette="dark">` attribute
3. Available palettes embedded in `data-available-palettes` attribute

**Runtime:**
1. User changes palette via selector UI
2. JavaScript updates `data-palette` attribute value
3. CSS cascade instantly switches colors (no file loading needed)

### CSS Architecture

Palettes use attribute selector scoping for multi-palette support:

```css
/* Color constants in :root (no conflicts between palettes) */
:root {
  --dark-bg: #222225;
  --dark-fg: #e8e9ed;
}

/* Variable mappings in [data-palette] (higher specificity) */
[data-palette="dark"] {
  --mkdocs-terminal-bg-color: var(--dark-bg);
  --mkdocs-terminal-font-color: var(--dark-fg);
  
  /* Legacy aliases for backwards compatibility */
  --background-color: var(--mkdocs-terminal-bg-color);
  --font-color: var(--mkdocs-terminal-font-color);
}
```

**Key Points:**

- **`:root` blocks:** Color constants only (prevents conflicts when multiple palettes load)
- **`[data-palette]` blocks:** Variable mappings (only applies when attribute matches)
- **Specificity:** `[data-palette]` (0,1,0) beats `:root` (0,0,1)
- **Compatibility layer:** `theme.css` maps legacy variables to namespaced ones with fallbacks

### CSS Cascade Order

```
terminal.css → theme.css → palettes/*.css → consuming code
```

1. **terminal.css** — Legacy glue variables only
2. **theme.css** — Compatibility layer with fallbacks  
3. **palettes/\*.css** — Color constants + scoped mappings
4. **Consuming code** — Uses variables from the cascade

### For Theme Developers

**Adding a new palette:**
- Use `openspec/changes/color-palette-toggle/specs/custom-palette-template.css` as a template
- Define color constants in `:root`
- Define variable mappings in `[data-palette="your-name"]`
- Test with `load_palette_context("your-name")` (see CSS Parser Utilities)

**Testing palettes:**
- See [CSS Parser Utilities](#css-parser-utilities-testing) section below
- Use `load_palette_context(name)` to simulate full cascade
- All color combinations must meet WCAG AA contrast requirements

**Migration guide:**
- Existing custom palettes in `extra_css` continue working
- New palettes should use `[data-palette]` architecture
- See `openspec/changes/color-palette-toggle/design.md` for details

## Documentation Updates

### Create a Feature Branch
Create a local branch to track your updates.  Include the topic of the feature in your branch name.  Example:  

```bash
git checkout -b docs-add-css-override-instructions
```

### Push Local Branch to Remote Repository
```bash
git push --set-upstream origin docs-add-css-override-instructions
```

### Start Local Documentation Server
```bash
make serve-docs
```

### Make Documentation Updates
- Update existing [documentation pages](documentation/docs)  
- Add any new pages to the documentation site nav in [documentation/mkdocs.yml](documentation/mkdocs.yml)  
- View changes in local server and confirm everything works as expected 
  - confirm images load
  - confirm links are not broken

### Push Changes and Create PR
See [Work On Pull Request](https://github.com/susam/gitpr#work-on-pull-request) for help on adding/pushing changes to your feature branch.  

See [Pull Requests](CONTRIBUTING.md#pull-requests) for instructions on creating a pull request to this repository.


## Theme Updates

### Create a Feature Branch
Create a local branch to track your updates.  Include the topic of the feature in your branch name.  Example:  

```bash
git checkout -b add-timeline-component
```

### Push Local Branch to Remote Repository
```bash
git push --set-upstream origin add-timeline-component
```

### Bump Theme Version
update version in:
- [`package.json`](package.json#L3)
- [`terminal/theme_version.html`](terminal/theme_version.html)

### Start Documentation Server with Local Theme
```bash
make serve-local-theme
```

### Make Updates
Update files in [terminal/](terminal/).  You should see changes loaded in [http://0.0.0.0:8080/mkdocs-terminal/](http://0.0.0.0:8080/mkdocs-terminal/).

- View changes in local server and confirm everything works as expected 
  - confirm images load
  - confirm links are not broken
  - confirm existing components/features still work

### Test Theme Build/Packaging Locally
Launch the project's ubuntu container and run tox build tests:

```bash
make ubuntu
make tox
```

### Add Functional Tests
If you are adding/changing theme functionality, please add a test to the relevant test class in [tests/](tests/).  You can run the test suite locally by using the commands described in this section.  

After you have installed the required testing software you can rerun `make quick-tests` whenever you want to re-execute.

```bash
make ubuntu
make install-test-prereqs
make install-test-requirements
make quick-tests
```

Remember to work in the project's [Docker container](#developer-setup) to avoid Python dependency conflicts.  Once you have run `make ubuntu`, your terminal prompt should include `root@CONTAINER_ID`:

![Docker Container](documentation/docs/img/developer-setup/developer-container.png)


Test suites can always be improved!  Please consider making a contribution or starting a discussion if you have any ideas.  

### Push Changes and Create PR
See [Work On Pull Request](https://github.com/susam/gitpr#work-on-pull-request) for help on adding/pushing changes to your feature branch.  

### Review PR Build

Pull Requests are tested using a [GitHub Action workflow](https://github.com/ntno/mkdocs-terminal/actions/workflows/test.yml).  Check the status of your PR build and resolve any reported issues.

## Plugin Architecture

The Terminal theme includes MkDocs plugins that extend build-time functionality. Plugins follow standard MkDocs plugin patterns similar to mkdocs-material.

### Palette Plugin

The `terminal/palette` plugin processes palette configuration during the MkDocs build process.

**Location:** `terminal/plugins/palette/`

**Files:**
- `config.py` — Configuration parsing and validation logic
- `plugin.py` — MkDocs plugin implementation

**Architecture:**

The plugin follows the standard MkDocs `BasePlugin` pattern:

```python
from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config
from mkdocs.config.config_options import Type

class PalettePlugin(BasePlugin):
    def on_config(self, config, **kwargs):
        """Process palette configuration during build."""
        # Parse theme.palette from mkdocs.yml
        # Validate bundled and custom palette options
        # Store normalized configuration
        
    def on_env(self, env, config, files, **kwargs):
        """Expose configuration to Jinja2 templates."""
        # Add palette_config to env.globals
        # Templates can access via {{ palette_config }}
```

**Configuration Schema:**

Uses MkDocs `Config` classes for type-safe configuration:

```python
from mkdocs.config.base import Config
from mkdocs.config.config_options import Type, Optional

class PaletteOption(Config):
    """Single palette option (bundled or custom)."""
    name = Type(str)
    css = Optional(Type(str))

class SelectorConfig(Config):
    """Palette selector UI configuration."""
    enabled = Type(bool, default=False)
    ui = Type(str, default="auto")
    options = ListOfItems(SubConfig(PaletteOption), default=[])
```

**Build-Time Processing:**

1. **Parse** `theme.palette` from `mkdocs.yml`
   - Supports legacy string format: `palette: "dark"`
   - Supports new object format with selector configuration
   - Normalizes both formats to consistent internal structure

2. **Validate** palette options
   - Bundled palettes verified against `terminal/css/palettes/*.css`
   - Custom palettes verified against `extra_css` list
   - Invalid options filtered with build warnings
   - Selector UI constraints enforced (toggle requires 2 options)

3. **Expose** to templates
   - Normalized configuration added to Jinja2 `env.globals`
   - Templates access via `{{ palette_config }}`
   - Available fields: `default`, `selector_enabled`, `selector_ui`, `valid_options`

**Legacy Format Normalization:**

The plugin maintains backwards compatibility with the simple string format:

```yaml
# Legacy format
theme:
  palette: "dark"

# Normalized internally to:
{
  "default": "dark",
  "selector_enabled": false,
  "selector_ui": "auto",
  "options": [],
  "valid_options": []
}
```

**Testing:**

Comprehensive test coverage in `tests/plugins/palette/`:

- `test_palette.py` — Configuration parsing and validation
- `test_palette_plugin.py` — Plugin lifecycle integration

Run tests:
```bash
pytest tests/plugins/ -v
```

**Registration:**

Plugins are registered via setuptools entry points in `pyproject.toml`:

```toml
[project.entry-points."mkdocs.plugins"]
"terminal/palette" = "terminal.plugins.palette.plugin:PalettePlugin"
```

Users activate by adding to their `mkdocs.yml`:

```yaml
plugins:
  - palette
```

**Key Design Decisions:**

- **Build-time validation only**: Static sites have no runtime server, so all validation must occur during `mkdocs build`
- **CSS pre-linking**: All palette CSS files linked in `<head>` at build time (cannot lazy-load)
- **Data attribute scoping**: Palette switching works via CSS `[data-palette="name"]` selectors
- **Template globals**: Configuration exposed via Jinja2 globals for flexible template access

## CSS Parser Utilities (Testing)

The theme uses a custom CSS parsing system to test palette variables and simulate browser CSS cascade behavior. This is necessary because palettes use the `[data-palette="name"]` attribute selector architecture for runtime switching.

**Location:** `tests/accessibility/utilities/css_parser.py`

### Key Functions

**`load_palette_context(palette_name: str)`** — Full cascade simulation

Use this to test how a palette appears in the browser. Automatically loads all three CSS files and resolves variables through the complete cascade.

```python
from tests.accessibility.utilities import load_palette_context

# Test the "dark" palette as it appears in browser
context = load_palette_context("dark")
assert context["font-color"] == "#e8e9ed"
assert context["background-color"] == "#222225"
```

**CSS cascade order:**
1. `terminal.css` :root (legacy glue variables)
2. `theme.css` :root (compatibility layer with fallbacks)
3. `palette.css` :root (color constants)
4. `palette.css` [data-palette] (variable mappings — highest specificity)

**`parse_data_palette_variables(css_text: str, palette_name: str)`** — Extract from attribute selectors

Parses variables from `[data-palette="name"]` blocks. Used internally by `load_palette_context()`.

```python
from tests.accessibility.utilities import parse_data_palette_variables

css = '''
[data-palette="dark"] {
  --mkdocs-terminal-font-color: #e8e9ed;
  --font-color: var(--mkdocs-terminal-font-color);
}
'''
vars = parse_data_palette_variables(css, "dark")
# Returns: {'--mkdocs-terminal-font-color': '#e8e9ed', '--font-color': 'var(...)'}
```

**`resolve_css_variable(value: str, css_variables: dict)`** — Resolve `var()` references

Handles nested variable references and CSS fallback syntax `var(--name, fallback)`.

```python
from tests.accessibility.utilities import resolve_css_variable

variables = {
    '--mkdocs-terminal-font-size': '15px',
    '--global-font-size': 'var(--mkdocs-terminal-font-size, 14px)'
}

# Resolves through chain
resolved = resolve_css_variable('var(--global-font-size)', variables)
# Returns: '15px'

# Uses fallback when variable missing
resolved = resolve_css_variable('var(--missing, 12px)', variables)
# Returns: '12px'
```

### When to Use Which Function

| Scenario | Function | Why |
|----------|----------|-----|
| Testing a complete palette | `load_palette_context("dark")` | Simulates full browser cascade, easiest to use |
| Testing CSS snippets | `extract_css_attributes_from_palette(css, data_palette="dark")` | More control, manual CSS loading |
| Parsing attribute selectors | `parse_data_palette_variables(css, "dark")` | Low-level, used internally |
| Resolving variables | `resolve_css_variable(value, vars)` | Low-level, used internally |

### Testing Custom Palettes

To test a custom palette that uses the `[data-palette]` architecture:

```python
# Option 1: If the palette file exists in terminal/css/palettes/
context = load_palette_context("my-custom-palette")

# Option 2: Test CSS strings directly
from tests.accessibility.utilities import extract_css_attributes_from_palette

with open("my-custom-palette.css") as f:
    palette_css = f.read()

attrs = extract_css_attributes_from_palette(
    css_content=palette_css,
    data_palette="my-custom-palette"
)
```

### Backwards Compatibility

The parser supports both old-style (variables in `:root`) and new-style (variables in `[data-palette]`) palettes:

- **Old style:** `extract_css_attributes(css_content)` — parses `:root` only
- **New style:** `load_palette_context(name)` — parses full cascade with `[data-palette]`

Existing tests using `extract_css_attributes()` continue to work for legacy palettes that define variables directly in `:root` blocks.

### Architecture Notes

**Why not use a CSS parser library?**

We need to simulate browser-specific CSS cascade behavior including:
- CSS specificity rules (`:root` vs `[data-palette]`)
- Load order precedence (terminal → theme → palette)
- Variable fallback syntax `var(--name, fallback)`

Standard CSS parsers don't simulate this cascade behavior, so we built lightweight utilities tailored to our architecture.

**How does this relate to the palette selector feature?**

The palette selector enables runtime switching by:
1. Loading ALL palette CSS files at build time
2. Using `[data-palette="name"]` selectors to scope variables
3. Changing the `<html data-palette>` attribute value with JavaScript

The CSS parser utilities test that this architecture works correctly by simulating the browser's variable resolution when a specific `data-palette` is active.
