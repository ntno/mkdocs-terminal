# Terminal for MkDocs Contributing Guide

A big welcome and thank you for considering contributing to Terminal for MkDocs!

Reading and following these guidelines will help us make the contribution process easy and effective for everyone involved. It also communicates that you agree to respect the time of the developers managing and developing this open source project. In return, we will reciprocate that respect by addressing your issue, assessing changes, and helping you finalize your pull requests.

## Quicklinks

- [Terminal for MkDocs Contributing Guide](#terminal-for-mkdocs-contributing-guide)
  - [Quicklinks](#quicklinks)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
    - [Issues](#issues)
    - [Pull Requests](#pull-requests)
- [Contribution](#contribution)
  - [Documentation](#documentation)
  - [Assets compilation](#assets-compilation)
  - [Environment setup](#environment-setup)
  - [Testing](#testing)
    - [Adding tests](#adding-tests)
    - [Running tests](#running-tests)
  - [Code quality tools](#code-quality-tools)
  - [CI Information](#ci-information)
  - [Repo-specific PR guidelines](#repo-specific-pr-guidelines)

## Code of Conduct

By participating and contributing to this project, you agree to uphold our [Code of Conduct](hhttps://github.com/ntno/mkdocs-terminal/blob/main/CODE_OF_CONDUCT.md).

## Getting Started

Contributions are made to this repo via Issues and Pull Requests (PRs). A few general guidelines that cover both:

- Search for existing Issues and PRs before creating your own.
- If you've never contributed before, see [the first timer's guide](https://auth0.com/blog/a-first-timers-guide-to-an-open-source-project/) for resources and tips on how to get started.

### Issues

Issues should be used to report problems with the theme, request a new feature, or to discuss potential changes before a PR is created. When you create a new Issue, a template will be loaded that will guide you through collecting and providing the information we need to investigate.

If you find an Issue that addresses the problem you're having, please add your own reproduction information to the existing issue rather than creating a new one. Adding a [reaction](https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) can also help be indicating to our maintainers that a particular problem is affecting more than just the reporter.

### Pull Requests

PRs to this theme are always welcome and can be a quick way to get your fix or improvement slated for the next release. In general, PRs should:

- Only fix/add the functionality in question **OR** address wide-spread whitespace/style issues, not both.
- Add unit or integration tests for fixed or changed functionality (if a test suite already exists).
- Address a single concern in the least number of changed lines as possible.
- Include documentation in the [mkdocs-terminal/documentation](https://github.com/ntno/mkdocs-terminal/tree/main/documentation/docs) docs.
- Be accompanied by a complete Pull Request template (loaded automatically when a PR is created).

For changes that address core functionality or would require breaking changes (e.g. a major release), it's best to open an Issue to discuss your proposal first.

In general, we follow the ["fork-and-pull" Git workflow](https://github.com/susam/gitpr)

1. Fork the repository to your own Github account
2. Clone the project to your machine
3. Create a branch locally with a succinct but descriptive name
4. Commit changes to the branch
5. Following any formatting and testing guidelines (see #testing)
6. Push changes to your fork
7. Open a PR in our repository and follow the PR template so that we can efficiently review the changes.








----
# Contribution

Please read [Auth0's contribution guidelines](https://github.com/auth0/open-source-template/blob/master/GENERAL-CONTRIBUTING.md).

## Documentation

- PR for docs site update, if needed
- Code-level documentation expectations
	- 100% documentation coverage for PRs
	- Include links to relevant Auth0 doc pages

## Assets compilation

Information about compiling CSS, JS, SVG, etc.

## Environment setup

Link to [README installation](README.md#installation) steps and include anything additional needed to contribute to the project.

## Testing


### Adding tests

General information about the test suite and how to format and structure tests.

### Running tests

Any additional information needed to run the test suite. Include `bash`-formatted commands like:

```bash
composer test
bundle exec rake test
```

Also include any information about essential manual tests.

## Code quality tools

Information about scripts to run before committing.

## CI Information

What CI checks for and how to pass.

## Repo-specific PR guidelines

Anything not covered in the general guidelines linked above.
