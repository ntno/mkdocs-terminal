# Project Context

## Purpose
Terminal for MkDocs is a third-party MkDocs theme and lightweight plugin suite that brings the
Terminal.css visual style to MkDocs documentation sites. The project provides a monospace,
terminal-inspired theme with additional features such as a built-in search modal, configurable
color palettes, revision date display, per-page or site-wide component hiding, a flexible image
grid, and utilities for converting select Markdown fragments to HTML during site build.

## Project Metadata
- **Name**: mkdocs-terminal
- **Repository**: https://github.com/ntno/mkdocs-terminal
- **Documentation**: https://ntno.github.io/mkdocs-terminal
- **License**: MIT

## Tech Stack
- **Language**: Python (>=3.7)
- **Primary framework**: MkDocs (theme + plugin entry points)
- **Templating**: Jinja2 (MkDocs theme templates)
- **Styling**: CSS (Terminal.css) and theme-specific CSS under `terminal/css`
- **JavaScript**: lightweight client-side enhancements (bundled under `terminal/js`)
- **Packaging / Build**: Hatch / hatchling, `python -m build`, `twine` for distribution
- **Version metadata**: NodeJS-based version source via `tool.hatch.version` (hatch-nodejs)
- **Testing**: pytest (unit/integration tests), tox to orchestrate testenvs
- **Linting**: flake8 (configured in `tox.ini`)
- **CI/CD**: GitHub Actions (matrix testing, pages deploy, publish workflow)

## Project Conventions

### Code Style
- Follow standard Python conventions (PEP 8) where practical.
- Linting is enforced with `flake8`; current config ignores line-length checks for the theme (`E501` ignored in `tox.ini`).
- Keep Jinja templates readable and minimize complex logic in templates — prefer helper filters/plugins for logic.

### Architecture Patterns
- The project is primarily a MkDocs theme with optional plugin entry points. Keep theme static assets in `terminal/` and
	theme templates under `terminal/partials` and `terminal/macros` as appropriate.
- Plugin code (Markdown filters) lives under `terminal/plugins` and should be small, well-tested, and isolated from theme-only code.
- Prefer composition over inheritance for utility functions; expose a minimal stable API for plugin hooks.

### Testing Strategy
- Unit and integration tests are written with `pytest` and located in `tests/`.
- `tox` manages environments: `py` env validates package build/checks; `pytest-linux` and `pytest-darwin` run platform-specific tests.
- CI runs a matrix across Python versions (`3.8`–`3.12`) and OS platforms (ubuntu, macOS, windows) via GitHub Actions.
- Before opening a PR, run: `make install-test-requirements && pytest` or `python -m tox -e pytest-linux` locally.

### Git Workflow
- Use feature branches named `feature/<short-description>` or `fix/<short-description>`.
- Open a Pull Request against `main` (or the repository's default branch). Ensure CI passes before merging.
- Follow repository PR template and use draft PRs for early feedback.
- Releases follow semantic versioning (MAJOR.MINOR.PATCH); see `documentation/docs/releases.md` for details.

### Dependency & Packaging
- Define runtime and build dependencies in `pyproject.toml`; do not add `setup.py` or `setup.cfg` files.
- Packaging is done with `hatch`/`hatchling` and `python -m build`; ensure static assets are included (see `tool.hatch.build.targets`).

### Developer Environment
- Development is container-first: prefer the Docker-based workflow described in `DEVELOPER_README.md` and use `Makefile` targets
	(`make ubuntu`, `make serve-docs`, `make serve-local-theme`) to run builds and local servers.
- Use `make install-test-prereqs` and `make install-test-requirements` to prepare CI-like environments locally when needed.

### Comments and Documentation
- Write concise, informative comments focused on intent and decisions; avoid noisy or redundant comments.
- Update the `documentation/docs/` site for any user-facing behavior changes and add docs for new theme components.

### Security and Sensitive Data
- Never hardcode secrets or credentials; do not commit sensitive data to the repository.
- Do not log sensitive data in tests or runtime.

### Testing & CI Expectations
- Add unit or integration tests for any new or changed functionality and include them under `tests/`.
- Keep tests deterministic and avoid network calls where possible; mock external services.
- CI will run the test matrix via GitHub Actions; ensure platform-specific steps are considered (macOS `tidy-html5` build, etc.).

### Pull Requests & Contributions
- Follow the `CONTRIBUTING.md` process: open an Issue for large or potentially breaking changes, work in a fork/branch, and use
	the provided PR template. Keep PRs focused and small.

### Commit Messages
- Use clear, imperative-style commit messages that summarize the change. PR titles should describe intent and link to issues when applicable.

### Release & Versioning
- Follow semantic versioning and bump `package.json` / `terminal/theme_version.html` when releasing a new theme version per
	`DEVELOPER_README.md` instructions.

## Domain Context
- This repository implements a MkDocs theme and supporting plugins; familiarity with MkDocs theme discovery,
	the `theme` and `plugins` entry points, and how MkDocs copies static assets during site build is important.
- Template changes affect HTML structure site-wide — exercise care to preserve accessibility and semantics.
- The `md-to-html` plugin transforms select Markdown blocks into raw HTML during the build; changes to this
	code may affect rendered documents and search indexing.

## Important Constraints
- Package metadata (version and some fields) is sourced via NodeJS tooling configured in Hatch; releases depend on
	that pipeline and `tool.hatch` configuration in `pyproject.toml`.
- Static assets and templates must be included in the wheel/sdist (see `tool.hatch.build.targets` in `pyproject.toml`).
- CI relies on platform-specific steps (e.g., building `tidy-html5` on macOS in CI). Local contributors may need platform
	specific prerequisites to run the full test matrix.

## External Dependencies

- MkDocs: https://www.mkdocs.org/
- Upstream Terminal.css project: https://github.com/Gioni06/terminal.css (visual styling)
- GitHub Actions for CI/CD and GitHub Pages deployment for documentation
- `tidy-html5` is used in some macOS CI steps and for HTML validation in tests/builds

## Quick References
 Entry points: `project.entry-points` in `pyproject.toml` expose `terminal` (theme) and `terminal/md-to-html` (plugin).
 Build/test commands (preferred Makefile targets):
 	- Install system prerequisites used in CI: `make install-test-prereqs`
 	- Install Python test requirements: `make install-test-requirements`
 	- Run quick lint + tests for local development: `make quick-tests`
 	- Run the full tox/test matrix locally: `make tox`
 	- Build the package (wheel/sdist) locally: `make build-theme`
 	- Serve the docs locally (documentation server): `make serve-docs`
 	- Serve the docs using the locally built theme: `make serve-local-theme`
 	- Lint only (if needed): `flake8 --ignore E501 terminal`

